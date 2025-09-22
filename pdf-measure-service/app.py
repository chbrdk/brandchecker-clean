import os
import json
import logging
from typing import List, Dict, Any

from flask import Flask, request, jsonify, send_from_directory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# ==== Minimal pdfmeasure implementation (modular) ====

# pdfmeasure/units.py
PT_TO_MM = 25.4 / 72.0

def pt_to_mm(pt: float, user_unit: float = 1.0) -> float:
    return pt * user_unit * PT_TO_MM

def bbox_pt_to_mm(b, user_unit=1.0):
    return [pt_to_mm(v, user_unit) for v in b]


# pdfmeasure/page_reader.py
def read_page_context(page):
    mediabox = page.mediabox
    rotate = page.rotation or 0
    user_unit = getattr(page, "userunit", 1.0) or 1.0
    return {
        "media_w": float(mediabox.width),
        "media_h": float(mediabox.height),
        "rotate": int(rotate),
        "user_unit": float(user_unit),
    }


# pdfmeasure/extractor_images.py
def _get_image_px(doc, xref: int):
    try:
        # PyMuPDF >=1.21
        img = doc.extract_image(xref)
        return [int(img.get("width", 0)), int(img.get("height", 0))]
    except Exception:
        return [None, None]

def extract_images(page, ctx):
    items = []
    doc = page.parent
    for entry in page.get_images(full=True):
        try:
            xref = int(entry[0])
        except Exception:
            continue
        px = _get_image_px(doc, xref)
        for r in page.get_image_rects(xref):
            bbox = [float(r.x0), float(r.y0), float(r.x1), float(r.y1)]
            items.append({
                "type": "image",
                "bbox_pt": bbox,
                "properties": {
                    "image_xref": xref,
                    "image_pixel_size": px,
                }
            })
    return items


# pdfmeasure/extractor_vectors.py
def _item_op(it):
    # Support PyMuPDF returning dict-like or tuple-based items
    if isinstance(it, dict):
        return it.get("op")
    if isinstance(it, (list, tuple)) and len(it) > 0:
        return it[0]
    return None

def _is_axis_aligned_rect(drawing: Dict[str, Any]) -> bool:
    items = drawing.get("items", [])
    # direct rectangle op
    if len(items) == 1 and _item_op(items[0]) == "re":
        return True
    # Heuristic: move + 3 lines + close (5 ops)
    ops = [_item_op(it) for it in items]
    if all(op in ("m", "l", "h") for op in ops if op is not None) and len(items) >= 4:
        # very rough, accept as rect-like
        return True
    return False

def extract_vectors(page, ctx):
    items: List[Dict[str, Any]] = []
    for d in page.get_drawings():
        r = d.get("rect")
        if not r:
            continue
        bbox = [float(r.x0), float(r.y0), float(r.x1), float(r.y1)]
        vtype = "rectangle" if _is_axis_aligned_rect(d) else "vector_path"
        items.append({
            "type": vtype,
            "bbox_pt": bbox,
            "properties": {
                "path_ops": [_item_op(it) for it in d.get("items", [])],
                "stroke_width_pt": d.get("width")
            }
        })
    return items


# pdfmeasure/extractor_text.py
def extract_text(page, ctx, glyph_level=True):
    items: List[Dict[str, Any]] = []
    raw = page.get_text("rawdict")
    for block in raw.get("blocks", []):
        for line in block.get("lines", []):
            lb = line.get("bbox")
            if lb:
                items.append({
                    "type": "text_line",
                    "bbox_pt": [float(v) for v in lb],
                    "properties": {}
                })
            if not glyph_level:
                continue
            for span in line.get("spans", []):
                font = span.get("font")
                size = span.get("size")
                scale_x = span.get("scalex", 100)
                for ch in span.get("chars", []):
                    cb = ch.get("bbox")
                    if not cb:
                        continue
                    items.append({
                        "type": "text_glyph",
                        "bbox_pt": [float(v) for v in cb],
                        "properties": {
                            "glyph": ch.get("c"),
                            "font_name": font,
                            "font_size_pt": size,
                            "h_scaling": scale_x
                        }
                    })
    return items


# pdfmeasure/normalize.py
def _normalize_rotation(bbox, w, h, rot):
    x0, y0, x1, y1 = bbox
    if rot == 0:
        return [x0, y0, x1, y1]
    if rot == 90:
        return [y0, w - x1, y1, w - x0]
    if rot == 180:
        return [w - x1, h - y1, w - x0, h - y0]
    if rot == 270:
        return [h - y1, x0, h - y0, x1]
    return [x0, y0, x1, y1]

def finalize_items(doc_path: str, page_no: int, ctx: Dict[str, Any], items: List[Dict[str, Any]]):
    import uuid
    out = []
    for it in items:
        bbox_pt = _normalize_rotation(it["bbox_pt"], ctx["media_w"], ctx["media_h"], ctx["rotate"])
        out.append({
            "doc_path": doc_path,
            "page_index": page_no - 1,
            "page_number": page_no,
            "page_size_pt": [ctx["media_w"], ctx["media_h"]],
            "type": it["type"],
            "id": str(uuid.uuid4()),
            "bbox_pt": bbox_pt,
            "bbox_mm": bbox_pt_to_mm(bbox_pt, ctx["user_unit"]),
            "visible_bbox_pt": it.get("visible_bbox_pt"),
            "stroke_width_pt": it.get("properties", {}).get("stroke_width_pt"),
            "matrix": it.get("matrix"),
            "rotation_deg": ctx["rotate"],
            "user_unit": ctx["user_unit"],
            "properties": it.get("properties", {})
        })
    return out


# writers
def write_jsonl(path, items):
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

def write_csv(path, items):
    import csv
    cols = ["page_number", "type", "x0", "y0", "x1", "y1", "x0mm", "y0mm", "x1mm", "y1mm"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for it in items:
            x0, y0, x1, y1 = it["bbox_pt"]
            x0m, y0m, x1m, y1m = it["bbox_mm"]
            w.writerow([it["page_number"], it["type"], x0, y0, x1, y1, x0m, y0m, x1m, y1m])


def measure_pdf(doc_path: str, out_dir: str = None, per_page: bool = False, max_pages: int = None,
                layout_only_outputs: bool = False) -> Dict[str, Any]:
    import fitz
    os.makedirs(out_dir, exist_ok=True) if out_dir else None

    doc = fitz.open(doc_path)
    all_items: List[Dict[str, Any]] = []
    layout_only_all: List[Dict[str, Any]] = []
    for i, page in enumerate(doc, start=1):
        if max_pages and i > max_pages:
            break
        ctx = read_page_context(page)
        page_items: List[Dict[str, Any]] = []
        page_items += extract_vectors(page, ctx)
        page_items += extract_images(page, ctx)
        page_items += extract_text(page, ctx, glyph_level=True)
        fin = finalize_items(doc_path, i, ctx, page_items)
        all_items.extend(fin)
        # layout boxes per page
        layout_boxes = compute_layout_boxes(fin, ctx)
        # Attach as synthetic items for output (type: text_block/image_block)
        layout_items_page: List[Dict[str, Any]] = []
        for lb in layout_boxes:
            layout_item = {
                "doc_path": doc_path,
                "page_index": i - 1,
                "page_number": i,
                "page_size_pt": [ctx["media_w"], ctx["media_h"]],
                "type": lb["type"],
                "id": f"layout-{i}-{lb['type']}-{lb['bbox_pt'][0]}-{lb['bbox_pt'][1]}",
                "bbox_pt": lb["bbox_pt"],
                "bbox_mm": lb["bbox_mm"],
                "visible_bbox_pt": None,
                "stroke_width_pt": None,
                "matrix": None,
                "rotation_deg": ctx["rotate"],
                "user_unit": ctx["user_unit"],
                "properties": {"children_count": lb["children_count"]}
            }
            all_items.append(layout_item)
            layout_items_page.append(layout_item)

        # optional per-page layout-only outputs
        if out_dir and per_page and layout_only_outputs and layout_items_page:
            base = os.path.join(out_dir, f"{os.path.basename(doc_path)}.page-{i:04d}_layout")
            write_jsonl(base + ".jsonl", layout_items_page)
            write_csv(base + ".csv", layout_items_page)

        if per_page and out_dir:
            base = os.path.join(out_dir, f"{os.path.basename(doc_path)}.page-{i:04d}")
            write_jsonl(base + ".jsonl", fin)
            write_csv(base + ".csv", fin)

    if not per_page and out_dir:
        base = os.path.join(out_dir, f"{os.path.basename(doc_path)}")
        write_jsonl(base + ".jsonl", all_items)
        write_csv(base + ".csv", all_items)
        if layout_only_outputs:
            # Write layout-only aggregates
            layout_only_all = [it for it in all_items if it.get("type") in ("text_block", "image_block")]
            if layout_only_all:
                write_jsonl(base + "_layout.jsonl", layout_only_all)
                write_csv(base + "_layout.csv", layout_only_all)

    doc.close()
    return {"total_items": len(all_items), "items": all_items}


def _rect_union(a, b):
    ax0, ay0, ax1, ay1 = a; bx0, by0, bx1, by1 = b
    return [min(ax0, bx0), min(ay0, by0), max(ax1, bx1), max(ay1, by1)]

def _rect_overlap_h(a, b) -> float:
    ax0, ay0, ax1, ay1 = a; bx0, by0, bx1, by1 = b
    inter = max(0.0, min(ax1, bx1) - max(ax0, bx0))
    width = max(1e-6, min(ax1-ax0, bx1-bx0))
    return inter / width

def compute_layout_boxes(items: List[Dict[str, Any]], ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Group text lines into blocks; images as blocks; merge overlapping images
    text_lines = [it for it in items if it.get("type") == "text_line"]
    images = [it for it in items if it.get("type") == "image"]

    # Sort text lines by top y then x
    text_lines_sorted = sorted(text_lines, key=lambda it: (it["bbox_pt"][1], it["bbox_pt"][0]))
    blocks = []  # each: {bbox, items}
    for tl in text_lines_sorted:
        bb = tl["bbox_pt"]
        placed = False
        for blk in blocks:
            bbb = blk["bbox"]
            # thresholds
            vert_gap = bb[1] - bbb[3]  # distance from block bottom to line top
            h_overlap = _rect_overlap_h(bb, bbb)
            same_column = abs(bb[0] - bbb[0]) <= 12.0  # left alignment tolerance
            if vert_gap <= 10.0 and (h_overlap >= 0.2 or same_column):
                blk["bbox"] = _rect_union(bbb, bb)
                blk["items"].append(tl)
                placed = True
                break
        if not placed:
            blocks.append({"bbox": bb[:], "items": [tl]})

    text_boxes = []
    for blk in blocks:
        bb = [round(v, 2) for v in blk["bbox"]]
        text_boxes.append({
            "type": "text_block",
            "bbox_pt": bb,
            "bbox_mm": bbox_pt_to_mm(bb, ctx.get("user_unit", 1.0)),
            "children_count": len(blk["items"]) 
        })

    # Image boxes: merge overlapping/nearby images
    img_boxes_raw = []
    for im in images:
        img_boxes_raw.append({"bbox": im["bbox_pt"][:], "item": im})
    merged = []
    for box in sorted(img_boxes_raw, key=lambda b: (b["bbox"][1], b["bbox"][0])):
        merged_flag = False
        for m in merged:
            # merge if overlap significantly
            if _rect_overlap_h(box["bbox"], m["bbox"]) > 0.3 and not (box["bbox"][3] < m["bbox"][1] or box["bbox"][1] > m["bbox"][3]):
                m["bbox"] = _rect_union(m["bbox"], box["bbox"])
                m["count"] += 1
                merged_flag = True
                break
        if not merged_flag:
            merged.append({"bbox": box["bbox"], "count": 1})

    image_boxes = []
    for m in merged:
        bb = [round(v, 2) for v in m["bbox"]]
        image_boxes.append({
            "type": "image_block",
            "bbox_pt": bb,
            "bbox_mm": bbox_pt_to_mm(bb, ctx.get("user_unit", 1.0)),
            "children_count": m["count"]
        })

    # Combine and sort by y,x
    boxes = text_boxes + image_boxes
    boxes.sort(key=lambda b: (b["bbox_pt"][1], b["bbox_pt"][0]))
    return boxes


# ==== Service Endpoints ====

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "pdf-measure-service", "version": "1.0"})


@app.route("/measure/from-path", methods=["POST"])
def measure_from_path():
    try:
        data = request.get_json(silent=True) or {}
        pdf_path = data.get("filepath")
        per_page = bool(data.get("per_page", False))
        max_pages = data.get("max_pages")
        max_pages = int(max_pages) if max_pages is not None else None
        save_outputs = bool(data.get("save_outputs", True))
        make_overlay = bool(data.get("make_overlay", False))
        overlay_stroke_pt = float(data.get("overlay_stroke_pt", 1.0))
        include_files = bool(data.get("include_files", False))
        include_files_content = bool(data.get("include_files_content", False))
        content_max_bytes = int(data.get("content_max_bytes", 200000))

        if not pdf_path or not os.path.exists(pdf_path):
            return jsonify({"success": False, "error": "File not found or no filepath provided"}), 400
        if not pdf_path.lower().endswith(".pdf"):
            return jsonify({"success": False, "error": "File must be a PDF"}), 400

        out_dir = os.getenv("MEASURE_OUT_DIR", "/shared/measurements") if save_outputs else None
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        result = measure_pdf(pdf_path, out_dir=out_dir, per_page=per_page, max_pages=max_pages,
                             layout_only_outputs=bool(data.get("layout_only_outputs", False)))

        overlay_url = None
        overlay_path = None
        if make_overlay:
            # generate overlay into out_dir (or default if out_dir is None)
            overlay_dir = out_dir or os.getenv("MEASURE_OUT_DIR", "/shared/measurements")
            os.makedirs(overlay_dir, exist_ok=True)
            base = os.path.splitext(os.path.basename(pdf_path))[0]
            overlay_path = os.path.join(overlay_dir, f"{base}_overlay.pdf")
            create_overlay_pdf(pdf_path, result.get("items", []), overlay_path, stroke_pt=overlay_stroke_pt)
            url_path = f"/files/{os.path.basename(overlay_path)}"
            base_url = request.host_url[:-1] if request.host_url.endswith('/') else request.host_url
            overlay_url = f"{base_url}{url_path}"

        # Optional layout-only reduction (filter items to layout_block types)
        items_out = result["items"]
        if bool(data.get("layout_only", False)):
            items_out = [it for it in items_out if it.get("type") in ("text_block","image_block")]

        # Collect output files if requested
        output_files = []
        if out_dir and (save_outputs or bool(data.get("layout_only_outputs", False)) or make_overlay) and include_files:
            try:
                base_name = os.path.basename(pdf_path)
                base_root = os.path.join(out_dir, base_name)
                # Gather matching files in out_dir
                for fname in os.listdir(out_dir):
                    if not fname.startswith(base_name):
                        continue
                    fpath = os.path.join(out_dir, fname)
                    if not os.path.isfile(fpath):
                        continue
                    url_path = f"/files/{fname}"
                    base_url = request.host_url[:-1] if request.host_url.endswith('/') else request.host_url
                    entry = {
                        "name": fname,
                        "path": fpath,
                        "url": f"{base_url}{url_path}",
                        "size_bytes": os.path.getsize(fpath)
                    }
                    if include_files_content and entry["size_bytes"] <= content_max_bytes:
                        try:
                            with open(fpath, "rb") as fh:
                                entry["content"] = fh.read().decode("utf-8", errors="replace")
                        except Exception:
                            pass
                    output_files.append(entry)
            except Exception as e:
                logger.warning(f"Failed to collect output files: {e}")

        return jsonify({
            "success": True,
            "filepath": pdf_path,
            "total_items": result["total_items"],
            "items": items_out,
            "layout_only": bool(data.get("layout_only", False)),
            "outputs_saved": bool(out_dir),
            "output_dir": out_dir,
            "overlay_path": overlay_path,
            "overlay_url": overlay_url,
            "outputs": output_files
        })
    except Exception as e:
        logger.exception("Error in measure_from_path")
        return jsonify({"success": False, "error": str(e)}), 500


def create_overlay_pdf(pdf_path: str, items: List[Dict[str, Any]], out_path: str,
                       stroke_pt: float = 1.0) -> None:
    import fitz
    colors = {
        "image": (1, 0, 0),           # red
        "rectangle": (0, 1, 0),       # green
        "vector_path": (0, 0, 1),     # blue
        "text_line": (1, 0.5, 0),     # orange
        "text_glyph": (1, 0, 1),      # magenta
        "form_xobject_expanded": (0, 0, 0) # black
    }
    doc = fitz.open(pdf_path)
    try:
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            # items use page_number (1-based)
            page_items = [it for it in items if it.get("page_number") == page_idx + 1]
            if not page_items:
                continue
            for it in page_items:
                bbox = it.get("bbox_pt") or it.get("bbox")
                if not bbox or len(bbox) != 4:
                    continue
                x0, y0, x1, y1 = [float(v) for v in bbox]
                rect = fitz.Rect(x0, y0, x1, y1)
                c = colors.get(it.get("type", ""), (0, 0, 0))
                shape = page.new_shape()
                shape.draw_rect(rect)
                shape.finish(color=c, width=stroke_pt)
                shape.commit()
                # draw visible clip bbox if present
                vb = it.get("visible_bbox_pt")
                if vb and isinstance(vb, (list, tuple)) and len(vb) == 4:
                    vrect = fitz.Rect(*[float(v) for v in vb])
                    vshape = page.new_shape()
                    vshape.draw_rect(vrect)
                    # dashed outline
                    vshape.finish(color=(0, 0, 0), dashes="2 2", width=max(0.7, stroke_pt * 0.8))
                    vshape.commit()
        # save overlay
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        doc.save(out_path)
    finally:
        doc.close()


@app.route("/measure/overlay-from-path", methods=["POST"])
def overlay_from_path():
    try:
        data = request.get_json(silent=True) or {}
        pdf_path = data.get("filepath")
        max_pages = data.get("max_pages")
        max_pages = int(max_pages) if max_pages is not None else None
        stroke_pt = float(data.get("stroke_pt", 1.0))
        per_page = bool(data.get("per_page", False))
        save_outputs = bool(data.get("save_outputs", False))

        if not pdf_path or not os.path.exists(pdf_path):
            return jsonify({"success": False, "error": "File not found or no filepath provided"}), 400
        if not pdf_path.lower().endswith(".pdf"):
            return jsonify({"success": False, "error": "File must be a PDF"}), 400

        # measure (optionally also write CSV/JSONL)
        out_dir = os.getenv("MEASURE_OUT_DIR", "/shared/measurements") if save_outputs else None
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        result = measure_pdf(pdf_path, out_dir=out_dir, per_page=per_page, max_pages=max_pages)
        items = result.get("items", [])

        # overlay always written (uses default dir if save_outputs false)
        overlay_dir = out_dir or os.getenv("MEASURE_OUT_DIR", "/shared/measurements")
        os.makedirs(overlay_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(pdf_path))[0]
        out_path = os.path.join(overlay_dir, f"{base}_overlay.pdf")
        create_overlay_pdf(pdf_path, items, out_path, stroke_pt=stroke_pt)

        # build URL
        url_path = f"/files/{os.path.basename(out_path)}"
        base_url = request.host_url[:-1] if request.host_url.endswith('/') else request.host_url
        return jsonify({
            "success": True,
            "filepath": pdf_path,
            "overlay_path": out_path,
            "overlay_url": f"{base_url}{url_path}",
            "total_items": result.get("total_items", 0),
            "outputs_saved": bool(out_dir),
            "output_dir": out_dir
        })
    except Exception as e:
        logger.exception("Error in overlay_from_path")
        return jsonify({"success": False, "error": str(e)}), 500


# ==== Render LLM Layout Report onto PDF ====

def render_layout_report(pdf_path: str, report: Dict[str, Any], out_path: str,
                         box_stroke: float = 1.0, issue_font_size: float = 8.0) -> None:
    import fitz
    # Colors - make them more visible
    col_box = (0, 0.8, 0)          # brighter green for boxes
    col_issue_err = (1, 0, 0)      # red for error
    col_issue_warn = (1, 0.6, 0)   # brighter orange for warn
    col_issue_info = (0, 0.6, 1)   # brighter blue for info

    def color_for_severity(sev: str):
        s = (sev or '').lower()
        if s == 'error':
            return col_issue_err
        if s == 'warn' or s == 'warning':
            return col_issue_warn
        return col_issue_info

    logger.info(f"Starting render_layout_report for {pdf_path}")
    logger.info(f"Report structure: {list(report.keys()) if isinstance(report, dict) else 'Not a dict'}")
    
    doc = fitz.open(pdf_path)
    try:
        pages = report.get('pages', []) if isinstance(report, dict) else []
        logger.info(f"Found {len(pages)} pages in report")
        
        for page_obj in pages:
            pno = int(page_obj.get('page_number', 1)) - 1
            if pno < 0 or pno >= len(doc):
                logger.warning(f"Page number {pno + 1} out of range (0-{len(doc)-1})")
                continue
                
            page = doc[pno]
            logger.info(f"Processing page {pno + 1}")
            
            # Draw boxes with thicker lines and better visibility
            boxes = page_obj.get('boxes', []) or []
            logger.info(f"Drawing {len(boxes)} boxes on page {pno + 1}")
            for b in boxes:
                bb = b.get('bbox_pt')
                if not (isinstance(bb, (list, tuple)) and len(bb) == 4):
                    logger.warning(f"Invalid bbox_pt for box: {b}")
                    continue
                rect = fitz.Rect(float(bb[0]), float(bb[1]), float(bb[2]), float(bb[3]))
                shp = page.new_shape()
                shp.draw_rect(rect)
                # Use thicker lines for better visibility
                shp.finish(color=col_box, width=max(3.0, box_stroke * 2))
                shp.commit()
                logger.info(f"Drew box at {bb} with color {col_box}")
                
            # Draw issues with thicker lines and better visibility
            issues = page_obj.get('issues', []) or []
            logger.info(f"Drawing {len(issues)} issues on page {pno + 1}")
            for iss in issues:
                sev = iss.get('severity', 'info')
                c = color_for_severity(sev)
                between = iss.get('between') or []
                
                # Draw both boxes involved, if present
                for bt in between:
                    bb = bt.get('bbox_pt')
                    if not (isinstance(bb, (list, tuple)) and len(bb) == 4):
                        logger.warning(f"Invalid bbox_pt for issue box: {bt}")
                        continue
                    rect = fitz.Rect(float(bb[0]), float(bb[1]), float(bb[2]), float(bb[3]))
                    shp = page.new_shape()
                    shp.draw_rect(rect)
                    # Use thicker lines for issues
                    shp.finish(color=c, width=max(4.0, box_stroke * 3))
                    shp.commit()
                    logger.info(f"Drew issue box at {bb} with color {c} and severity {sev}")
                    
                # Place small label near first box top-left
                label = iss.get('type', 'issue')
                desc = iss.get('description')
                text = label if not desc else f"{label}: {desc}"
                if between and isinstance(between[0].get('bbox_pt'), (list, tuple)):
                    x0, y0, *_ = between[0]['bbox_pt']
                    try:
                        page.insert_text(fitz.Point(float(x0), float(y0) - 4),
                                         text[:140], color=c, fontsize=max(10, issue_font_size))
                        logger.info(f"Added text label '{text[:50]}...' at ({x0}, {y0})")
                    except Exception as e:
                        logger.warning(f"Failed to insert text for issue: {e}")
                        
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        doc.save(out_path)
        logger.info(f"Successfully saved rendered report to {out_path}")
    finally:
        doc.close()


@app.route('/measure/render-report', methods=['POST'])
def render_report_endpoint():
    try:
        data = request.get_json(silent=True) or {}
        pdf_path = data.get('filepath')
        report = data.get('report')  # can be dict or JSON string
        box_stroke = float(data.get('box_stroke', 1.0))
        issue_font_size = float(data.get('issue_font_size', 8.0))

        if not pdf_path or not os.path.exists(pdf_path):
            return jsonify({"success": False, "error": "File not found or no filepath provided"}), 400
        if not pdf_path.lower().endswith('.pdf'):
            return jsonify({"success": False, "error": "File must be a PDF"}), 400
        if isinstance(report, str):
            try:
                report = json.loads(report)
            except Exception:
                return jsonify({"success": False, "error": "report is not valid JSON"}), 400
        if not isinstance(report, dict):
            return jsonify({"success": False, "error": "report must be a JSON object"}), 400

        # Handle nested report structure (when report contains another report field)
        if 'report' in report and isinstance(report['report'], dict):
            actual_report = report['report']
            logger.info(f"Extracted nested report structure with {len(actual_report.get('pages', []))} pages")
        else:
            actual_report = report

        out_dir = os.getenv('MEASURE_OUT_DIR', '/shared/measurements')
        os.makedirs(out_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(pdf_path))[0]
        out_path = os.path.join(out_dir, f"{base}_layout_report.pdf")

        render_layout_report(pdf_path, actual_report, out_path, box_stroke=box_stroke, issue_font_size=issue_font_size)

        url_path = f"/files/{os.path.basename(out_path)}"
        base_url = request.host_url[:-1] if request.host_url.endswith('/') else request.host_url
        return jsonify({
            "success": True,
            "filepath": pdf_path,
            "report_overlay_path": out_path,
            "report_overlay_url": f"{base_url}{url_path}"
        })
    except Exception as e:
        logger.exception('Error in render_report_endpoint')
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/files/<path:filename>', methods=['GET'])
def serve_saved_file(filename):
    directory = os.getenv("MEASURE_OUT_DIR", "/shared/measurements")
    return send_from_directory(directory, filename)


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    app.run(host=host, port=port)


