import os
import io
import time
import logging
from typing import List, Dict, Any, Tuple

from flask import Flask, request, jsonify, send_from_directory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def render_page_to_image(pdf_path: str, page_index: int, zoom: float = 2.0) -> Tuple[Any, float]:
    import fitz
    from PIL import Image
    import numpy as np
    doc = fitz.open(pdf_path)
    try:
        page = doc[page_index]
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        np_img = (np.array(img))
        return np_img, zoom
    finally:
        doc.close()


def detect_image_blocks(pdf_path: str) -> Dict[str, Any]:
    import fitz
    results: List[Dict[str, Any]] = []
    per_page_counts: Dict[int, int] = {}
    doc = fitz.open(pdf_path)
    try:
        for page_index in range(len(doc)):
            page = doc[page_index]
            raw = page.get_text("rawdict")
            page_count = 0
            for block in raw.get("blocks", []):
                if block.get("type") == 1:  # image block
                    bbox = block.get("bbox", None)
                    if isinstance(bbox, list) and len(bbox) == 4:
                        x1, y1, x2, y2 = bbox
                        width = float(x2 - x1)
                        height = float(y2 - y1)
                        area = width * height
                        results.append({
                            "page": page_index + 1,
                            "bbox": [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)],
                            "width_pt": round(width, 2),
                            "height_pt": round(height, 2),
                            "area_pt2": round(area, 2),
                            "method": "rawdict-image-block"
                        })
                        page_count += 1
            per_page_counts[page_index + 1] = page_count

        # Also collect embedded image metadata counts (no position)
        pages_image_meta = []
        for page_index in range(len(doc)):
            page = doc[page_index]
            imgs = page.get_images(full=True)
            pages_image_meta.append({
                "page": page_index + 1,
                "embedded_images": len(imgs)
            })

        return {
            "images": results,
            "per_page_counts": per_page_counts,
            "embedded_counts": pages_image_meta,
            "total_images": len(results)
        }
    finally:
        doc.close()


def label_quality(dpi_x: float, dpi_y: float) -> str:
    dpi = min(dpi_x, dpi_y)
    if dpi >= 300:
        return "high"
    if dpi >= 150:
        return "medium"
    if dpi >= 72:
        return "low"
    return "very_low"


def detect_images_highlevel_with_dpi(pdf_path: str) -> List[Dict[str, Any]]:
    """High-level PyMuPDF: match image XObjects (pixel dims) to placed image blocks (bbox) and compute DPI."""
    import fitz
    results: List[Dict[str, Any]] = []
    doc = fitz.open(pdf_path)
    try:
        for page_index in range(len(doc)):
            page = doc[page_index]
            # Map of image xref -> (width_px, height_px)
            xref_dims: Dict[int, Tuple[int, int]] = {}
            for img in page.get_images(full=True):
                try:
                    xref = int(img[0])
                    # width_px, height_px indexes: see PyMuPDF docs → (width, height) at positions 2,3
                    wpx = int(img[2]); hpx = int(img[3])
                    xref_dims[xref] = (wpx, hpx)
                except Exception:
                    continue

            # Find placed image blocks with bbox
            raw = page.get_text("rawdict")
            for block in raw.get("blocks", []):
                if block.get("type") != 1:
                    continue
                bbox = block.get("bbox", None)
                if not (isinstance(bbox, list) and len(bbox) == 4):
                    continue
                x1, y1, x2, y2 = bbox
                width_pts = float(x2 - x1)
                height_pts = float(y2 - y1)

                # Heuristic: choose the largest xref on this page as candidate when unknown
                # PyMuPDF rawdict does not expose xref per block reliably, so approximate
                wpx = hpx = None
                if xref_dims:
                    # pick the pixel dims with closest aspect ratio
                    aspect_block = width_pts / max(1e-6, height_pts)
                    best = None; best_diff = 1e9
                    for (pw, ph) in xref_dims.values():
                        ar = pw / max(1e-6, ph)
                        diff = abs(ar - aspect_block)
                        if diff < best_diff:
                            best = (pw, ph); best_diff = diff
                    if best:
                        wpx, hpx = best

                # If we have pixel dims, compute DPI
                dpi_x = dpi_y = None
                quality = None
                if wpx and hpx and width_pts > 0 and height_pts > 0:
                    dpi_x = (wpx * 72.0) / width_pts
                    dpi_y = (hpx * 72.0) / height_pts
                    quality = label_quality(dpi_x, dpi_y)

                results.append({
                    "page": page_index + 1,
                    "bbox": [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)],
                    "width_pts": round(width_pts, 2),
                    "height_pts": round(height_pts, 2),
                    "width_px": wpx,
                    "height_px": hpx,
                    "dpi_x": round(dpi_x, 1) if dpi_x else None,
                    "dpi_y": round(dpi_y, 1) if dpi_y else None,
                    "quality": quality,
                    "method": "highlevel-xobject+rawdict",
                    "coord_sys": "pdf_tl"
                })
        return results
    finally:
        doc.close()


def detect_images_lowlevel_with_dpi(pdf_path: str) -> List[Dict[str, Any]]:
    """Low-level pikepdf: enumerate /XObject /Image, parse content stream for placement matrix (Do + CTM)."""
    import pikepdf
    import re
    results: List[Dict[str, Any]] = []
    try:
        with pikepdf.open(pdf_path) as pdf:
            for page_index, page in enumerate(pdf.pages, start=1):
                resources = page.get("/Resources")
                if resources is None:
                    continue
                xobjects = resources.get("/XObject")
                if not isinstance(xobjects, pikepdf.Dictionary):
                    # still try content stream for Do operators
                    pass

                # Extract content stream bytes
                contents = page.get("/Contents")
                if contents is None:
                    continue
                if isinstance(contents, pikepdf.Stream):
                    streams = [contents]
                elif isinstance(contents, pikepdf.Array):
                    streams = [obj for obj in contents if isinstance(obj, pikepdf.Stream)]
                else:
                    streams = []

                # Parse a very simplified graphics state: track CTM and image Do calls
                # We assume placements like: q a b c d e f cm /ImX Do Q
                # This is a heuristic and may miss complex cases, but often works.
                content_bytes = b"".join(s.read_bytes() for s in streams)
                text = content_bytes.decode('latin-1', errors='ignore')
                tokens = text.replace('\n', ' ').split()
                # current matrix a b c d e f
                ctm = [1, 0, 0, 1, 0, 0]
                i = 0
                while i < len(tokens):
                    tok = tokens[i]
                    if tok == 'q':
                        i += 1
                        continue
                    elif tok == 'Q':
                        i += 1
                        continue
                    elif tok == 'cm' and i >= 6:
                        try:
                            a = float(tokens[i-6]); b = float(tokens[i-5]); c = float(tokens[i-4]); d = float(tokens[i-3]); e = float(tokens[i-2]); f = float(tokens[i-1])
                            ctm = [a, b, c, d, e, f]
                        except Exception:
                            pass
                        i += 1
                        continue
                    elif tok == 'Do' and i >= 1:
                        name = tokens[i-1]
                        if name.startswith('/'):
                            # Try to fetch image XObject by name
                            if isinstance(xobjects, pikepdf.Dictionary) and name in xobjects:
                                xobj = xobjects[name]
                                if isinstance(xobj, pikepdf.Stream):
                                    sub = xobj.get('/Subtype')
                                    if str(sub) == '/Image':
                                        wpx = int(xobj.get('/Width', 0))
                                        hpx = int(xobj.get('/Height', 0))
                                        # placed size from CTM (|a d|)
                                        width_pts = abs(ctm[0])
                                        height_pts = abs(ctm[3])
                                        dpi_x = (wpx * 72.0) / width_pts if width_pts > 0 else None
                                        dpi_y = (hpx * 72.0) / height_pts if height_pts > 0 else None
                                        quality = label_quality(dpi_x or 0, dpi_y or 0) if (dpi_x and dpi_y) else None
                                        # bbox in page coords approx (translate e,f with size a,d)
                                        x1 = float(ctm[4]); y1 = float(ctm[5])
                                        x2 = x1 + width_pts; y2 = y1 + height_pts
                                        results.append({
                                            'page': page_index,
                                            'bbox': [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)],
                                            'width_pts': round(width_pts, 2),
                                            'height_pts': round(height_pts, 2),
                                            'width_px': wpx,
                                            'height_px': hpx,
                                            'dpi_x': round(dpi_x, 1) if dpi_x else None,
                                            'dpi_y': round(dpi_y, 1) if dpi_y else None,
                                            'quality': quality,
                                            'method': 'lowlevel-xobject+ctm',
                                            'coord_sys': 'pdf_bl'
                                        })
                        i += 1
                        continue
                    else:
                        i += 1
                # end token loop
        return results
    except Exception:
        return []
def detect_images_by_render_segmentation(pdf_path: str, zoom: float = 2.0) -> List[Dict[str, Any]]:
    """Render pages and segment large photo-like regions using edge density + color variance heuristics."""
    import numpy as np
    import cv2
    import fitz
    dets: List[Dict[str, Any]] = []
    doc = fitz.open(pdf_path)
    try:
        for page_index in range(len(doc)):
            page = doc[page_index]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            np_img = cv2.cvtColor(np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3], cv2.COLOR_RGB2BGR)

            # downscale for speed
            small = cv2.resize(np_img, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            # edge map + blur
            edges = cv2.Canny(gray, 50, 150)
            edges = cv2.GaussianBlur(edges, (5, 5), 1.2)
            # threshold on low edge density (photo regions are often low edge-density blobs)
            _, low_edges = cv2.threshold(edges, 20, 255, cv2.THRESH_BINARY_INV)
            # morphology open/close to unify regions
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(low_edges, cv2.MORPH_OPEN, kernel, iterations=1)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
            # find contours of low-edge regions
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            H, W = small.shape[:2]
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                area = w * h
                if area < (H * W * 0.02):  # skip tiny regions
                    continue
                aspect = w / max(1, h)
                if aspect < 0.5 or aspect > 10:
                    continue
                # compute color variance to avoid flat backgrounds
                roi = small[y:y+h, x:x+w]
                var = float(np.var(roi))
                if var < 200:  # too flat, likely background
                    continue
                # map back to PDF pt coordinates (reverse downscale and zoom)
                sx1 = int(round(x / 0.5)); sy1 = int(round(y / 0.5))
                sx2 = int(round((x + w) / 0.5)); sy2 = int(round((y + h) / 0.5))
                px1 = round(sx1 / zoom, 2); py1 = round(sy1 / zoom, 2)
                px2 = round(sx2 / zoom, 2); py2 = round(sy2 / zoom, 2)
                dets.append({
                    "page": page_index + 1,
                    "bbox": [px1, py1, px2, py2],
                    "method": "render-segmentation",
                    "coord_sys": "pdf_tl",
                    "color_variance": round(var, 1)
                })
    finally:
        doc.close()
    return dets

def save_image_crops(pdf_path: str, detections: List[Dict[str, Any]], zoom: float = 2.0, save_dir: str = "/shared/images") -> List[Dict[str, Any]]:
    """Render precise crops using PyMuPDF clip rectangles (in pt) to avoid pixel rounding errors."""
    import fitz  # PyMuPDF
    os.makedirs(save_dir, exist_ok=True)

    out: List[Dict[str, Any]] = []
    doc = fitz.open(pdf_path)
    try:
        for det in detections:
            try:
                page_num = int(det["page"]) - 1
                x1, y1, x2, y2 = [float(v) for v in det["bbox"]]
                # Normalize bbox to PyMuPDF coordinate system (origin top-left)
                # If detection coord_sys is pdf_bl (origin bottom-left), convert Y using page height
                page = doc[page_num]
                page_height = float(page.rect.height)
                coord_sys = det.get("coord_sys", "pdf_tl")
                if coord_sys == "pdf_bl":
                    # convert bottom-left to top-left: y' = page_height - y
                    y1_conv = page_height - y2
                    y2_conv = page_height - y1
                    y1, y2 = y1_conv, y2_conv
                # Clip rect in page points (top-left coords)
                rect = fitz.Rect(x1, y1, x2, y2)
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat, clip=rect)
                fname = f"image_{int(time.time())}_{page_num+1}.png"
                fpath = os.path.join(save_dir, fname)
                pix.save(fpath)
                det_copy = {**det}
                det_copy["image_path"] = fpath
                det_copy["image_url_path"] = f"/files/{fname}"
                out.append(det_copy)
            except Exception as e:
                logger.warning(f"Crop save failed: {e}")
                out.append(det)
    finally:
        doc.close()
    return out


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "image-profile-service", "version": "1.0"})


@app.route("/images/from-path", methods=["POST"])
def images_from_path():
    try:
        data = request.get_json(silent=True) or {}
        pdf_path = data.get("filepath")
        zoom = float(data.get("zoom", 2.0))
        save_thumbnails = bool(data.get("save_thumbnails", True))

        if not pdf_path or not os.path.exists(pdf_path):
            return jsonify({"success": False, "error": "File not found or no filepath provided"}), 400
        if not pdf_path.lower().endswith(".pdf"):
            return jsonify({"success": False, "error": "File must be a PDF"}), 400

        # Strategy: High-level first (with DPI), then low-level CTM parsing, then render segmentation fallback
        hl = detect_images_highlevel_with_dpi(pdf_path)
        detections = hl
        if not detections:
            ll = detect_images_lowlevel_with_dpi(pdf_path)
            detections = ll
        if not detections:
            seg = detect_images_by_render_segmentation(pdf_path, zoom=zoom)
            detections = seg

        # Build det summary for response consistency
        per_page_counts: Dict[int, int] = {}
        for d in detections:
            per_page_counts[d["page"]] = per_page_counts.get(d["page"], 0) + 1
        det = {
            "images": detections,
            "per_page_counts": per_page_counts,
            "total_images": len(detections)
        }

        # optionally save crops
        if save_thumbnails and detections:
            save_dir = os.getenv("IMAGES_SAVE_DIR", "/shared/images")
            detections = save_image_crops(pdf_path, detections, zoom=zoom, save_dir=save_dir)
            # add absolute URL base
            base = request.host_url[:-1] if request.host_url.endswith('/') else request.host_url
            for d in detections:
                if d.get("image_url_path"):
                    d["image_url"] = f"{base}{d['image_url_path']}"

        return jsonify({
            "success": True,
            "filepath": pdf_path,
            "total_images": det.get("total_images", 0),
            "per_page_counts": det.get("per_page_counts", {}),
            "embedded_counts": det.get("embedded_counts", []),
            "images": detections
        })

    except Exception as e:
        logger.exception("Error detecting images")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/files/<path:filename>', methods=['GET'])
def serve_saved_file(filename):
    directory = os.getenv("IMAGES_SAVE_DIR", "/shared/images")
    return send_from_directory(directory, filename)


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    app.run(host=host, port=port)


