import os
import io
import json
import logging
from typing import Dict, List, Tuple

from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def normalize_font_name(full_font_name: str) -> Tuple[str, str, str]:
    """Normalize a PDF font name to (family, style, full_name_clean).
    - Remove subset prefixes like 'ABCDEE+'.
    - Split family/style by hyphen, infer style keywords (Bold, Italic, Oblique, Regular).
    """
    name = full_font_name or ""
    # Remove subset prefix (ABCDEE+FontName)
    if "+" in name:
        parts = name.split("+", 1)
        if len(parts[-1]) > 0:
            name = parts[-1]
    family = name
    style = "Regular"
    if "-" in name:
        family, style_part = name.split("-", 1)
        style = style_part
    # Normalize common styles
    s_lower = style.lower()
    if "bold" in s_lower and ("italic" in s_lower or "oblique" in s_lower):
        style_norm = "BoldItalic"
    elif "bold" in s_lower:
        style_norm = "Bold"
    elif "italic" in s_lower or "oblique" in s_lower:
        style_norm = "Italic"
    else:
        style_norm = "Regular"
    return family, style_norm, name


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "font-profile-service", "version": "1.0"})


def _float_close(a: float, b: float, tol: float = 0.15) -> bool:
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False


def _round_to_step(value: float, step: float) -> float:
    try:
        return round(round(float(value) / float(step)) * float(step), 2)
    except Exception:
        return round(float(value), 2)


@app.route("/fonts/sections-from-path", methods=["POST"])
def font_sections_from_path():
    """Return sequential sections of text where font properties stay constant.
    New section starts when any of (family, style, size, line_height ratio) changes beyond tolerance.
    """
    try:
        data = request.get_json(silent=True) or {}
        pdf_path = data.get("filepath")
        size_tolerance = float(data.get("size_tolerance", 0.15))
        lh_tolerance = float(data.get("line_height_tolerance", 0.3))
        normalize = bool(data.get("normalize", True))
        norm_step_pt = float(data.get("normalize_step_pt", 0.5))
        norm_ratio_step = float(data.get("normalize_ratio_step", 0.05))

        if not pdf_path or not os.path.exists(pdf_path):
            return jsonify({"success": False, "error": "File not found or no filepath provided"}), 400
        if not pdf_path.lower().endswith(".pdf"):
            return jsonify({"success": False, "error": "File must be a PDF"}), 400

        import fitz  # PyMuPDF

        doc = fitz.open(pdf_path)

        sections: List[Dict] = []
        current = None
        section_index = 0

        for page_index in range(len(doc)):
            page = doc[page_index]
            text = page.get_text("dict")
            for block in text.get("blocks", []):
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    line_bbox = line.get("bbox", [0, 0, 0, 0])
                    # Derive line height from bbox
                    try:
                        line_height = float(line_bbox[3] - line_bbox[1])
                    except Exception:
                        line_height = 0.0
                    for span in line.get("spans", []):
                        full_font = span.get("font", "")
                        size = float(span.get("size", 0.0))
                        text_content = span.get("text", "")
                        if not text_content:
                            continue
                        family, style, full_clean = normalize_font_name(full_font)
                        ratio = (line_height / size) if size > 0 else 0.0

                        props = {
                            "page": page_index + 1,
                            "font_family": family,
                            "style": style,
                            "font_size": round(size, 2),
                            "line_height": round(line_height, 2),
                            "line_height_ratio": round(ratio, 2)
                        }

                        if normalize:
                            props["font_size_normalized"] = _round_to_step(size, norm_step_pt)
                            props["line_height_normalized"] = _round_to_step(line_height, norm_step_pt)
                            props["line_height_ratio_normalized"] = _round_to_step(ratio, norm_ratio_step)

                        def same_props(a: Dict, b: Dict) -> bool:
                            return (
                                a.get("page") == b.get("page") and
                                a.get("font_family") == b.get("font_family") and
                                a.get("style") == b.get("style") and
                                _float_close(a.get("font_size", 0.0), b.get("font_size", 0.0), size_tolerance) and
                                _float_close(a.get("line_height", 0.0), b.get("line_height", 0.0), lh_tolerance)
                            )

                        # Start new section if needed
                        if current is None or not same_props(current["properties"], props):
                            if current is not None:
                                # finalize bbox union to list
                                current["bbox"] = [
                                    round(current["_bbox_min_x"], 2),
                                    round(current["_bbox_min_y"], 2),
                                    round(current["_bbox_max_x"], 2),
                                    round(current["_bbox_max_y"], 2)
                                ]
                                del current["_bbox_min_x"]; del current["_bbox_min_y"]; del current["_bbox_max_x"]; del current["_bbox_max_y"]
                                sections.append(current)

                            section_index += 1
                            current = {
                                "section_index": section_index,
                                "properties": props,
                                "text": "",
                                "lines": [],
                                "bbox": [0, 0, 0, 0],
                                "_bbox_min_x": float("inf"),
                                "_bbox_min_y": float("inf"),
                                "_bbox_max_x": float("-inf"),
                                "_bbox_max_y": float("-inf")
                            }

                        # Append span text and update line/bbox
                        # Update bbox union using span bbox
                        sb = span.get("bbox", line_bbox)
                        try:
                            x0, y0, x1, y1 = [float(v) for v in sb]
                            current["_bbox_min_x"] = min(current["_bbox_min_x"], x0)
                            current["_bbox_min_y"] = min(current["_bbox_min_y"], y0)
                            current["_bbox_max_x"] = max(current["_bbox_max_x"], x1)
                            current["_bbox_max_y"] = max(current["_bbox_max_y"], y1)
                        except Exception:
                            pass

                        # Add/merge line record
                        line_rec = {
                            "page": page_index + 1,
                            "bbox": [round(line_bbox[0], 2), round(line_bbox[1], 2), round(line_bbox[2], 2), round(line_bbox[3], 2)],
                            "font_size": round(size, 2),
                            "line_height": round(line_height, 2),
                            "line_height_ratio": round(ratio, 2),
                            "text": text_content
                        }

                        if normalize:
                            line_rec["font_size_normalized"] = _round_to_step(size, norm_step_pt)
                            line_rec["line_height_normalized"] = _round_to_step(line_height, norm_step_pt)
                            line_rec["line_height_ratio_normalized"] = _round_to_step(ratio, norm_ratio_step)

                        # If last line in this section has same bbox, append text; else push new
                        if current["lines"] and current["lines"][-1]["bbox"] == line_rec["bbox"]:
                            current["lines"][-1]["text"] += text_content
                        else:
                            current["lines"].append(line_rec)

                        # Append to section text with newline at line breaks
                        if current["text"] and current["lines"] and current["lines"][-1]["text"] == text_content:
                            # already appended as new line; ensure newline before new line text
                            current["text"] += "\n" + text_content
                        else:
                            # If same line, just concatenate
                            if current["text"] and not current["text"].endswith("\n"):
                                current["text"] += text_content
                            else:
                                current["text"] += text_content

        # finalize last section
        if current is not None:
            current["bbox"] = [
                round(current["_bbox_min_x"], 2),
                round(current["_bbox_min_y"], 2),
                round(current["_bbox_max_x"], 2),
                round(current["_bbox_max_y"], 2)
            ]
            del current["_bbox_min_x"]; del current["_bbox_min_y"]; del current["_bbox_max_x"]; del current["_bbox_max_y"]
            sections.append(current)

        doc.close()

        return jsonify({
            "success": True,
            "filepath": pdf_path,
            "sections": sections,
            "total_sections": len(sections)
        })

    except Exception as e:
        logger.exception("Error extracting font sections")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/fonts/from-path", methods=["POST"])
def fonts_from_path():
    try:
        data = request.get_json(silent=True) or {}
        pdf_path = data.get("filepath")
        zoom = float(data.get("zoom", 1.0))  # not used here; text extraction is vector-based

        if not pdf_path or not os.path.exists(pdf_path):
            return jsonify({"success": False, "error": "File not found or no filepath provided"}), 400
        if not pdf_path.lower().endswith(".pdf"):
            return jsonify({"success": False, "error": "File must be a PDF"}), 400

        import fitz  # PyMuPDF

        doc = fitz.open(pdf_path)

        font_stats: Dict[Tuple[str, str], Dict] = {}
        total_chars = 0

        for page_index in range(len(doc)):
            page = doc[page_index]
            text = page.get_text("dict")
            for block in text.get("blocks", []):
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    # line bbox: [x0,y0,x1,y1]
                    try:
                        line_bbox = line.get("bbox", [0, 0, 0, 0])
                        line_height = max(0.0, float(line_bbox[3] - line_bbox[1]))
                    except Exception:
                        line_height = 0.0
                    for span in line.get("spans", []):
                        full_font = span.get("font", "")
                        size = float(span.get("size", 0.0))
                        text_content = span.get("text", "")
                        char_count = len(text_content)
                        if char_count == 0:
                            continue
                        family, style, full_clean = normalize_font_name(full_font)
                        key = (family.lower(), style.lower())
                        if key not in font_stats:
                            font_stats[key] = {
                                "font_family": family,
                                "style": style,
                                "full_names": set([full_clean]),
                                "size_sum": 0.0,
                                "size_count": 0,
                                "size_min": None,
                                "size_max": None,
                                "lh_sum": 0.0,
                                "lh_count": 0,
                                "lh_min": None,
                                "lh_max": None,
                                "ratio_sum": 0.0,
                                "ratio_count": 0,
                                "pages": set(),
                                "usage_chars": 0,
                            }
                        s = font_stats[key]
                        s["full_names"].add(full_clean)
                        s["size_sum"] += size
                        s["size_count"] += 1
                        s["size_min"] = size if s["size_min"] is None else min(s["size_min"], size)
                        s["size_max"] = size if s["size_max"] is None else max(s["size_max"], size)
                        if line_height > 0:
                            s["lh_sum"] += line_height
                            s["lh_count"] += 1
                            if s["lh_min"] is None:
                                s["lh_min"] = line_height
                            else:
                                s["lh_min"] = min(s["lh_min"], line_height)
                            if s["lh_max"] is None:
                                s["lh_max"] = line_height
                            else:
                                s["lh_max"] = max(s["lh_max"], line_height)
                            if size > 0:
                                s["ratio_sum"] += (line_height / size)
                                s["ratio_count"] += 1
                        s["pages"].add(page_index + 1)
                        s["usage_chars"] += char_count
                        total_chars += char_count

        doc.close()

        # Build output list
        fonts: List[Dict] = []
        for key, s in font_stats.items():
            size_avg = (s["size_sum"] / s["size_count"]) if s["size_count"] > 0 else 0.0
            lh_avg = (s["lh_sum"] / s["lh_count"]) if s["lh_count"] > 0 else 0.0
            ratio_avg = (s["ratio_sum"] / s["ratio_count"]) if s["ratio_count"] > 0 else 0.0
            usage_pct = (s["usage_chars"] / total_chars * 100.0) if total_chars > 0 else 0.0
            fonts.append({
                "font_family": s["font_family"],
                "style": s["style"],
                "full_names": sorted(list(s["full_names"])),
                "size_min": round(s["size_min"], 2) if s["size_min"] is not None else 0.0,
                "size_max": round(s["size_max"], 2) if s["size_max"] is not None else 0.0,
                "size_avg": round(size_avg, 2),
                "line_height_min": round(s["lh_min"], 2) if s["lh_min"] is not None else 0.0,
                "line_height_max": round(s["lh_max"], 2) if s["lh_max"] is not None else 0.0,
                "line_height_avg": round(lh_avg, 2),
                "line_height_ratio_avg": round(ratio_avg, 2),
                "usage_count": s["usage_chars"],
                "usage_percentage": round(usage_pct, 1),
                "pages": sorted(list(s["pages"]))
            })

        fonts.sort(key=lambda f: f["usage_percentage"], reverse=True)

        return jsonify({
            "success": True,
            "filepath": pdf_path,
            "fonts": fonts,
            "total_fonts": len(fonts),
            "total_characters": total_chars
        })

    except Exception as e:
        logger.exception("Error extracting fonts")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    app.run(host=host, port=port)


