import os
import io
import json
import logging
from typing import List, Dict, Any, Tuple

from flask import Flask, request, jsonify, send_from_directory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def _extract_page_image(pdf_path: str, page_index: int = 0, zoom: float = 2.0) -> Tuple[Any, Tuple[int, int]]:
    import fitz
    from PIL import Image
    import numpy as np
    doc = fitz.open(pdf_path)
    try:
        page = doc[page_index]
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        np_img = np.array(img)
        return np_img, (page.rect.width * zoom, page.rect.height * zoom)
    finally:
        doc.close()


def _detect_top_right_bosch_logo(np_img) -> List[Dict[str, Any]]:
    """Detect a Bosch logo heuristically in the top-right area using OpenCV.
    Heuristics:
      - Crop top-right 35% width x 25% height region
      - Find red-dominant blobs and circular features (gear icon), and/or 'BOSCH' word via template-free cues
    Returns list of candidate bboxes in page coordinates of the cropped region mapped back.
    """
    import cv2
    import numpy as np

    h, w, _ = np_img.shape
    crop_w = int(w * 0.35)
    crop_h = int(h * 0.25)
    x0 = w - crop_w
    y0 = 0
    roi = np_img[y0:y0+crop_h, x0:x0+crop_w]

    # Convert to HSV for robust red mask
    hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
    # red has two ranges in HSV
    lower_red1 = np.array([0, 80, 80]); upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 80, 80]); upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Morphology to clean
    kernel = np.ones((3, 3), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours of red blobs
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch
        if area < 200:  # filter noise
            continue
        aspect = cw / max(1, ch)
        if aspect < 0.5 or aspect > 5.0:
            continue
        # Expand bbox slightly
        pad = 4
        x1 = max(0, x - pad); y1 = max(0, y - pad)
        x2 = min(crop_w, x + cw + pad); y2 = min(crop_h, y + ch + pad)
        candidates.append((x1, y1, x2, y2))

    # Merge overlapping candidates
    def iou(a, b):
        ax1, ay1, ax2, ay2 = a; bx1, by1, bx2, by2 = b
        inter_x1 = max(ax1, bx1); inter_y1 = max(ay1, by1)
        inter_x2 = min(ax2, bx2); inter_y2 = min(ay2, by2)
        inter = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
        area_a = (ax2 - ax1) * (ay2 - ay1)
        area_b = (bx2 - bx1) * (by2 - by1)
        denom = area_a + area_b - inter
        return inter / denom if denom > 0 else 0

    merged = []
    for c in candidates:
        merged_flag = False
        for i, m in enumerate(merged):
            if iou(c, m) > 0.3:
                nx1 = min(c[0], m[0]); ny1 = min(c[1], m[1])
                nx2 = max(c[2], m[2]); ny2 = max(c[3], m[3])
                merged[i] = (nx1, ny1, nx2, ny2)
                merged_flag = True
                break
        if not merged_flag:
            merged.append(c)

    # Map back to full page coordinates
    results = []
    for (mx1, my1, mx2, my2) in merged:
        bx1 = x0 + mx1; by1 = y0 + my1; bx2 = x0 + mx2; by2 = y0 + my2
        results.append({
            "page": 1,
            "bbox": [round(float(bx1), 2), round(float(by1), 2), round(float(bx2), 2), round(float(by2), 2)],
            "confidence": 0.6,
            "method": "top-right-red-heuristic"
        })

    return results


def _detect_monochrome_logo(np_img) -> List[Dict[str, Any]]:
    """Detect dark monochrome logo marks in the same top-right ROI by edge/shape cues."""
    import cv2
    import numpy as np
    h, w, _ = np_img.shape
    crop_w = int(w * 0.35)
    crop_h = int(h * 0.25)
    x0 = w - crop_w
    y0 = 0
    roi = np_img[y0:y0+crop_h, x0:x0+crop_w]

    gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
    # adaptive threshold to catch dark elements
    thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 31, 10)
    kernel = np.ones((3, 3), np.uint8)
    thr = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=1)
    thr = cv2.morphologyEx(thr, cv2.MORPH_CLOSE, kernel, iterations=1)

    contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    results = []
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch
        if area < 250:
            continue
        aspect = cw / max(1, ch)
        if 0.4 <= aspect <= 8.0:
            bx1 = x0 + x; by1 = y0 + y; bx2 = x0 + x + cw; by2 = y0 + y + ch
            results.append({
                "page": 1,
                "bbox": [round(float(bx1), 2), round(float(by1), 2), round(float(bx2), 2), round(float(by2), 2)],
                "confidence": 0.5,
                "method": "top-right-mono-heuristic"
            })
    return results


def _ocr_check_bosch(np_img, bbox: List[float]) -> float:
    """OCR on bbox region; return confidence boost if 'BOSCH' found."""
    import pytesseract
    from PIL import Image
    import numpy as np
    x1, y1, x2, y2 = [int(round(v)) for v in bbox]
    x1 = max(0, x1); y1 = max(0, y1); x2 = max(x1+1, x2); y2 = max(y1+1, y2)
    crop = np_img[y1:y2, x1:x2]
    if crop.size == 0:
        return 0.0
    pil = Image.fromarray(crop)
    text = pytesseract.image_to_string(pil, config='--psm 6')
    if 'BOSCH' in text.upper():
        return 0.25
    return 0.0


def _bbox_area(b: List[float]) -> float:
    try:
        return max(0.0, (b[2] - b[0])) * max(0.0, (b[3] - b[1]))
    except Exception:
        return 0.0


def _union_bbox(boxes: List[List[float]]) -> List[float]:
    x1 = min(b[0] for b in boxes)
    y1 = min(b[1] for b in boxes)
    x2 = max(b[2] for b in boxes)
    y2 = max(b[3] for b in boxes)
    return [round(float(x1), 2), round(float(y1), 2), round(float(x2), 2), round(float(y2), 2)]


def _detect_circular_mark(np_img) -> List[Dict[str, Any]]:
    """Detect circular mark (gear/icon) in top-right ROI using HoughCircles and contour circularity."""
    import cv2
    import numpy as np
    h, w, _ = np_img.shape
    crop_w = int(w * 0.35)
    crop_h = int(h * 0.25)
    x0 = w - crop_w
    y0 = 0
    roi = np_img[y0:y0+crop_h, x0:x0+crop_w]

    gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 1.2)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=15,
                               param1=100, param2=18,
                               minRadius=int(max(6, min(crop_w, crop_h) * 0.02)),
                               maxRadius=int(min(crop_w, crop_h) * 0.15))
    results: List[Dict[str, Any]] = []
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (cx, cy, r) in circles:
            x1 = max(0, cx - r - 2); y1 = max(0, cy - r - 2)
            x2 = min(crop_w, cx + r + 2); y2 = min(crop_h, cy + r + 2)
            bx1 = x0 + x1; by1 = y0 + y1; bx2 = x0 + x2; by2 = y0 + y2
            results.append({
                "page": 1,
                "bbox": [round(float(bx1), 2), round(float(by1), 2), round(float(bx2), 2), round(float(by2), 2)],
                "confidence": 0.55,
                "method": "top-right-circle-heuristic"
            })

    # Fallback via contour circularity
    thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 8)
    contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 120:
            continue
        perim = cv2.arcLength(cnt, True)
        if perim <= 0:
            continue
        circularity = 4 * 3.14159 * (area / (perim * perim))
        if circularity > 0.6:
            x, y, cw, ch = cv2.boundingRect(cnt)
            bx1 = x0 + x; by1 = y0 + y; bx2 = x0 + x + cw; by2 = y0 + y + ch
            results.append({
                "page": 1,
                "bbox": [round(float(bx1), 2), round(float(by1), 2), round(float(bx2), 2), round(float(by2), 2)],
                "confidence": 0.5,
                "method": "top-right-circle-circularity"
            })

    # Deduplicate overlapping circle detections
    dedup: List[Dict[str, Any]] = []
    def iou_box(b1, b2):
        x1, y1, x2, y2 = b1; a1, b1y, a2, b2y = b2
        inter_x1 = max(x1, a1); inter_y1 = max(y1, b1y)
        inter_x2 = min(x2, a2); inter_y2 = min(y2, b2y)
        inter = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
        area1 = _bbox_area(b1); area2 = _bbox_area(b2)
        denom = area1 + area2 - inter
        return inter / denom if denom > 0 else 0
    for r in results:
        exists = False
        for i, d in enumerate(dedup):
            if iou_box(r['bbox'], d['bbox']) > 0.4:
                # merge
                merged = _union_bbox([r['bbox'], d['bbox']])
                d['bbox'] = merged
                d['confidence'] = max(d['confidence'], r['confidence'])
                exists = True
                break
        if not exists:
            dedup.append(r)
    return dedup
def _select_single_logo(dets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Select a single best logo per page. Strategy:
    - Prefer detections with brand == BOSCH and highest confidence
    - Else prefer red-heuristic with largest area
    - Else union of all detections into one box, confidence=max
    Returns a list with at most one detection for the whole page (page 1 assumed).
    """
    if not dets:
        return []
    # group by page (we currently only process page 1)
    by_brand = [d for d in dets if str(d.get('brand', '')).upper() == 'BOSCH']
    if by_brand:
        best = max(by_brand, key=lambda d: d.get('confidence', 0))
        best['method'] = f"{best.get('method','')}+select-brand"
        return [best]

    red = [d for d in dets if 'red-heuristic' in str(d.get('method',''))]
    if red:
        best = max(red, key=lambda d: _bbox_area(d.get('bbox', [0,0,0,0])))
        best['method'] = f"{best.get('method','')}+select-red"
        return [best]

    # fallback: union all boxes
    boxes = [d.get('bbox') for d in dets if d.get('bbox')]
    if not boxes:
        return []
    uni = _union_bbox(boxes)
    conf = max(d.get('confidence', 0.5) for d in dets)
    return [{
        'page': dets[0].get('page', 1),
        'bbox': uni,
        'confidence': round(conf, 2),
        'method': 'merged-union'
    }]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "logo-profile-service", "version": "1.0"})


@app.route("/logos/from-path", methods=["POST"])
def logos_from_path():
    try:
        data = request.get_json(silent=True) or {}
        pdf_path = data.get("filepath")
        method = (data.get("method") or "intelligent").lower()

        if not pdf_path or not os.path.exists(pdf_path):
            return jsonify({"success": False, "error": "File not found or no filepath provided"}), 400
        if not pdf_path.lower().endswith(".pdf"):
            return jsonify({"success": False, "error": "File must be a PDF"}), 400

        results: Dict[str, Any] = {"success": True, "filepath": pdf_path, "logos": []}

        # New approach: purely heuristic, no legacy dependencies
        np_img, _ = _extract_page_image(pdf_path, page_index=0, zoom=float(data.get("zoom", 2.0)))
        red_detections = _detect_top_right_bosch_logo(np_img)
        mono_detections = _detect_monochrome_logo(np_img)
        circle_detections = _detect_circular_mark(np_img)

        # Merge and apply OCR check
        merged = red_detections + mono_detections + circle_detections
        for d in merged:
            try:
                boost = _ocr_check_bosch(np_img, d["bbox"])
                d["confidence"] = round(min(1.0, d.get("confidence", 0.5) + boost), 2)
                if boost > 0 and not d.get("brand"):
                    d["brand"] = "BOSCH"
            except Exception:
                continue

        # Reduce to a single logo box per Seite
        single = _select_single_logo(merged)

        # If a circle mark is near the selected box, expand to include it
        if single and circle_detections:
            sx1, sy1, sx2, sy2 = single[0]['bbox']
            s_cx = (sx1 + sx2) / 2.0; s_cy = (sy1 + sy2) / 2.0
            def center(b):
                x1, y1, x2, y2 = b; return ((x1 + x2)/2.0, (y1 + y2)/2.0)
            # choose nearest circle center
            nearest = None; min_dist = 1e9
            for c in circle_detections:
                cx, cy = center(c['bbox'])
                dist = abs(cx - s_cx) + abs(cy - s_cy)
                if dist < min_dist:
                    min_dist = dist; nearest = c
            if nearest:
                single[0]['bbox'] = _union_bbox([single[0]['bbox'], nearest['bbox']])
                single[0]['method'] = f"{single[0].get('method','')}+union-circle"

        # Asymmetric fixed padding: left=50% width, top/right/bottom=20%
        # Allow override via request, else use defaults (0.5 left, 0.2 others)
        pad_left = float(data.get('pad_left_ratio', 0.5))
        pad_other = float(data.get('pad_other_ratio', 0.2))
        if single:
            x1, y1, x2, y2 = single[0]['bbox']
            bw = x2 - x1; bh = y2 - y1
            px1 = x1 - bw * pad_left
            py1 = y1 - bh * pad_other
            px2 = x2 + bw * pad_other
            py2 = y2 + bh * pad_other
            # clip to image bounds
            ph, pw = np_img.shape[:2]
            px1 = max(0.0, px1); py1 = max(0.0, py1)
            px2 = min(float(pw - 1), px2); py2 = min(float(ph - 1), py2)
            single[0]['bbox_padded'] = [round(px1, 2), round(py1, 2), round(px2, 2), round(py2, 2)]

        # Save crop and attach URL if present
        if single:
            # Save under configurable dir, defaulting to /shared/logos
            save_dir = os.getenv("LOGO_SAVE_DIR", "/shared/logos")
            try:
                # Ensure path exists
                os.makedirs(save_dir, exist_ok=True)
                # Save crop image
                from PIL import Image
                import numpy as np
                # Prefer padded bbox if present
                crop_box = single[0].get("bbox_padded", single[0]["bbox"])
                x1, y1, x2, y2 = [int(round(v)) for v in crop_box]
                x1 = max(0, x1); y1 = max(0, y1)
                x2 = max(x1 + 1, x2); y2 = max(y1 + 1, y2)
                crop = np_img[y1:y2, x1:x2]
                import time
                filename = f"logo_{int(time.time())}.png"
                file_path = os.path.join(save_dir, filename)
                Image.fromarray(crop).save(file_path, format='PNG')

                # Build URL
                url_path = f"/files/{filename}"
                base = request.host_url[:-1] if request.host_url.endswith('/') else request.host_url
                single[0]["image_path"] = file_path
                single[0]["image_url"] = f"{base}{url_path}"
                single[0]["image_url_path"] = url_path
            except Exception as e:
                logger.warning(f"Failed to save logo crop: {e}")

        results["logos"] = single

        results["total_logos"] = len(results.get("logos", []))
        return jsonify(results)

    except Exception as e:
        logger.exception("Error detecting logos")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    app.run(host=host, port=port)


@app.route('/files/<path:filename>', methods=['GET'])
def serve_saved_file(filename):
    """Serve saved logo crops from the LOGO_SAVE_DIR."""
    directory = os.getenv("LOGO_SAVE_DIR", "/shared/logos")
    return send_from_directory(directory, filename)


