import os
import io
import math
import json
import logging
from typing import List, Dict, Tuple, Optional

from flask import Flask, request, jsonify

# Heavy libs imported lazily inside functions to keep import-time fast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    r = max(0, min(255, int(round(r))))
    g = max(0, min(255, int(round(g))))
    b = max(0, min(255, int(round(b))))
    return f"#{r:02x}{g:02x}{b:02x}"


def rgb_to_cmyk(rgb: Tuple[int, int, int]) -> Tuple[float, float, float, float]:
    r, g, b = [x / 255.0 for x in rgb]
    k = 1 - max(r, g, b)
    if k >= 1.0 - 1e-9:
        return 0.0, 0.0, 0.0, 100.0
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return round(c * 100, 1), round(m * 100, 1), round(y * 100, 1), round(k * 100, 1)


def detect_color_spaces_and_spots(pdf_path: str) -> Dict:
    """Detect declared color spaces and Separation/spot color names using pikepdf.
    Returns a dict with discovered color space hints and any spot color names (potential PMS).
    """
    try:
        import pikepdf
        color_spaces = set()
        spot_colors = set()

        with pikepdf.open(pdf_path) as pdf:
            for page in pdf.pages:
                resources = page.get("/Resources")
                if resources is None:
                    continue
                cs = resources.get("/ColorSpace")
                if cs is not None:
                    # cs may be a dictionary mapping names to colorspace objects
                    if isinstance(cs, pikepdf.Dictionary):
                        for _, cs_obj in cs.items():
                            try:
                                if isinstance(cs_obj, pikepdf.Array) and len(cs_obj) > 0:
                                    cs_name = str(cs_obj[0])
                                    if "DeviceRGB" in cs_name:
                                        color_spaces.add("RGB")
                                    elif "DeviceCMYK" in cs_name:
                                        color_spaces.add("CMYK")
                                    elif "DeviceGray" in cs_name:
                                        color_spaces.add("Gray")
                                    elif "ICCBased" in cs_name:
                                        color_spaces.add("ICCBased")
                                    elif "Separation" in cs_name:
                                        color_spaces.add("Separation")
                                        # Spot color name is usually the second element in the array
                                        if len(cs_obj) >= 2:
                                            name_obj = cs_obj[1]
                                            try:
                                                spot_name = str(name_obj)
                                                if spot_name.startswith("/"):
                                                    spot_name = spot_name[1:]
                                                spot_colors.add(spot_name)
                                            except Exception:
                                                pass
                            except Exception:
                                continue

        return {
            "declared_color_spaces": sorted(list(color_spaces)),
            "spot_colors": sorted(list(spot_colors))
        }
    except Exception as e:
        logger.warning(f"Color space detection failed: {e}")
        return {"declared_color_spaces": [], "spot_colors": []}


def render_pdf_pages_to_images(pdf_path: str, zoom: float = 2.0) -> List["Image.Image"]:
    """Render each page to a PIL Image at given zoom factor."""
    import fitz  # PyMuPDF
    from PIL import Image

    images: List[Image.Image] = []
    doc = fitz.open(pdf_path)
    try:
        for page_index in range(len(doc)):
            page = doc[page_index]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")
            pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            images.append(pil_img)
    finally:
        doc.close()
    return images


def kmeans_colors_from_image(img, max_colors: int = 12, white_threshold: int = 245) -> List[Dict]:
    """Extract dominant colors via KMeans. Filters out near-white pixels to reduce noise."""
    import numpy as np
    from sklearn.cluster import KMeans

    arr = np.array(img)
    h, w, _ = arr.shape
    pixels = arr.reshape(-1, 3)

    # Filter out near-white pixels (optional but helps with realistic percentages)
    mask = ~((pixels[:, 0] >= white_threshold) & (pixels[:, 1] >= white_threshold) & (pixels[:, 2] >= white_threshold))
    colored = pixels[mask]
    if colored.size == 0:
        return []

    # Heuristic for number of clusters
    n_clusters = min(max_colors, max(2, int(round(math.sqrt(colored.shape[0] / 15000))) * 3))

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(colored)
    centers = km.cluster_centers_

    counts = {}
    for lbl in labels:
        counts[lbl] = counts.get(lbl, 0) + 1

    results = []
    total_colored = colored.shape[0]
    for idx, center in enumerate(centers):
        r, g, b = [int(round(x)) for x in center]
        cnt = counts.get(idx, 0)
        results.append({
            "rgb": [r, g, b],
            "hex": rgb_to_hex(r, g, b),
            "count": int(cnt),
            "percentage_colored": float(cnt / total_colored * 100.0),
            "pixels_total": h * w,
            "colored_pixels_total": int(total_colored)
        })

    # Sort by count desc
    results.sort(key=lambda x: x["count"], reverse=True)
    return results


def aggregate_colors_across_pages(page_color_lists: List[List[Dict]]) -> List[Dict]:
    """Aggregate clusters across pages by hex matching, sum counts and recompute percentages."""
    from collections import defaultdict

    aggregate = {}
    total_colored_pixels = 0

    for color_list in page_color_lists:
        for c in color_list:
            total_colored_pixels += c.get("count", 0)
            key = c["hex"].lower()
            if key not in aggregate:
                aggregate[key] = {
                    "hex": c["hex"],
                    "rgb": c["rgb"],
                    "count": 0
                }
            aggregate[key]["count"] += c.get("count", 0)

    # Convert to list and compute percentages
    result = []
    for key, val in aggregate.items():
        rgb = val["rgb"]
        cmyk = list(rgb_to_cmyk(tuple(rgb)))
        appearance = (val["count"] / total_colored_pixels * 100.0) if total_colored_pixels > 0 else 0.0
        result.append({
            "hex": val["hex"],
            "rgb": rgb,
            "cmyk": cmyk,
            "pms": None,  # filled if we detect spot names below
            "appearance_percent": round(appearance, 1)
        })

    result.sort(key=lambda x: x["appearance_percent"], reverse=True)
    return result


def map_spot_names_to_colors(spots: List[str]) -> Dict[str, str]:
    """Heuristic mapping: return a dict of spot name to PMS code string if recognizable.
    If names include PMS/Pantone, return them directly; otherwise return empty mapping.
    """
    mapping = {}
    for name in spots:
        normalized = name.strip()
        if not normalized:
            continue
        if normalized.lower().startswith("pms") or normalized.lower().startswith("pantone"):
            mapping[normalized] = normalized
        else:
            mapping[normalized] = normalized  # keep as-found; may still be meaningful
    return mapping


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "color-profile-service", "version": "1.0"})


@app.route("/colors/from-path", methods=["POST"])
def colors_from_path():
    try:
        data = request.get_json(silent=True) or {}
        pdf_path = data.get("filepath")
        max_colors = int(data.get("max_colors", 12))
        zoom = float(data.get("zoom", 2.0))

        if not pdf_path or not os.path.exists(pdf_path):
            return jsonify({"success": False, "error": "File not found or no filepath provided"}), 400
        if not pdf_path.lower().endswith(".pdf"):
            return jsonify({"success": False, "error": "File must be a PDF"}), 400

        # Detect color spaces and spot/PMS names (if any)
        cs_info = detect_color_spaces_and_spots(pdf_path)
        declared_spaces = cs_info.get("declared_color_spaces", [])
        spot_names = cs_info.get("spot_colors", [])

        # Render pages and extract colors via KMeans
        images = render_pdf_pages_to_images(pdf_path, zoom=zoom)
        page_colors: List[List[Dict]] = []
        for img in images:
            page_colors.append(kmeans_colors_from_image(img, max_colors=max_colors))

        aggregated = aggregate_colors_across_pages(page_colors)

        # Attempt to attach PMS if there are recognizable spot names
        spot_map = map_spot_names_to_colors(spot_names)
        if spot_map:
            # Simple rule: if exactly one spot/PMS is declared, annotate each color with that PMS name
            if len(spot_map) == 1:
                pms_name = list(spot_map.values())[0]
                for c in aggregated:
                    c["pms"] = pms_name

        response = {
            "success": True,
            "filepath": pdf_path,
            "declared_color_spaces": declared_spaces,
            "detected_spot_colors": spot_names,
            "colors": aggregated,
            "total_colors": len(aggregated)
        }

        return jsonify(response)

    except Exception as e:
        logger.exception("Error extracting colors")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    app.run(host=host, port=port)


