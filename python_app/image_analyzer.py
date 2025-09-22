import os
import re
import json
import logging
import numpy as np
from collections import defaultdict, Counter
import tempfile
import shutil
import cv2
from PIL import Image, ImageDraw, ImageFont
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_images_from_pdf_comprehensive(pdf_path):
    """Comprehensive image and graphic extraction from PDF using multiple methods"""
    
    # Import libraries here to avoid import issues
    import fitz  # PyMuPDF
    import pdfplumber
    
    image_data = {
        "pages": [],
        "overall_stats": {},
        "image_types": {},
        "logo_analysis": {},
        "quality_analysis": {},
        "placement_analysis": {},
        "branding_elements": {}
    }
    
    try:
        # Method 1: PyMuPDF for image extraction
        logger.info("Starting PyMuPDF image analysis...")
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_rect = page.rect
            
            page_images = {
                "page_number": page_num + 1,
                "images": [],
                "graphics": [],
                "logos": [],
                "image_stats": {}
            }
            
            # Get image list from page
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                try:
                    # Get image information
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    # Get image metadata
                    img_info = {
                        "index": img_index,
                        "xref": xref,
                        "width": pix.width,
                        "height": pix.height,
                        "colorspace": pix.colorspace.name if pix.colorspace else "unknown",
                        "size_bytes": len(pix.tobytes()),
                        "format": pix.colorspace.name if pix.colorspace else "unknown"
                    }
                    
                    # Get image position on page
                    img_rect = page.get_image_bbox(img)
                    if img_rect:
                        img_info.update({
                            "x": img_rect.x0,
                            "y": img_rect.y0,
                            "width_px": img_rect.width,
                            "height_px": img_rect.height,
                            "center_x": (img_rect.x0 + img_rect.x1) / 2,
                            "center_y": (img_rect.y0 + img_rect.y1) / 2,
                            "area": img_rect.width * img_rect.height,
                            "aspect_ratio": img_rect.width / img_rect.height if img_rect.height > 0 else 0
                        })
                    
                    # Analyze image content
                    img_analysis = analyze_image_content(pix)
                    img_info.update(img_analysis)
                    
                    # Categorize image type
                    img_type = categorize_image_type(img_info)
                    img_info["type"] = img_type
                    
                    page_images["images"].append(img_info)
                    
                    # Check if it might be a logo
                    if is_potential_logo(img_info):
                        page_images["logos"].append(img_info)
                    
                    pix = None  # Free memory
                    
                except Exception as e:
                    logger.warning(f"Error processing image {img_index} on page {page_num + 1}: {e}")
                    continue
            
            # Method 2: Extract graphics and shapes
            graphics = extract_graphics_from_page(page)
            page_images["graphics"] = graphics
            
            # Calculate page image statistics
            page_images["image_stats"] = calculate_page_image_stats(page_images)
            
            image_data["pages"].append(page_images)
        
        doc.close()
        
        # Method 3: pdfplumber for additional image analysis
        logger.info("Starting pdfplumber image analysis...")
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_images = image_data["pages"][page_num]
                
                # Extract images using pdfplumber
                if hasattr(page, 'images'):
                    for img in page.images:
                        img_info = {
                            "source": "pdfplumber",
                            "x": img["x0"],
                            "y": img["y0"],
                            "width": img["width"],
                            "height": img["height"],
                            "page": page_num + 1
                        }
                        
                        # Analyze image properties
                        img_analysis = analyze_pdfplumber_image(img)
                        img_info.update(img_analysis)
                        
                        page_images["images"].append(img_info)
        
        # Analyze overall patterns
        image_data["overall_stats"] = analyze_overall_image_stats(image_data["pages"])
        image_data["image_types"] = analyze_image_types(image_data["pages"])
        image_data["logo_analysis"] = analyze_logos(image_data["pages"])
        image_data["quality_analysis"] = analyze_image_quality(image_data["pages"])
        image_data["placement_analysis"] = analyze_image_placement(image_data["pages"])
        image_data["branding_elements"] = analyze_branding_elements(image_data["pages"])
        
    except Exception as e:
        logger.error(f"Error in comprehensive image extraction: {e}")
        return {"error": str(e)}
    
    return image_data

def analyze_image_content(pix):
    """Analyze image content and properties"""
    
    try:
        # Convert to PIL Image for analysis
        img_data = pix.tobytes("ppm")
        pil_image = Image.open(io.BytesIO(img_data))
        
        # Convert to numpy array for OpenCV analysis
        img_array = np.array(pil_image)
        
        # Basic image analysis
        analysis = {
            "pil_width": pil_image.width,
            "pil_height": pil_image.height,
            "mode": pil_image.mode,
            "format": pil_image.format,
            "size_bytes_pil": len(img_data)
        }
        
        # Color analysis
        if pil_image.mode in ['RGB', 'RGBA']:
            # Convert to OpenCV format
            if pil_image.mode == 'RGBA':
                opencv_image = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
            else:
                opencv_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Analyze colors
            color_analysis = analyze_image_colors(opencv_image)
            analysis.update(color_analysis)
            
            # Analyze edges and shapes
            edge_analysis = analyze_image_edges(opencv_image)
            analysis.update(edge_analysis)
            
            # Analyze texture
            texture_analysis = analyze_image_texture(opencv_image)
            analysis.update(texture_analysis)
        
        return analysis
        
    except Exception as e:
        logger.warning(f"Error in image content analysis: {e}")
        return {}

def analyze_image_colors(opencv_image):
    """Analyze color properties of image"""
    
    try:
        # Convert to different color spaces
        hsv = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        
        # Calculate color statistics
        mean_color = cv2.mean(opencv_image)
        std_color = cv2.meanStdDev(opencv_image)[1].flatten()
        
        color_stats = {
            "mean_color": [float(x) for x in mean_color],
            "std_color": [float(x) for x in std_color],
            "brightness": float(np.mean(gray)),
            "contrast": float(np.std(gray)),
            "saturation": float(np.mean(hsv[:, :, 1])),
            "hue_variety": int(len(np.unique(hsv[:, :, 0])))
        }
        
        # Detect if image is mostly monochrome
        color_variance = np.var(opencv_image, axis=(0, 1))
        color_stats["is_monochrome"] = bool(np.all(color_variance < 1000))
        color_stats["color_variance"] = float(np.mean(color_variance))
        
        # Detect if image has high contrast (potential logo)
        color_stats["high_contrast"] = bool(color_stats["contrast"] > 50)
        
        return color_stats
        
    except Exception as e:
        logger.warning(f"Error in color analysis: {e}")
        return {}

def analyze_image_edges(opencv_image):
    """Analyze edges and shapes in image"""
    
    try:
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze contours
        if contours:
            areas = [cv2.contourArea(c) for c in contours]
            perimeters = [cv2.arcLength(c, True) for c in contours]
            
            edge_analysis = {
                "num_contours": int(len(contours)),
                "total_edge_area": float(sum(areas)),
                "avg_contour_area": float(np.mean(areas) if areas else 0),
                "max_contour_area": float(max(areas) if areas else 0),
                "total_perimeter": float(sum(perimeters)),
                "edge_density": float(len(edges[edges > 0]) / edges.size)
            }
            
            # Detect geometric shapes
            shape_analysis = detect_geometric_shapes(contours)
            edge_analysis.update(shape_analysis)
            
        else:
            edge_analysis = {
                "num_contours": 0,
                "total_edge_area": 0,
                "avg_contour_area": 0,
                "max_contour_area": 0,
                "total_perimeter": 0,
                "edge_density": 0
            }
        
        return edge_analysis
        
    except Exception as e:
        logger.warning(f"Error in edge analysis: {e}")
        return {}

def detect_geometric_shapes(contours):
    """Detect geometric shapes in contours"""
    
    shapes = {
        "circles": 0,
        "rectangles": 0,
        "triangles": 0,
        "complex_shapes": 0
    }
    
    for contour in contours:
        if len(contour) < 3:
            continue
            
        # Approximate contour to polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Count vertices
        vertices = len(approx)
        
        if vertices == 3:
            shapes["triangles"] += 1
        elif vertices == 4:
            # Check if it's a rectangle
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.8 <= aspect_ratio <= 1.2:  # Close to square
                shapes["rectangles"] += 1
        elif vertices > 8:
            # Check if it's approximately circular
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                if circularity > 0.8:
                    shapes["circles"] += 1
                else:
                    shapes["complex_shapes"] += 1
        else:
            shapes["complex_shapes"] += 1
    
    return shapes

def analyze_image_texture(opencv_image):
    """Analyze texture properties of image"""
    
    try:
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        
        # Calculate texture features using GLCM-like approach
        texture_features = {
            "smoothness": float(calculate_smoothness(gray)),
            "uniformity": float(calculate_uniformity(gray)),
            "entropy": float(calculate_entropy(gray))
        }
        
        return texture_features
        
    except Exception as e:
        logger.warning(f"Error in texture analysis: {e}")
        return {}

def calculate_smoothness(gray_image):
    """Calculate image smoothness"""
    laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
    return float(np.var(laplacian))

def calculate_uniformity(gray_image):
    """Calculate image uniformity"""
    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
    hist_norm = hist / hist.sum()
    return float(np.sum(hist_norm ** 2))

def calculate_entropy(gray_image):
    """Calculate image entropy"""
    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
    hist_norm = hist / hist.sum()
    hist_norm = hist_norm[hist_norm > 0]
    return float(-np.sum(hist_norm * np.log2(hist_norm)))

def categorize_image_type(img_info):
    """Categorize image based on its properties"""
    
    # Check if it's likely a logo
    if is_potential_logo(img_info):
        return "logo"
    
    # Check if it's likely a photo
    if is_potential_photo(img_info):
        return "photo"
    
    # Check if it's likely an icon
    if is_potential_icon(img_info):
        return "icon"
    
    # Check if it's likely a graphic/illustration
    if is_potential_graphic(img_info):
        return "graphic"
    
    return "unknown"

def is_potential_logo(img_info):
    """Check if image is likely a logo"""
    
    # Logo characteristics
    logo_indicators = 0
    
    # Size indicators (logos are usually small to medium)
    if 50 <= img_info.get("width", 0) <= 500 and 50 <= img_info.get("height", 0) <= 500:
        logo_indicators += 1
    
    # Aspect ratio (logos are often square or close to square)
    aspect_ratio = img_info.get("aspect_ratio", 0)
    if 0.5 <= aspect_ratio <= 2.0:
        logo_indicators += 1
    
    # High contrast indicator
    if img_info.get("high_contrast", False):
        logo_indicators += 1
    
    # Edge density (logos often have clear edges)
    if img_info.get("edge_density", 0) > 0.1:
        logo_indicators += 1
    
    # Color variety (logos often have limited colors)
    if img_info.get("hue_variety", 0) < 50:
        logo_indicators += 1
    
    return logo_indicators >= 3

def is_potential_photo(img_info):
    """Check if image is likely a photo"""
    
    # Photo characteristics
    photo_indicators = 0
    
    # Size indicators (photos are usually larger)
    if img_info.get("width", 0) > 200 and img_info.get("height", 0) > 200:
        photo_indicators += 1
    
    # Low contrast (photos often have natural contrast)
    if not img_info.get("high_contrast", False):
        photo_indicators += 1
    
    # High color variety
    if img_info.get("hue_variety", 0) > 100:
        photo_indicators += 1
    
    # Low edge density (photos have natural edges)
    if img_info.get("edge_density", 0) < 0.05:
        photo_indicators += 1
    
    return photo_indicators >= 2

def is_potential_icon(img_info):
    """Check if image is likely an icon"""
    
    # Icon characteristics
    icon_indicators = 0
    
    # Small size
    if img_info.get("width", 0) < 100 and img_info.get("height", 0) < 100:
        icon_indicators += 1
    
    # Square aspect ratio
    aspect_ratio = img_info.get("aspect_ratio", 0)
    if 0.8 <= aspect_ratio <= 1.2:
        icon_indicators += 1
    
    # High contrast
    if img_info.get("high_contrast", False):
        icon_indicators += 1
    
    # Simple shapes
    if img_info.get("num_contours", 0) < 10:
        icon_indicators += 1
    
    return icon_indicators >= 3

def is_potential_graphic(img_info):
    """Check if image is likely a graphic/illustration"""
    
    # Graphic characteristics
    graphic_indicators = 0
    
    # Medium size
    if 100 <= img_info.get("width", 0) <= 800 and 100 <= img_info.get("height", 0) <= 800:
        graphic_indicators += 1
    
    # Medium edge density
    edge_density = img_info.get("edge_density", 0)
    if 0.05 <= edge_density <= 0.2:
        graphic_indicators += 1
    
    # Medium color variety
    hue_variety = img_info.get("hue_variety", 0)
    if 20 <= hue_variety <= 150:
        graphic_indicators += 1
    
    return graphic_indicators >= 2

def extract_graphics_from_page(page):
    """Extract graphics and shapes from page"""
    
    graphics = []
    
    try:
        # Get drawings and paths
        drawings = page.get_drawings()
        
        for drawing in drawings:
            graphic_info = {
                "type": "drawing",
                "rect": drawing.get("rect", []),
                "items": len(drawing.get("items", [])),
                "stroke_color": drawing.get("stroke", {}).get("color"),
                "fill_color": drawing.get("fill", {}).get("color")
            }
            graphics.append(graphic_info)
        
        # Get text blocks that might be graphics (large text)
        text_dict = page.get_text("dict")
        for block in text_dict.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    for span in line.get("spans", []):
                        # Check if this might be a graphic text element
                        if span.get("size", 0) > 20:  # Large text
                            graphic_info = {
                                "type": "text_graphic",
                                "text": span.get("text", ""),
                                "size": span.get("size", 0),
                                "font": span.get("font", ""),
                                "bbox": span.get("bbox", []),
                                "color": span.get("color", 0)
                            }
                            graphics.append(graphic_info)
    
    except Exception as e:
        logger.warning(f"Error extracting graphics: {e}")
    
    return graphics

def analyze_pdfplumber_image(img):
    """Analyze image from pdfplumber"""
    
    return {
        "source": "pdfplumber",
        "area": img["width"] * img["height"],
        "aspect_ratio": img["width"] / img["height"] if img["height"] > 0 else 0
    }

def calculate_page_image_stats(page_images):
    """Calculate statistics for images on a page"""
    
    images = page_images["images"]
    
    if not images:
        return {
            "total_images": 0,
            "total_area": 0,
            "avg_size": 0,
            "image_types": {},
            "placement_zones": {}
        }
    
    # Calculate basic stats
    total_images = len(images)
    total_area = sum(img.get("area", 0) for img in images)
    avg_size = total_area / total_images if total_images > 0 else 0
    
    # Count image types
    type_counts = Counter(img.get("type", "unknown") for img in images)
    
    # Analyze placement zones
    placement_zones = analyze_placement_zones(images)
    
    return {
        "total_images": total_images,
        "total_area": total_area,
        "avg_size": avg_size,
        "image_types": dict(type_counts),
        "placement_zones": placement_zones
    }

def analyze_placement_zones(images):
    """Analyze where images are placed on the page"""
    
    zones = {
        "top_left": 0,
        "top_center": 0,
        "top_right": 0,
        "center_left": 0,
        "center": 0,
        "center_right": 0,
        "bottom_left": 0,
        "bottom_center": 0,
        "bottom_right": 0
    }
    
    for img in images:
        center_x = img.get("center_x", 0)
        center_y = img.get("center_y", 0)
        
        # Determine zone based on position
        if center_y < 0.33:
            if center_x < 0.33:
                zones["top_left"] += 1
            elif center_x < 0.67:
                zones["top_center"] += 1
            else:
                zones["top_right"] += 1
        elif center_y < 0.67:
            if center_x < 0.33:
                zones["center_left"] += 1
            elif center_x < 0.67:
                zones["center"] += 1
            else:
                zones["center_right"] += 1
        else:
            if center_x < 0.33:
                zones["bottom_left"] += 1
            elif center_x < 0.67:
                zones["bottom_center"] += 1
            else:
                zones["bottom_right"] += 1
    
    return zones

def analyze_overall_image_stats(pages):
    """Analyze overall image statistics across all pages"""
    
    all_images = []
    all_logos = []
    all_graphics = []
    
    for page in pages:
        all_images.extend(page["images"])
        all_logos.extend(page["logos"])
        all_graphics.extend(page["graphics"])
    
    return {
        "total_images": len(all_images),
        "total_logos": len(all_logos),
        "total_graphics": len(all_graphics),
        "images_per_page": len(all_images) / len(pages) if pages else 0,
        "total_image_area": sum(img.get("area", 0) for img in all_images),
        "avg_image_size": sum(img.get("area", 0) for img in all_images) / len(all_images) if all_images else 0
    }

def analyze_image_types(pages):
    """Analyze distribution of image types"""
    
    type_counts = Counter()
    type_areas = defaultdict(list)
    
    for page in pages:
        for img in page["images"]:
            img_type = img.get("type", "unknown")
            type_counts[img_type] += 1
            type_areas[img_type].append(img.get("area", 0))
    
    return {
        "type_distribution": dict(type_counts),
        "type_areas": {img_type: sum(areas) for img_type, areas in type_areas.items()},
        "avg_areas_by_type": {img_type: sum(areas) / len(areas) if areas else 0 
                             for img_type, areas in type_areas.items()}
    }

def analyze_logos(pages):
    """Analyze logo patterns and consistency"""
    
    logos = []
    for page in pages:
        logos.extend(page["logos"])
    
    if not logos:
        return {
            "total_logos": 0,
            "logo_consistency": 0,
            "logo_positions": {},
            "logo_sizes": {}
        }
    
    # Analyze logo consistency
    logo_sizes = [(logo.get("width", 0), logo.get("height", 0)) for logo in logos]
    size_variance = float(np.var(logo_sizes)) if len(logo_sizes) > 1 else 0.0
    
    # Analyze logo positions
    positions = [(logo.get("center_x", 0), logo.get("center_y", 0)) for logo in logos]
    position_variance = float(np.var(positions)) if len(positions) > 1 else 0.0
    
    return {
        "total_logos": len(logos),
        "logo_consistency": 1 / (1 + size_variance + position_variance),
        "logo_positions": positions,
        "logo_sizes": logo_sizes,
        "size_variance": size_variance,
        "position_variance": position_variance
    }

def analyze_image_quality(pages):
    """Analyze image quality across all pages"""
    
    all_images = []
    for page in pages:
        all_images.extend(page["images"])
    
    if not all_images:
        return {
            "avg_resolution": 0,
            "quality_distribution": {},
            "compression_analysis": {}
        }
    
    # Analyze resolution
    resolutions = []
    for img in all_images:
        if img.get("width") and img.get("height"):
            resolution = img["width"] * img["height"]
            resolutions.append(resolution)
    
    # Analyze quality indicators
    quality_indicators = {
        "high_resolution": sum(1 for r in resolutions if r > 1000000),
        "medium_resolution": sum(1 for r in resolutions if 100000 <= r <= 1000000),
        "low_resolution": sum(1 for r in resolutions if r < 100000)
    }
    
    return {
        "avg_resolution": np.mean(resolutions) if resolutions else 0,
        "quality_distribution": quality_indicators,
        "compression_analysis": {
            "total_size": sum(img.get("size_bytes", 0) for img in all_images),
            "avg_size_per_image": sum(img.get("size_bytes", 0) for img in all_images) / len(all_images)
        }
    }

def analyze_image_placement(pages):
    """Analyze image placement patterns"""
    
    placement_patterns = {
        "consistent_placement": False,
        "placement_preferences": {},
        "spacing_analysis": {}
    }
    
    # Analyze placement preferences across pages
    all_placements = []
    for page in pages:
        for img in page["images"]:
            center_x = img.get("center_x", 0)
            center_y = img.get("center_y", 0)
            all_placements.append((center_x, center_y))
    
    if all_placements:
        # Check for consistent placement
        x_positions = [pos[0] for pos in all_placements]
        y_positions = [pos[1] for pos in all_placements]
        
        x_variance = float(np.var(x_positions))
        y_variance = float(np.var(y_positions))
        
        placement_patterns["consistent_placement"] = (x_variance < 0.1 and y_variance < 0.1)
        placement_patterns["placement_preferences"] = {
            "x_variance": x_variance,
            "y_variance": y_variance,
            "avg_x": float(np.mean(x_positions)),
            "avg_y": float(np.mean(y_positions))
        }
    
    return placement_patterns

def analyze_branding_elements(pages):
    """Analyze branding elements in images"""
    
    branding_analysis = {
        "logo_usage": {},
        "color_consistency": {},
        "style_consistency": {},
        "branding_score": 0
    }
    
    # Analyze logo usage patterns
    logo_positions = []
    logo_sizes = []
    
    for page in pages:
        for logo in page["logos"]:
            logo_positions.append((logo.get("center_x", 0), logo.get("center_y", 0)))
            logo_sizes.append((logo.get("width", 0), logo.get("height", 0)))
    
    if logo_positions:
        # Calculate logo consistency
        position_variance = float(np.var(logo_positions)) if len(logo_positions) > 1 else 0.0
        size_variance = float(np.var(logo_sizes)) if len(logo_sizes) > 1 else 0.0
        
        branding_analysis["logo_usage"] = {
            "total_logos": len(logo_positions),
            "position_consistency": 1 / (1 + position_variance),
            "size_consistency": 1 / (1 + size_variance)
        }
        
        # Calculate overall branding score
        branding_score = (
            branding_analysis["logo_usage"]["position_consistency"] * 0.4 +
            branding_analysis["logo_usage"]["size_consistency"] * 0.4 +
            (1 if len(logo_positions) > 0 else 0) * 0.2
        )
        branding_analysis["branding_score"] = float(branding_score)
    
    return branding_analysis 