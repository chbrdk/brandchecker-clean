import os
import re
import json
import logging
import numpy as np
import colorsys
import io
from collections import Counter
import tempfile
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def rgb_to_hex(r, g, b):
    """Convert RGB values to hex color with improved precision"""
    return f"#{r:02x}{g:02x}{b:02x}"

def convert_color_with_precision(color_val, color_space="rgb"):
    """Convert color values with high precision and multiple color space support"""
    try:
        if isinstance(color_val, (list, tuple)):
            if len(color_val) == 3:
                r, g, b = color_val
                
                # Handle normalized values (0-1)
                if r <= 1 and g <= 1 and b <= 1:
                    r, g, b = r * 255, g * 255, b * 255
                
                # Round with precision
                r_precise = round(r, 2)
                g_precise = round(g, 2)
                b_precise = round(b, 2)
                
                # Final RGB integers
                r_int = round(r_precise)
                g_int = round(g_precise)
                b_int = round(b_precise)
                
                return {
                    "rgb": [r_int, g_int, b_int],
                    "rgb_precise": [r_precise, g_precise, b_precise],
                    "hex": rgb_to_hex(r_int, g_int, b_int),
                    "original": color_val,
                    "color_space": color_space
                }
            elif len(color_val) == 4:
                # CMYK values
                c, m, y, k = color_val
                # Convert CMYK to RGB (simplified)
                r = 255 * (1 - c) * (1 - k)
                g = 255 * (1 - m) * (1 - k)
                b = 255 * (1 - y) * (1 - k)
                
                r_int, g_int, b_int = round(r), round(g), round(b)
                
                return {
                    "rgb": [r_int, g_int, b_int],
                    "cmyk": [c, m, y, k],
                    "hex": rgb_to_hex(r_int, g_int, b_int),
                    "original": color_val,
                    "color_space": "cmyk"
                }
        elif isinstance(color_val, (int, float)):
            # Single value (grayscale)
            if color_val <= 1:
                val = color_val * 255
            else:
                val = color_val
            
            val_int = round(val)
            return {
                "rgb": [val_int, val_int, val_int],
                "gray": val,
                "hex": rgb_to_hex(val_int, val_int, val_int),
                "original": color_val,
                "color_space": "gray"
            }
        
        return None
    except Exception as e:
        logger.error(f"Error converting color: {e}")
        return None

def correct_color_values(color_info, expected_colors=None):
    """Attempt to correct color values to match expected colors"""
    if not color_info or not expected_colors:
        return color_info
    
    try:
        current_hex = color_info["hex"]
        current_rgb = color_info["rgb"]
        
        # Find closest expected color
        min_distance = float('inf')
        closest_expected = None
        
        for expected_hex in expected_colors:
            # Convert hex to RGB
            expected_rgb = [
                int(expected_hex[1:3], 16),
                int(expected_hex[3:5], 16),
                int(expected_hex[5:7], 16)
            ]
            
            # Calculate color distance
            distance = sum((a - b) ** 2 for a, b in zip(current_rgb, expected_rgb)) ** 0.5
            
            if distance < min_distance:
                min_distance = distance
                closest_expected = expected_hex
        
        # If the distance is small enough, suggest correction
        if min_distance < 50:  # Threshold for color similarity
            corrected_rgb = [
                int(closest_expected[1:3], 16),
                int(closest_expected[3:5], 16),
                int(closest_expected[5:7], 16)
            ]
            
            color_info["corrected_rgb"] = corrected_rgb
            color_info["corrected_hex"] = closest_expected
            color_info["correction_distance"] = min_distance
            color_info["correction_applied"] = True
        
        return color_info
    except Exception as e:
        logger.error(f"Error correcting color values: {e}")
        return color_info

def rgb_to_hsv(r, g, b):
    """Convert RGB to HSV"""
    r, g, b = r/255.0, g/255.0, b/255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h * 360, s * 100, v * 100

def get_color_name(r, g, b):
    """Get approximate color name based on RGB values"""
    h, s, v = rgb_to_hsv(r, g, b)
    
    if v < 20:
        return "Black"
    elif v > 80 and s < 20:
        return "White"
    elif s < 20:
        return "Gray"
    elif h < 30 or h > 330:
        return "Red"
    elif 30 <= h < 60:
        return "Orange"
    elif 60 <= h < 90:
        return "Yellow"
    elif 90 <= h < 150:
        return "Green"
    elif 150 <= h < 240:
        return "Blue"
    elif 240 <= h < 300:
        return "Purple"
    else:
        return "Pink"

def extract_colors_from_image(image_array, max_colors=20):
    """Extract dominant colors from image using K-means clustering"""
    colors = []
    
    try:
        # Import libraries here to avoid import issues
        from sklearn.cluster import KMeans
        
        # Reshape image for clustering
        pixels = image_array.reshape(-1, 3)
        
        # Use K-means to find dominant colors
        if len(pixels) > max_colors:
            kmeans = KMeans(n_clusters=max_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # Get cluster centers and counts
            cluster_centers = kmeans.cluster_centers_
            cluster_counts = np.bincount(kmeans.labels_)
            
            # Create color information
            for i, (center, count) in enumerate(zip(cluster_centers, cluster_counts)):
                r, g, b = int(center[0]), int(center[1]), int(center[2])
                hex_color = rgb_to_hex(r, g, b)
                color_name = get_color_name(r, g, b)
                
                colors.append({
                    "rgb": [r, g, b],
                    "hex": hex_color,
                    "name": color_name,
                    "count": int(count),
                    "percentage": float(count / len(pixels) * 100)
                })
            
            # Sort by usage
            colors.sort(key=lambda x: x["count"], reverse=True)
        
    except Exception as e:
        logger.error(f"Error in image color extraction: {e}")
    
    return colors

def extract_colors_from_pdf_comprehensive(pdf_path):
    """Comprehensive color extraction from PDF using multiple methods"""
    
    # Import libraries here to avoid import issues
    import fitz  # PyMuPDF
    import cv2
    from PIL import Image
    import pdfplumber
    from sklearn.cluster import KMeans
    
    all_colors = []
    color_sources = {
        "text_colors": [],
        "image_colors": [],
        "vector_colors": [],
        "background_colors": []
    }
    
    try:
        # Method 1: PyMuPDF for overall page analysis
        logger.info("Starting PyMuPDF analysis...")
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Convert page to image for color analysis
            mat = fitz.Matrix(2.0, 2.0)  # Higher resolution for better color detection
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to numpy array
            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.height, pix.width, pix.n
            )
            
            # Convert RGBA to RGB if necessary
            if pix.n == 4:
                img_array = img_array[:, :, :3]
            
            # Extract colors from the page image
            page_colors = extract_colors_from_image(img_array, max_colors=15)
            
            for color in page_colors:
                color["source"] = "page_image"
                color["page"] = page_num + 1
                all_colors.append(color)
                color_sources["image_colors"].append(color)
            
            # Extract text colors using PyMuPDF
            text_dict = page.get_text("dict")
            for block in text_dict.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line.get("spans", []):
                            if "color" in span:
                                color_val = span["color"]
                                if color_val != 0:  # Not black
                                    r, g, b = int(color_val), int(color_val), int(color_val)
                                    hex_color = rgb_to_hex(r, g, b)
                                    color_name = get_color_name(r, g, b)
                                    
                                    text_color = {
                                        "rgb": [r, g, b],
                                        "hex": hex_color,
                                        "name": color_name,
                                        "count": 1,
                                        "percentage": 1.0,
                                        "source": "text",
                                        "page": page_num + 1
                                    }
                                    all_colors.append(text_color)
                                    color_sources["text_colors"].append(text_color)
        
        doc.close()
        
        # Method 2: pdfplumber for detailed text and shape analysis
        logger.info("Starting pdfplumber analysis...")
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract text with color information
                chars = page.chars
                for char in chars:
                    if "non_stroking_color" in char and char["non_stroking_color"]:
                        color_val = char["non_stroking_color"]
                        if isinstance(color_val, (list, tuple)) and len(color_val) >= 3:
                            r, g, b = int(color_val[0] * 255), int(color_val[1] * 255), int(color_val[2] * 255)
                            hex_color = rgb_to_hex(r, g, b)
                            color_name = get_color_name(r, g, b)
                            
                            text_color = {
                                "rgb": [r, g, b],
                                "hex": hex_color,
                                "name": color_name,
                                "count": 1,
                                "percentage": 1.0,
                                "source": "text_detailed",
                                "page": page_num + 1
                            }
                            all_colors.append(text_color)
                            color_sources["text_colors"].append(text_color)
                
                # Extract shapes and their colors (using different method)
                try:
                    # Try to get shapes using different pdfplumber methods
                    if hasattr(page, 'shapes'):
                        shapes = page.shapes
                        for shape in shapes:
                            if "stroke_color" in shape and shape["stroke_color"]:
                                color_val = shape["stroke_color"]
                                if isinstance(color_val, (list, tuple)) and len(color_val) >= 3:
                                    r, g, b = int(color_val[0] * 255), int(color_val[1] * 255), int(color_val[2] * 255)
                                    hex_color = rgb_to_hex(r, g, b)
                                    color_name = get_color_name(r, g, b)
                                    
                                    vector_color = {
                                        "rgb": [r, g, b],
                                        "hex": hex_color,
                                        "name": color_name,
                                        "count": 1,
                                        "percentage": 1.0,
                                        "source": "vector_shape",
                                        "page": page_num + 1
                                    }
                                    all_colors.append(vector_color)
                                    color_sources["vector_colors"].append(vector_color)
                except Exception as e:
                    logger.warning(f"Could not extract shapes from page {page_num + 1}: {e}")
        
        # Method 3: OpenCV for advanced image processing
        logger.info("Starting OpenCV analysis...")
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Convert to high-resolution image
            mat = fitz.Matrix(3.0, 3.0)  # Very high resolution
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("ppm")
            pil_image = Image.open(io.BytesIO(img_data))
            
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Apply color enhancement
            enhanced = cv2.convertScaleAbs(opencv_image, alpha=1.2, beta=10)
            
            # Extract colors from enhanced image
            enhanced_colors = extract_colors_from_image(enhanced, max_colors=10)
            
            for color in enhanced_colors:
                color["source"] = "opencv_enhanced"
                color["page"] = page_num + 1
                all_colors.append(color)
                color_sources["image_colors"].append(color)
        
        doc.close()
        
    except Exception as e:
        logger.error(f"Error in comprehensive color extraction: {e}")
        return {"error": str(e)}
    
    # Aggregate and analyze all colors
    color_analysis = aggregate_colors(all_colors, color_sources)
    
    return color_analysis

def aggregate_colors(all_colors, color_sources):
    """Aggregate and analyze all extracted colors"""
    
    # Group colors by hex value
    color_groups = {}
    
    for color in all_colors:
        hex_val = color["hex"]
        if hex_val not in color_groups:
            color_groups[hex_val] = {
                "rgb": color["rgb"],
                "hex": hex_val,
                "name": color["name"],
                "total_count": 0,
                "sources": set(),
                "pages": set(),
                "details": []
            }
        
        color_groups[hex_val]["total_count"] += color["count"]
        color_groups[hex_val]["sources"].add(color["source"])
        color_groups[hex_val]["pages"].add(color["page"])
        color_groups[hex_val]["details"].append(color)
    
    # Calculate total usage
    total_usage = sum(group["total_count"] for group in color_groups.values())
    
    # Create final color list
    final_colors = []
    for hex_val, group in color_groups.items():
        percentage = (group["total_count"] / total_usage * 100) if total_usage > 0 else 0
        
        final_color = {
            "rgb": group["rgb"],
            "hex": hex_val,
            "name": group["name"],
            "usage_count": group["total_count"],
            "usage_percentage": round(percentage, 2),
            "sources": list(group["sources"]),
            "pages": list(group["pages"]),
            "description": f"{group['name']} color used {group['total_count']} times ({percentage:.1f}%) across {len(group['sources'])} sources"
        }
        final_colors.append(final_color)
    
    # Sort by usage
    final_colors.sort(key=lambda x: x["usage_count"], reverse=True)
    
    # Create summary
    summary = {
        "total_colors": len(final_colors),
        "total_usage": total_usage,
        "color_sources": {
            "text_colors": len(color_sources["text_colors"]),
            "image_colors": len(color_sources["image_colors"]),
            "vector_colors": len(color_sources["vector_colors"]),
            "background_colors": len(color_sources["background_colors"])
        },
        "colors": final_colors
    }
    
    return summary 

def extract_design_colors_only(pdf_path):
    """Extract colors only from design elements (text, logos, shapes) - NOT from product images with improved precision"""
    
    import fitz  # PyMuPDF
    import cv2
    from PIL import Image
    import pdfplumber
    
    # New function for direct color extraction from PDF raw data
    def extract_raw_colors_from_pdf(pdf_path):
        """Extract colors directly from PDF raw data without rendering"""
        raw_colors = []
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Get raw page data
                page_dict = page.get_text("rawdict")
                
                # Extract colors from raw text data
                for block in page_dict.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line.get("spans", []):
                                if "color" in span:
                                    color_val = span["color"]
                                    raw_colors.append({
                                        "type": "text",
                                        "page": page_num + 1,
                                        "raw_value": color_val,
                                        "source": "raw_text"
                                    })
                
                # Extract colors from raw drawing data
                drawings = page.get_drawings()
                for drawing in drawings:
                    if "stroke" in drawing and drawing["stroke"]:
                        raw_colors.append({
                            "type": "stroke",
                            "page": page_num + 1,
                            "raw_value": drawing["stroke"],
                            "source": "raw_drawing"
                        })
                    
                    if "fill" in drawing and drawing["fill"]:
                        raw_colors.append({
                            "type": "fill",
                            "page": page_num + 1,
                            "raw_value": drawing["fill"],
                            "source": "raw_drawing"
                        })
            
            doc.close()
            return raw_colors
        except Exception as e:
            logger.error(f"Error extracting raw colors: {e}")
            return []
    
    design_colors = []
    color_sources = {
        "text_colors": [],
        "logo_colors": [],
        "shape_colors": [],
        "background_colors": []
    }
    
    try:
        logger.info("Starting improved design-only color analysis...")
        
        # Method 1: Extract raw colors directly from PDF data
        raw_colors = extract_raw_colors_from_pdf(pdf_path)
        logger.info(f"Found {len(raw_colors)} raw color entries")
        
        # Expected colors for correction (if known)
        expected_colors = ["#e30613", "#e41617", "#df231d"]
        
        # Method 2: Extract colors using improved precision
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract text colors using PyMuPDF with improved precision
            text_dict = page.get_text("dict")
            for block in text_dict.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line.get("spans", []):
                            if "color" in span:
                                color_val = span["color"]
                                if color_val != 0:  # Not black
                                    # Use improved color conversion
                                    color_info = convert_color_with_precision(color_val, "text")
                                    if color_info:
                                        # Apply color correction if possible
                                        color_info = correct_color_values(color_info, expected_colors)
                                        color_name = get_color_name(*color_info["rgb"])
                                        
                                        text_color = {
                                            "rgb": color_info["rgb"],
                                            "rgb_precise": color_info.get("rgb_precise", color_info["rgb"]),
                                            "hex": color_info["hex"],
                                            "name": color_name,
                                            "count": 1,
                                            "percentage": 1.0,
                                            "source": "text",
                                            "page": page_num + 1,
                                            "description": f"Text color: {color_name}",
                                            "original_values": color_info["original"],
                                            "color_space": color_info["color_space"]
                                        }
                                        
                                        # Add correction info if available
                                        if color_info.get("correction_applied"):
                                            text_color["corrected_rgb"] = color_info["corrected_rgb"]
                                            text_color["corrected_hex"] = color_info["corrected_hex"]
                                            text_color["correction_distance"] = color_info["correction_distance"]
                                        
                                        design_colors.append(text_color)
                                        color_sources["text_colors"].append(text_color)
            
            # Extract drawings and shapes (logos, icons) with improved precision
            drawings = page.get_drawings()
            for drawing in drawings:
                if "stroke" in drawing and drawing["stroke"]:
                    stroke_color = drawing["stroke"]
                    if isinstance(stroke_color, (list, tuple)) and len(stroke_color) >= 3:
                        # Use improved color conversion
                        color_info = convert_color_with_precision(stroke_color, "shape_stroke")
                        if color_info:
                            # Apply color correction if possible
                            color_info = correct_color_values(color_info, expected_colors)
                            color_name = get_color_name(*color_info["rgb"])
                            
                            shape_color = {
                                "rgb": color_info["rgb"],
                                "rgb_precise": color_info.get("rgb_precise", color_info["rgb"]),
                                "hex": color_info["hex"],
                                "name": color_name,
                                "count": 1,
                                "percentage": 1.0,
                                "source": "shape",
                                "page": page_num + 1,
                                "description": f"Shape/Logo color: {color_name}",
                                "original_values": color_info["original"],
                                "color_space": color_info["color_space"]
                            }
                            
                            # Add correction info if available
                            if color_info.get("correction_applied"):
                                shape_color["corrected_rgb"] = color_info["corrected_rgb"]
                                shape_color["corrected_hex"] = color_info["corrected_hex"]
                                shape_color["correction_distance"] = color_info["correction_distance"]
                            
                            design_colors.append(shape_color)
                            color_sources["shape_colors"].append(shape_color)
                
                if "fill" in drawing and drawing["fill"]:
                    fill_color = drawing["fill"]
                    if isinstance(fill_color, (list, tuple)) and len(fill_color) >= 3:
                        # Use improved color conversion
                        color_info = convert_color_with_precision(fill_color, "shape_fill")
                        if color_info:
                            # Apply color correction if possible
                            color_info = correct_color_values(color_info, expected_colors)
                            color_name = get_color_name(*color_info["rgb"])
                            
                            fill_color_info = {
                                "rgb": color_info["rgb"],
                                "rgb_precise": color_info.get("rgb_precise", color_info["rgb"]),
                                "hex": color_info["hex"],
                                "name": color_name,
                                "count": 1,
                                "percentage": 1.0,
                                "source": "shape_fill",
                                "page": page_num + 1,
                                "description": f"Shape fill color: {color_name}",
                                "original_values": color_info["original"],
                                "color_space": color_info["color_space"]
                            }
                            
                            # Add correction info if available
                            if color_info.get("correction_applied"):
                                fill_color_info["corrected_rgb"] = color_info["corrected_rgb"]
                                fill_color_info["corrected_hex"] = color_info["corrected_hex"]
                                fill_color_info["correction_distance"] = color_info["correction_distance"]
                            
                            design_colors.append(fill_color_info)
                        color_sources["shape_colors"].append(fill_color_info)
        
        doc.close()
        
        # Method 3: pdfplumber for additional text color details
        logger.info("Starting pdfplumber design analysis...")
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract text with color information
                chars = page.chars
                for char in chars:
                    if "non_stroking_color" in char and char["non_stroking_color"]:
                        color_val = char["non_stroking_color"]
                        if isinstance(color_val, (list, tuple)) and len(color_val) >= 3:
                            r, g, b = int(color_val[0] * 255), int(color_val[1] * 255), int(color_val[2] * 255)
                            hex_color = rgb_to_hex(r, g, b)
                            color_name = get_color_name(r, g, b)
                            
                            text_color = {
                                "rgb": [r, g, b],
                                "hex": hex_color,
                                "name": color_name,
                                "count": 1,
                                "percentage": 1.0,
                                "source": "text_detailed",
                                "page": page_num + 1,
                                "description": f"Detailed text color: {color_name}"
                            }
                            design_colors.append(text_color)
                            color_sources["text_colors"].append(text_color)
        
        # Aggregate and deduplicate colors
        aggregated_colors = aggregate_design_colors(design_colors)
        
        return {
            "design_colors": aggregated_colors,
            "color_sources": color_sources,
            "total_design_colors": len(aggregated_colors),
            "analysis_method": "design_elements_only"
        }
        
    except Exception as e:
        logger.error(f"Error in design-only color extraction: {e}")
        return {"error": str(e)}

def aggregate_design_colors(design_colors):
    """Aggregate and deduplicate design colors with improved precision data"""
    
    color_groups = {}
    
    for color in design_colors:
        hex_val = color["hex"]
        if hex_val not in color_groups:
            color_groups[hex_val] = {
                "rgb": color["rgb"],
                "hex": hex_val,
                "name": color["name"],
                "count": 0,
                "sources": set(),
                "pages": set(),
                "descriptions": [],
                "rgb_precise": color.get("rgb_precise"),
                "original_values": color.get("original_values"),
                "color_space": color.get("color_space"),
                "all_original_values": [],
                "corrected_rgb": color.get("corrected_rgb"),
                "corrected_hex": color.get("corrected_hex"),
                "correction_distance": color.get("correction_distance")
            }
        
        color_groups[hex_val]["count"] += 1
        color_groups[hex_val]["sources"].add(color["source"])
        color_groups[hex_val]["pages"].add(color["page"])
        color_groups[hex_val]["descriptions"].append(color.get("description", ""))
        
        # Collect all original values for this color
        if color.get("original_values"):
            color_groups[hex_val]["all_original_values"].append(color["original_values"])
    
    # Convert to list format
    aggregated = []
    total_count = sum(group["count"] for group in color_groups.values())
    
    for hex_val, group in color_groups.items():
        aggregated.append({
            "rgb": group["rgb"],
            "hex": hex_val,
            "name": group["name"],
            "usage_count": group["count"],
            "usage_percentage": (group["count"] / total_count * 100) if total_count > 0 else 0,
            "sources": list(group["sources"]),
            "pages": list(group["pages"]),
            "description": f"{group['name']} color used {group['count']} times across {len(group['sources'])} sources",
            "all_descriptions": group["descriptions"],
            "rgb_precise": group["rgb_precise"],
            "original_values": group["original_values"],
            "color_space": group["color_space"],
            "all_original_values": group["all_original_values"],
            "corrected_rgb": group["corrected_rgb"],
            "corrected_hex": group["corrected_hex"],
            "correction_distance": group["correction_distance"]
        })
    
    # Sort by usage count
    aggregated.sort(key=lambda x: x["usage_count"], reverse=True)
    
    return aggregated 

def extract_color_profiles(pdf_path):
    """Extract color profiles and color space information from PDF"""
    
    import fitz  # PyMuPDF
    import pdfplumber
    from PIL import Image
    import io
    
    color_profiles = {
        "pdf_color_spaces": [],
        "image_color_profiles": [],
        "text_color_spaces": [],
        "overall_color_management": {}
    }
    
    try:
        logger.info("Starting color profile analysis...")
        
        # Method 1: PyMuPDF for PDF-level color spaces
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get page resources (fonts, images, color spaces)
            resources = page.get_text("dict").get("resources", {})
            
            # Extract color spaces
            if "ColorSpace" in resources:
                color_spaces = resources["ColorSpace"]
                for cs_name, cs_def in color_spaces.items():
                    color_profiles["pdf_color_spaces"].append({
                        "name": cs_name,
                        "definition": cs_def,
                        "page": page_num + 1,
                        "type": "pdf_color_space"
                    })
            
            # Extract images and their color profiles
            image_list = page.get_images()
            for img_index, img in enumerate(image_list):
                try:
                    # Get image data
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    if pix.n - pix.alpha > 1:  # Not grayscale
                        # Try to extract color profile info
                        img_info = {
                            "page": page_num + 1,
                            "image_index": img_index,
                            "width": pix.width,
                            "height": pix.height,
                            "colorspace": pix.colorspace.name if pix.colorspace else "Unknown",
                            "n_components": pix.n,
                            "has_alpha": pix.alpha > 0
                        }
                        
                        # Try to get ICC profile info
                        try:
                            # Convert to PIL Image to check for ICC profile
                            img_data = pix.tobytes("png")
                            pil_img = Image.open(io.BytesIO(img_data))
                            
                            if hasattr(pil_img, 'info') and 'icc_profile' in pil_img.info:
                                img_info["icc_profile"] = {
                                    "present": True,
                                    "size": len(pil_img.info['icc_profile']),
                                    "profile_info": extract_icc_profile_info(pil_img.info['icc_profile'])
                                }
                            else:
                                img_info["icc_profile"] = {"present": False}
                                
                        except Exception as e:
                            img_info["icc_profile"] = {"present": False, "error": str(e)}
                        
                        color_profiles["image_color_profiles"].append(img_info)
                    
                    pix = None  # Free memory
                    
                except Exception as e:
                    logger.warning(f"Error processing image {img_index} on page {page_num + 1}: {e}")
        
        doc.close()
        
        # Method 2: pdfplumber for detailed color space analysis
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract text color spaces
                chars = page.chars
                for char in chars:
                    if "non_stroking_color" in char:
                        color_val = char["non_stroking_color"]
                        if isinstance(color_val, (list, tuple)):
                            # Determine color space from number of components
                            if len(color_val) == 1:
                                color_space = "Gray"
                            elif len(color_val) == 3:
                                color_space = "RGB"
                            elif len(color_val) == 4:
                                color_space = "CMYK"
                            else:
                                color_space = f"Unknown({len(color_val)})"
                            
                            color_profiles["text_color_spaces"].append({
                                "page": page_num + 1,
                                "color_space": color_space,
                                "components": len(color_val),
                                "values": color_val
                            })
        
        # Method 3: Analyze overall color management
        color_profiles["overall_color_management"] = analyze_overall_color_management(color_profiles)
        
        return color_profiles
        
    except Exception as e:
        logger.error(f"Error in color profile extraction: {e}")
        return {"error": str(e)}

def extract_icc_profile_info(icc_data):
    """Extract basic information from ICC profile data"""
    
    try:
        # ICC profile header is 128 bytes
        if len(icc_data) < 128:
            return {"error": "ICC profile too small"}
        
        # Extract profile type (bytes 12-15)
        profile_type = icc_data[12:16]
        profile_types = {
            b'sRGB': 'sRGB',
            b'RGB ': 'RGB',
            b'CMYK': 'CMYK',
            b'GRAY': 'Gray',
            b'LAB ': 'Lab'
        }
        
        profile_name = profile_types.get(profile_type, f"Unknown({profile_type})")
        
        # Extract creation date (bytes 24-31)
        creation_date = icc_data[24:32]
        
        return {
            "profile_type": profile_name,
            "creation_date": creation_date.hex(),
            "total_size": len(icc_data)
        }
        
    except Exception as e:
        return {"error": str(e)}

def analyze_overall_color_management(color_profiles):
    """Analyze overall color management strategy"""
    
    analysis = {
        "color_spaces_used": set(),
        "icc_profiles_found": 0,
        "color_management_strategy": "Unknown",
        "recommendations": []
    }
    
    # Analyze text color spaces
    for text_cs in color_profiles["text_color_spaces"]:
        analysis["color_spaces_used"].add(text_cs["color_space"])
    
    # Count ICC profiles
    for img_profile in color_profiles["image_color_profiles"]:
        if img_profile["icc_profile"]["present"]:
            analysis["icc_profiles_found"] += 1
    
    # Determine color management strategy
    color_spaces = list(analysis["color_spaces_used"])
    
    if "CMYK" in color_spaces:
        analysis["color_management_strategy"] = "Print-Optimized"
        analysis["recommendations"].append("CMYK detected - optimized for printing")
    elif "RGB" in color_spaces and analysis["icc_profiles_found"] > 0:
        analysis["color_management_strategy"] = "Color-Managed RGB"
        analysis["recommendations"].append("ICC profiles found - good color management")
    elif "RGB" in color_spaces:
        analysis["color_management_strategy"] = "Standard RGB"
        analysis["recommendations"].append("RGB without ICC profiles - may use sRGB")
    elif "Gray" in color_spaces:
        analysis["color_management_strategy"] = "Grayscale"
        analysis["recommendations"].append("Grayscale document - minimal color management")
    
    # Convert set to list for JSON serialization
    analysis["color_spaces_used"] = list(analysis["color_spaces_used"])
    
    return analysis 

def extract_colors_with_proper_color_space(pdf_path):
    """Extract colors with proper color space detection and format-specific output"""
    
    import fitz  # PyMuPDF
    import pdfplumber
    from PIL import Image
    import io
    import re
    
    # Step 1: Detect color space and profiles
    logger.info("Step 1: Detecting color space and profiles...")
    color_profiles = extract_color_profiles(pdf_path)
    
    # Step 2: Determine primary color space
    primary_color_space = determine_primary_color_space(color_profiles)
    
    # Step 3: Extract colors in the correct format
    logger.info(f"Step 2: Extracting colors in {primary_color_space} format...")
    
    if primary_color_space == "CMYK":
        colors = extract_cmyk_colors(pdf_path, color_profiles)
    elif primary_color_space == "RGB":
        colors = extract_rgb_colors(pdf_path, color_profiles)
    elif primary_color_space == "Pantone":
        colors = extract_pantone_colors(pdf_path, color_profiles)
    elif primary_color_space == "RAL":
        colors = extract_ral_colors(pdf_path, color_profiles)
    elif primary_color_space == "Gray":
        colors = extract_gray_colors(pdf_path, color_profiles)
    else:
        colors = extract_mixed_colors(pdf_path, color_profiles)
    
    return {
        "color_space_analysis": color_profiles,
        "primary_color_space": primary_color_space,
        "colors": colors,
        "total_colors": len(colors),
        "analysis_method": f"color_space_aware_{primary_color_space.lower()}"
    }

def determine_primary_color_space(color_profiles):
    """Determine the primary color space used in the document"""
    
    color_spaces = color_profiles.get("overall_color_management", {}).get("color_spaces_used", [])
    text_spaces = color_profiles.get("text_color_spaces", [])
    img_profiles = color_profiles.get("image_color_profiles", [])
    
    # Priority order: Pantone > RAL > CMYK > RGB > Gray
    if has_pantone_colors(text_spaces):
        return "Pantone"
    elif has_ral_colors(text_spaces):
        return "RAL"
    elif "CMYK" in color_spaces:
        return "CMYK"
    elif "RGB" in color_spaces:
        return "RGB"
    elif "Gray" in color_spaces:
        return "Gray"
    else:
        return "Mixed"

def has_pantone_colors(text_spaces):
    """Check if document contains Pantone colors"""
    pantone_patterns = [
        r'PANTONE\s+\d{3,4}[A-Z]?',
        r'PMS\s+\d{3,4}[A-Z]?',
        r'Pantone\s+\d{3,4}[A-Z]?'
    ]
    
    for space in text_spaces:
        # Check color names or descriptions for Pantone references
        if "pantone" in str(space).lower():
            return True
    
    return False

def has_ral_colors(text_spaces):
    """Check if document contains RAL colors"""
    ral_patterns = [
        r'RAL\s+\d{4}',
        r'RAL\s+\d{4}[A-Z]?'
    ]
    
    for space in text_spaces:
        if "ral" in str(space).lower():
            return True
    
    return False

def extract_cmyk_colors(pdf_path, color_profiles):
    """Extract colors in CMYK format"""
    
    cmyk_colors = []
    
    try:
        # Extract from text color spaces
        text_spaces = color_profiles.get("text_color_spaces", [])
        for space in text_spaces:
            if space.get("color_space") == "CMYK":
                cmyk_values = space.get("values", [])
                if len(cmyk_values) == 4:
                    cmyk_colors.append({
                        "format": "CMYK",
                        "values": {
                            "C": round(cmyk_values[0] * 100, 1),  # Convert to percentage
                            "M": round(cmyk_values[1] * 100, 1),
                            "Y": round(cmyk_values[2] * 100, 1),
                            "K": round(cmyk_values[3] * 100, 1)
                        },
                        "hex": cmyk_to_hex(cmyk_values),
                        "name": get_cmyk_color_name(cmyk_values),
                        "source": "text",
                        "page": space.get("page", 1),
                        "usage_count": 1
                    })
        
        # Extract from image color profiles
        img_profiles = color_profiles.get("image_color_profiles", [])
        for profile in img_profiles:
            if profile.get("colorspace") == "DeviceCMYK":
                cmyk_colors.append({
                    "format": "CMYK",
                    "values": {
                        "C": 0, "M": 0, "Y": 0, "K": 0  # Default for images
                    },
                    "hex": "#000000",
                    "name": "CMYK Image",
                    "source": "image",
                    "page": profile.get("page", 1),
                    "usage_count": 1,
                    "image_info": {
                        "width": profile.get("width"),
                        "height": profile.get("height")
                    }
                })
        
        # Aggregate and deduplicate
        return aggregate_cmyk_colors(cmyk_colors)
        
    except Exception as e:
        logger.error(f"Error extracting CMYK colors: {e}")
        return []

def extract_rgb_colors(pdf_path, color_profiles):
    """Extract colors in RGB format"""
    
    rgb_colors = []
    
    try:
        # Extract from text color spaces
        text_spaces = color_profiles.get("text_color_spaces", [])
        for space in text_spaces:
            if space.get("color_space") == "RGB":
                rgb_values = space.get("values", [])
                if len(rgb_values) == 3:
                    rgb_colors.append({
                        "format": "RGB",
                        "values": {
                            "R": int(rgb_values[0] * 255),
                            "G": int(rgb_values[1] * 255),
                            "B": int(rgb_values[2] * 255)
                        },
                        "hex": rgb_to_hex(int(rgb_values[0] * 255), int(rgb_values[1] * 255), int(rgb_values[2] * 255)),
                        "name": get_color_name(int(rgb_values[0] * 255), int(rgb_values[1] * 255), int(rgb_values[2] * 255)),
                        "source": "text",
                        "page": space.get("page", 1),
                        "usage_count": 1
                    })
        
        return aggregate_rgb_colors(rgb_colors)
        
    except Exception as e:
        logger.error(f"Error extracting RGB colors: {e}")
        return []

def extract_pantone_colors(pdf_path, color_profiles):
    """Extract Pantone colors"""
    
    pantone_colors = []
    
    try:
        # This would require more sophisticated Pantone detection
        # For now, we'll extract CMYK colors and try to match to Pantone
        cmyk_colors = extract_cmyk_colors(pdf_path, color_profiles)
        
        for color in cmyk_colors:
            pantone_match = find_pantone_match(color["values"])
            if pantone_match:
                pantone_colors.append({
                    "format": "Pantone",
                    "pantone_code": pantone_match["code"],
                    "pantone_name": pantone_match["name"],
                    "cmyk_values": color["values"],
                    "hex": color["hex"],
                    "source": color["source"],
                    "page": color["page"],
                    "usage_count": color["usage_count"]
                })
        
        return pantone_colors
        
    except Exception as e:
        logger.error(f"Error extracting Pantone colors: {e}")
        return []

def extract_ral_colors(pdf_path, color_profiles):
    """Extract RAL colors"""
    
    ral_colors = []
    
    try:
        # Similar to Pantone, would require RAL color matching
        cmyk_colors = extract_cmyk_colors(pdf_path, color_profiles)
        
        for color in cmyk_colors:
            ral_match = find_ral_match(color["values"])
            if ral_match:
                ral_colors.append({
                    "format": "RAL",
                    "ral_code": ral_match["code"],
                    "ral_name": ral_match["name"],
                    "cmyk_values": color["values"],
                    "hex": color["hex"],
                    "source": color["source"],
                    "page": color["page"],
                    "usage_count": color["usage_count"]
                })
        
        return ral_colors
        
    except Exception as e:
        logger.error(f"Error extracting RAL colors: {e}")
        return []

def extract_gray_colors(pdf_path, color_profiles):
    """Extract grayscale colors"""
    
    gray_colors = []
    
    try:
        text_spaces = color_profiles.get("text_color_spaces", [])
        for space in text_spaces:
            if space.get("color_space") == "Gray":
                gray_value = space.get("values", [0])[0]
                gray_percentage = round(gray_value * 100, 1)
                
                gray_colors.append({
                    "format": "Gray",
                    "values": {
                        "Gray": gray_percentage
                    },
                    "hex": gray_to_hex(gray_value),
                    "name": f"Gray {gray_percentage}%",
                    "source": "text",
                    "page": space.get("page", 1),
                    "usage_count": 1
                })
        
        return aggregate_gray_colors(gray_colors)
        
    except Exception as e:
        logger.error(f"Error extracting gray colors: {e}")
        return []

def extract_mixed_colors(pdf_path, color_profiles):
    """Extract colors in mixed format (when multiple color spaces are used)"""
    
    mixed_colors = []
    
    try:
        # Extract all color types and format them appropriately
        cmyk_colors = extract_cmyk_colors(pdf_path, color_profiles)
        rgb_colors = extract_rgb_colors(pdf_path, color_profiles)
        gray_colors = extract_gray_colors(pdf_path, color_profiles)
        
        mixed_colors.extend(cmyk_colors)
        mixed_colors.extend(rgb_colors)
        mixed_colors.extend(gray_colors)
        
        return mixed_colors
        
    except Exception as e:
        logger.error(f"Error extracting mixed colors: {e}")
        return []

# Helper functions for color conversion and aggregation
def cmyk_to_hex(cmyk_values):
    """Convert CMYK values to hex (approximate)"""
    try:
        c, m, y, k = cmyk_values
        r = int(255 * (1 - c) * (1 - k))
        g = int(255 * (1 - m) * (1 - k))
        b = int(255 * (1 - y) * (1 - k))
        return rgb_to_hex(r, g, b)
    except:
        return "#000000"

def gray_to_hex(gray_value):
    """Convert gray value to hex"""
    try:
        gray_int = int(gray_value * 255)
        return rgb_to_hex(gray_int, gray_int, gray_int)
    except:
        return "#000000"

def get_cmyk_color_name(cmyk_values):
    """Get approximate color name from CMYK values"""
    try:
        c, m, y, k = cmyk_values
        
        if k > 0.9:
            return "Black"
        elif c == 0 and m == 0 and y == 0 and k == 0:
            return "White"
        elif c > 0.5 and m < 0.2 and y < 0.2:
            return "Cyan"
        elif m > 0.5 and c < 0.2 and y < 0.2:
            return "Magenta"
        elif y > 0.5 and c < 0.2 and m < 0.2:
            return "Yellow"
        elif c > 0.3 and m > 0.3 and y < 0.2:
            return "Blue"
        elif m > 0.3 and y > 0.3 and c < 0.2:
            return "Red"
        elif c > 0.3 and y > 0.3 and m < 0.2:
            return "Green"
        else:
            return "Mixed CMYK"
    except:
        return "Unknown CMYK"

def find_pantone_match(cmyk_values):
    """Find closest Pantone match for CMYK values"""
    # This would require a Pantone color database
    # For now, return None
    return None

def find_ral_match(cmyk_values):
    """Find closest RAL match for CMYK values"""
    # This would require a RAL color database
    # For now, return None
    return None

def aggregate_cmyk_colors(cmyk_colors):
    """Aggregate and deduplicate CMYK colors"""
    color_groups = {}
    
    for color in cmyk_colors:
        key = f"{color['values']['C']}_{color['values']['M']}_{color['values']['Y']}_{color['values']['K']}"
        if key not in color_groups:
            color_groups[key] = color.copy()
            color_groups[key]["usage_count"] = 0
        color_groups[key]["usage_count"] += 1
    
    return list(color_groups.values())

def aggregate_rgb_colors(rgb_colors):
    """Aggregate and deduplicate RGB colors"""
    color_groups = {}
    
    for color in rgb_colors:
        key = f"{color['values']['R']}_{color['values']['G']}_{color['values']['B']}"
        if key not in color_groups:
            color_groups[key] = color.copy()
            color_groups[key]["usage_count"] = 0
        color_groups[key]["usage_count"] += 1
    
    return list(color_groups.values())

def aggregate_gray_colors(gray_colors):
    """Aggregate and deduplicate gray colors"""
    color_groups = {}
    
    for color in gray_colors:
        key = f"{color['values']['Gray']}"
        if key not in color_groups:
            color_groups[key] = color.copy()
            color_groups[key]["usage_count"] = 0
        color_groups[key]["usage_count"] += 1
    
    return list(color_groups.values()) 

def calculate_color_distance(color1_rgb, color2_rgb):
    """Calculate Euclidean distance between two RGB colors"""
    try:
        r1, g1, b1 = color1_rgb
        r2, g2, b2 = color2_rgb
        
        # Calculate Euclidean distance
        distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
        
        # Normalize to 0-1 scale (max distance is sqrt(255^2 + 255^2 + 255^2) ≈ 441.67)
        normalized_distance = distance / 441.67
        
        return distance, normalized_distance
    except Exception as e:
        logger.error(f"Error calculating color distance: {e}")
        return float('inf'), 1.0

def compare_colors_with_bosch(extracted_colors, bosch_colors=None):
    """
    Compare extracted colors with Bosch colors from database
    Returns enhanced color analysis with Bosch color matches
    """
    try:
        if not bosch_colors:
            # Try to get Bosch colors from database
            try:
                from knowledge_database import knowledge_db_manager
                bosch_results = knowledge_db_manager.search_bosch_colors("", limit=100)
                logger.info(f"Found {len(bosch_results)} Bosch colors from database")
                bosch_colors = []
                for result in bosch_results:
                    if result.get('metadata'):
                        metadata = result['metadata']
                        if isinstance(metadata, str):
                            try:
                                metadata = json.loads(metadata)
                            except:
                                metadata = {}
                        
                        hex_code = metadata.get('hex_code')
                        rgb_values = metadata.get('rgb_values')
                        color_family = metadata.get('color_family')
                        variant_name = metadata.get('variant_name')
                        ral_code = metadata.get('ral')
                        pms_code = metadata.get('pms')
                        
                        if hex_code and rgb_values:
                            # Ensure rgb_values is a list
                            if isinstance(rgb_values, str):
                                try:
                                    rgb_values = json.loads(rgb_values)
                                except:
                                    # Try to parse as comma-separated string
                                    rgb_values = [int(x.strip()) for x in rgb_values.strip('[]').split(',') if x.strip().isdigit()]
                            
                            if isinstance(rgb_values, list) and len(rgb_values) >= 3:
                                bosch_colors.append({
                                    'hex_code': hex_code,
                                    'rgb_values': rgb_values[:3],  # Take first 3 values
                                    'color_family': color_family,
                                    'variant_name': variant_name,
                                    'ral_code': ral_code,
                                    'pms_code': pms_code,
                                    'content': result.get('content', '')
                                })
                                logger.debug(f"Added Bosch color: {hex_code} - RGB: {rgb_values[:3]}")
            except Exception as e:
                logger.error(f"Error loading Bosch colors from database: {e}")
                bosch_colors = []
        
        logger.info(f"Processing {len(extracted_colors)} extracted colors against {len(bosch_colors)} Bosch colors")
        
        if not bosch_colors:
            logger.warning("No Bosch colors available for comparison")
            return extracted_colors
        
        enhanced_colors = []
        
        for color in extracted_colors:
            enhanced_color = color.copy()
            enhanced_color['bosch_matches'] = []
            enhanced_color['best_bosch_match'] = None
            enhanced_color['color_compliance'] = 'unknown'
            
            # Get RGB values for comparison
            color_rgb = None
            if 'rgb' in color:
                color_rgb = color['rgb']
            elif 'hex' in color:
                # Convert hex to RGB
                hex_val = color['hex'].replace('#', '')
                if len(hex_val) == 6:
                    r = int(hex_val[0:2], 16)
                    g = int(hex_val[2:4], 16)
                    b = int(hex_val[4:6], 16)
                    color_rgb = [r, g, b]
            
            if not color_rgb:
                enhanced_colors.append(enhanced_color)
                continue
            
            logger.debug(f"Comparing color RGB {color_rgb} with {len(bosch_colors)} Bosch colors")
            
            # Compare with each Bosch color
            best_match = None
            best_distance = float('inf')
            best_normalized_distance = 1.0
            
            for bosch_color in bosch_colors:
                bosch_rgb = bosch_color.get('rgb_values')
                if not bosch_rgb:
                    continue
                
                # Ensure bosch_rgb is a list of 3 integers
                if isinstance(bosch_rgb, (list, tuple)) and len(bosch_rgb) >= 3:
                    bosch_rgb = [int(x) for x in bosch_rgb[:3]]
                else:
                    continue
                
                # Calculate distance
                distance, normalized_distance = calculate_color_distance(color_rgb, bosch_rgb)
                
                # Store match if within reasonable distance (normalized < 0.3)
                if normalized_distance < 0.3:
                    match_info = {
                        'bosch_color': bosch_color,
                        'distance': distance,
                        'normalized_distance': normalized_distance,
                        'similarity_percentage': (1 - normalized_distance) * 100
                    }
                    enhanced_color['bosch_matches'].append(match_info)
                    
                    # Track best match
                    if distance < best_distance:
                        best_distance = distance
                        best_normalized_distance = normalized_distance
                        best_match = match_info
            
            # Set best match
            if best_match:
                enhanced_color['best_bosch_match'] = best_match
                
                # Determine compliance level
                if best_normalized_distance < 0.1:
                    enhanced_color['color_compliance'] = 'exact_match'
                elif best_normalized_distance < 0.2:
                    enhanced_color['color_compliance'] = 'close_match'
                elif best_normalized_distance < 0.3:
                    enhanced_color['color_compliance'] = 'approximate_match'
                else:
                    enhanced_color['color_compliance'] = 'no_match'
            else:
                enhanced_color['color_compliance'] = 'no_match'
            
            enhanced_colors.append(enhanced_color)
        
        return enhanced_colors
        
    except Exception as e:
        logger.error(f"Error comparing colors with Bosch: {e}")
        return extracted_colors

def extract_design_colors_with_bosch_comparison(pdf_path):
    """
    Extract design colors and compare with Bosch colors from database
    Returns enhanced color analysis with Bosch color matches
    """
    try:
        # Extract design colors using existing function
        design_colors_result = extract_design_colors_only(pdf_path)
        
        # Handle different return structures
        if isinstance(design_colors_result, dict):
            # If it's a dict, look for 'colors' key or 'design_colors' key
            if 'colors' in design_colors_result:
                design_colors = design_colors_result['colors']
            elif 'design_colors' in design_colors_result:
                design_colors = design_colors_result['design_colors']
            else:
                # If no 'colors' key, treat the whole dict as colors
                design_colors = [design_colors_result]
        elif isinstance(design_colors_result, list):
            # If it's already a list
            design_colors = design_colors_result
        else:
            # If it's something else, try to convert
            design_colors = []
            if design_colors_result:
                design_colors = [design_colors_result]
        
        # Ensure design_colors is a list of dicts
        if not isinstance(design_colors, list):
            design_colors = [design_colors] if design_colors else []
        
        # Convert to list of dicts if needed and extract RGB values
        processed_colors = []
        for color in design_colors:
            if isinstance(color, dict):
                # Extract RGB values from the color dict
                color_rgb = None
                if 'rgb' in color:
                    color_rgb = color['rgb']
                elif 'corrected_rgb' in color:
                    color_rgb = color['corrected_rgb']
                elif 'hex' in color:
                    # Convert hex to RGB
                    hex_val = color['hex'].replace('#', '')
                    if len(hex_val) == 6:
                        r = int(hex_val[0:2], 16)
                        g = int(hex_val[2:4], 16)
                        b = int(hex_val[4:6], 16)
                        color_rgb = [r, g, b]
                
                if color_rgb:
                    processed_color = color.copy()
                    processed_color['rgb'] = color_rgb
                    processed_colors.append(processed_color)
            else:
                # Convert to dict if it's not already
                processed_colors.append({
                    'name': str(color),
                    'value': color,
                    'type': 'unknown'
                })
        
        logger.info(f"Processed {len(processed_colors)} colors for Bosch comparison")
        
        # Compare with Bosch colors
        enhanced_colors = compare_colors_with_bosch(processed_colors)
        
        # Add summary statistics
        total_colors = len(enhanced_colors)
        exact_matches = len([c for c in enhanced_colors if c.get('color_compliance') == 'exact_match'])
        close_matches = len([c for c in enhanced_colors if c.get('color_compliance') == 'close_match'])
        approximate_matches = len([c for c in enhanced_colors if c.get('color_compliance') == 'approximate_match'])
        no_matches = len([c for c in enhanced_colors if c.get('color_compliance') == 'no_match'])
        
        summary = {
            'total_colors': total_colors,
            'exact_matches': exact_matches,
            'close_matches': close_matches,
            'approximate_matches': approximate_matches,
            'no_matches': no_matches,
            'compliance_rate': ((exact_matches + close_matches) / total_colors * 100) if total_colors > 0 else 0
        }
        
        return {
            'colors': enhanced_colors,
            'summary': summary,
            'analysis_type': 'design_colors_with_bosch_comparison'
        }
        
    except Exception as e:
        logger.error(f"Error in extract_design_colors_with_bosch_comparison: {e}")
        return {
            'colors': [],
            'summary': {},
            'error': str(e),
            'analysis_type': 'design_colors_with_bosch_comparison'
        } 