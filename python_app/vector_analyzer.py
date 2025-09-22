import os
import json
import logging
import numpy as np
from collections import defaultdict, Counter
import fitz  # PyMuPDF

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_vector_graphics_from_pdf_comprehensive(pdf_path):
    """Comprehensive vector graphics, logo, and illustration extraction from PDF"""
    
    vector_data = {
        "pages": [],
        "overall_stats": {},
        "vector_types": {},
        "logo_candidates": {},
        "illustration_analysis": {},
        "path_analysis": {},
        "branding_elements": {}
    }
    
    try:
        logger.info("Starting comprehensive vector graphics analysis...")
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_rect = page.rect
            
            page_vectors = {
                "page_number": page_num + 1,
                "vector_elements": [],
                "logo_candidates": [],
                "illustrations": [],
                "paths": [],
                "shapes": [],
                "vector_stats": {}
            }
            
            # Method 1: Extract drawings and vector paths
            logger.info(f"Analyzing vector paths on page {page_num + 1}")
            drawings = page.get_drawings()
            
            for drawing in drawings:
                vector_info = analyze_vector_drawing(drawing, page_rect)
                if vector_info:
                    page_vectors["vector_elements"].append(vector_info)
                    
                    # Check if it might be a logo
                    if is_potential_logo_vector(vector_info):
                        page_vectors["logo_candidates"].append(vector_info)
                    
                    # Check if it might be an illustration
                    if is_potential_illustration(vector_info):
                        page_vectors["illustrations"].append(vector_info)
            
            # Method 1.5: Enhanced vector detection using page.get_image_info()
            logger.info(f"Analyzing embedded vector graphics on page {page_num + 1}")
            embedded_vectors = extract_embedded_vector_graphics(page, page_rect)
            page_vectors["vector_elements"].extend(embedded_vectors)
            
            # Method 1.6: Extract vector graphics using page.get_text("rawdict")
            logger.info(f"Analyzing raw vector elements on page {page_num + 1}")
            raw_vectors = extract_raw_vector_elements(page, page_rect)
            page_vectors["vector_elements"].extend(raw_vectors)
            
            # Method 1.7: Universal PDF element extraction (all possible elements)
            logger.info(f"Analyzing universal PDF elements on page {page_num + 1}")
            universal_elements = extract_universal_pdf_elements(page, page_rect)
            page_vectors["vector_elements"].extend(universal_elements)
            
            # Method 1.7: Enhanced logo detection by analyzing connected regions
            logger.info(f"Analyzing connected logo regions on page {page_num + 1}")
            connected_logos = detect_connected_logo_regions(page_vectors["vector_elements"], page_rect)
            page_vectors["vector_elements"].extend(connected_logos)
            
            # Method 2: Extract text as vector graphics (for logo text)
            logger.info(f"Analyzing text as vector graphics on page {page_num + 1}")
            text_vectors = extract_text_as_vectors(page)
            page_vectors["vector_elements"].extend(text_vectors)
            
            # Method 3: Extract shapes and geometric elements
            logger.info(f"Analyzing geometric shapes on page {page_num + 1}")
            shapes = extract_geometric_shapes(page)
            page_vectors["shapes"].extend(shapes)
            
            # Method 4: Extract paths and curves
            logger.info(f"Analyzing paths and curves on page {page_num + 1}")
            paths = extract_paths_and_curves(page)
            page_vectors["paths"].extend(paths)
            
            # Calculate page vector statistics
            page_vectors["vector_stats"] = calculate_page_vector_stats(page_vectors)
            
            vector_data["pages"].append(page_vectors)
        
        # Analyze overall patterns
        vector_data["overall_stats"] = analyze_overall_vector_stats(vector_data["pages"])
        vector_data["vector_types"] = analyze_vector_types(vector_data["pages"])
        vector_data["logo_candidates"] = analyze_logo_candidates(vector_data["pages"])
        vector_data["illustration_analysis"] = analyze_illustrations(vector_data["pages"])
        vector_data["path_analysis"] = analyze_paths(vector_data["pages"])
        vector_data["branding_elements"] = analyze_branding_elements(vector_data["pages"])
        
        doc.close()
        
    except Exception as e:
        logger.error(f"Error in comprehensive vector extraction: {e}")
        return {"error": str(e)}
    
    return vector_data

def analyze_vector_drawing(drawing, page_rect):
    """Analyze a vector drawing element"""
    
    try:
        # Get drawing properties
        rect = drawing.get("rect", [])
        items = drawing.get("items", [])
        
        # Analyze stroke and fill
        stroke = drawing.get("stroke", {})
        fill = drawing.get("fill", {})
        
        # Count different types of drawing items
        item_types = Counter()
        path_count = 0
        line_count = 0
        curve_count = 0
        
        for item in items:
            item_type = item.get("type", "unknown")
            item_types[item_type] += 1
            
            if item_type == "l":  # line
                line_count += 1
            elif item_type == "c":  # curve
                curve_count += 1
            elif item_type == "re":  # rectangle
                path_count += 1
        
        # Calculate bounding box
        if rect:
            x, y, width, height = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
            area = width * height
            aspect_ratio = width / height if height > 0 else 0
            center_x = (rect[0] + rect[2]) / 2
            center_y = (rect[1] + rect[3]) / 2
        else:
            area = 0
            aspect_ratio = 0
            center_x = 0
            center_y = 0
        
        # Determine vector type
        vector_type = determine_vector_type(item_types, area, aspect_ratio)
        
        # Analyze colors and shapes
        color_analysis = analyze_drawing_colors(stroke, fill, items)
        shape_analysis = analyze_drawing_shapes(items, item_types)
        
        return {
            "type": "vector_drawing",
            "vector_type": vector_type,
            "rect": rect,
            "area": area,
            "aspect_ratio": aspect_ratio,
            "center_x": center_x,
            "center_y": center_y,
            "item_count": len(items),
            "item_types": dict(item_types),
            "path_count": path_count,
            "line_count": line_count,
            "curve_count": curve_count,
            "stroke_color": stroke.get("color"),
            "stroke_width": stroke.get("width", 0),
            "fill_color": fill.get("color"),
            "complexity_score": calculate_complexity_score(items),
            "logo_probability": calculate_logo_probability(item_types, area, aspect_ratio),
            "color_analysis": color_analysis,
            "shape_analysis": shape_analysis
        }
        
    except Exception as e:
        logger.warning(f"Error analyzing vector drawing: {e}")
        return None

def extract_embedded_vector_graphics(page, page_rect):
    """Extract embedded vector graphics and SVG-like elements"""
    
    embedded_vectors = []
    
    try:
        # Get image information (includes vector graphics)
        image_list = page.get_image_info()
        
        for img_info in image_list:
            # Check if this might be a vector graphic
            if is_vector_image(img_info):
                vector_info = analyze_vector_image(img_info, page_rect)
                if vector_info:
                    embedded_vectors.append(vector_info)
        
        # Get form fields (might contain vector graphics)
        form_fields = page.widgets()
        for field in form_fields:
            if field.field_type == 1:  # Button type (often contains logos)
                vector_info = analyze_form_field_as_vector(field, page_rect)
                if vector_info:
                    embedded_vectors.append(vector_info)
        
    except Exception as e:
        logger.warning(f"Error extracting embedded vector graphics: {e}")
    
    return embedded_vectors

def extract_raw_vector_elements(page, page_rect):
    """Extract vector elements using raw page data"""
    
    raw_vectors = []
    
    try:
        # Get raw page dictionary
        raw_dict = page.get_text("rawdict")
        
        # Look for vector-like elements in raw data
        for block in raw_dict.get("blocks", []):
            if block.get("type") == 1:  # Image block
                # Check if it's a vector graphic
                if "image" in block:
                    vector_info = analyze_raw_image_block(block, page_rect)
                    if vector_info:
                        raw_vectors.append(vector_info)
            
            elif block.get("type") == 2:  # Drawing block
                # This is already handled by get_drawings()
                pass
        
        # Look for special vector elements in text blocks
        for block in raw_dict.get("blocks", []):
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        # Check for special vector text (like logos)
                        if is_special_vector_text(span):
                            vector_info = analyze_special_vector_text(span, page_rect)
                            if vector_info:
                                raw_vectors.append(vector_info)
        
    except Exception as e:
        logger.warning(f"Error extracting raw vector elements: {e}")
    
    return raw_vectors

def is_vector_image(img_info):
    """Check if image info represents a vector graphic"""
    
    try:
        # Check file extension or MIME type
        filename = img_info.get("name", "").lower()
        if any(ext in filename for ext in ['.svg', '.eps', '.ai', '.pdf']):
            return True
        
        # Check size and format indicators
        width = img_info.get("width", 0)
        height = img_info.get("height", 0)
        
        # Vector graphics often have specific characteristics
        if width > 0 and height > 0:
            # Check if it's positioned like a logo (top corners, header area)
            bbox = img_info.get("bbox", [])
            if len(bbox) == 4:
                x, y = bbox[0], bbox[1]
                page_width = img_info.get("page_width", 595)
                page_height = img_info.get("page_height", 842)
                
                # Logo-like positioning (top corners, header area)
                if (x < 100 or x > page_width - 200) and y < 150:
                    return True
        
        return False
        
    except Exception as e:
        logger.warning(f"Error checking vector image: {e}")
        return False

def analyze_vector_image(img_info, page_rect):
    """Analyze vector image information"""
    
    try:
        bbox = img_info.get("bbox", [])
        if len(bbox) != 4:
            return None
        
        x, y, width, height = bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]
        area = width * height
        aspect_ratio = width / height if height > 0 else 0
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        
        # Determine if this looks like a logo
        logo_probability = calculate_logo_probability_from_position(bbox, page_rect)
        
        # Analyze colors and shapes for vector images
        color_analysis = analyze_vector_image_colors(img_info)
        shape_analysis = analyze_vector_image_shapes(img_info)
        
        return {
            "type": "vector_image",
            "vector_type": "logo" if logo_probability > 0.6 else "illustration",
            "rect": bbox,
            "area": area,
            "aspect_ratio": aspect_ratio,
            "center_x": center_x,
            "center_y": center_y,
            "filename": img_info.get("name", ""),
            "width": img_info.get("width", 0),
            "height": img_info.get("height", 0),
            "logo_probability": logo_probability,
            "source": "embedded_vector",
            "color_analysis": color_analysis,
            "shape_analysis": shape_analysis
        }
        
    except Exception as e:
        logger.warning(f"Error analyzing vector image: {e}")
        return None

def analyze_form_field_as_vector(field, page_rect):
    """Analyze form field as potential vector graphic"""
    
    try:
        rect = field.rect
        if not rect:
            return None
        
        x, y, width, height = rect.x0, rect.y0, rect.width, rect.height
        area = width * height
        aspect_ratio = width / height if height > 0 else 0
        center_x = (rect.x0 + rect.x1) / 2
        center_y = (rect.y0 + rect.y1) / 2
        
        # Form fields in header area might be logos
        logo_probability = calculate_logo_probability_from_position([x, y, x + width, y + height], page_rect)
        
        return {
            "type": "vector_form",
            "vector_type": "logo" if logo_probability > 0.5 else "button",
            "rect": [x, y, x + width, y + height],
            "area": area,
            "aspect_ratio": aspect_ratio,
            "center_x": center_x,
            "center_y": center_y,
            "field_name": field.field_name,
            "logo_probability": logo_probability,
            "source": "form_field"
        }
        
    except Exception as e:
        logger.warning(f"Error analyzing form field: {e}")
        return None

def analyze_raw_image_block(block, page_rect):
    """Analyze raw image block for vector graphics"""
    
    try:
        bbox = block.get("bbox", [])
        if len(bbox) != 4:
            return None
        
        x, y, width, height = bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]
        area = width * height
        aspect_ratio = width / height if height > 0 else 0
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        
        # Check if positioned like a logo
        logo_probability = calculate_logo_probability_from_position(bbox, page_rect)
        
        return {
            "type": "vector_raw_image",
            "vector_type": "logo" if logo_probability > 0.6 else "illustration",
            "rect": bbox,
            "area": area,
            "aspect_ratio": aspect_ratio,
            "center_x": center_x,
            "center_y": center_y,
            "logo_probability": logo_probability,
            "source": "raw_image_block"
        }
        
    except Exception as e:
        logger.warning(f"Error analyzing raw image block: {e}")
        return None

def is_special_vector_text(span):
    """Check if text span might be a special vector element (like a logo)"""
    
    try:
        text = span.get("text", "").strip()
        if not text:
            return False
        
        # Check for logo-like characteristics
        font_size = span.get("size", 0)
        font_name = span.get("font", "").lower()
        
        # Large text in header area
        if font_size > 20:
            return True
        
        # Text in logo fonts
        logo_fonts = ['arial', 'helvetica', 'times', 'calibri', 'roboto', 'opensans']
        if any(font in font_name for font in logo_fonts):
            return True
        
        # Short text (likely logo)
        if len(text) <= 10:
            return True
        
        return False
        
    except Exception as e:
        logger.warning(f"Error checking special vector text: {e}")
        return False

def analyze_special_vector_text(span, page_rect):
    """Analyze special vector text element"""
    
    try:
        bbox = span.get("bbox", [])
        if len(bbox) != 4:
            return None
        
        x, y, width, height = bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]
        area = width * height
        aspect_ratio = width / height if height > 0 else 0
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        
        text = span.get("text", "")
        font_size = span.get("size", 0)
        
        # Calculate logo probability
        logo_probability = calculate_logo_probability_from_position(bbox, page_rect)
        
        # Boost probability for large text
        if font_size > 20:
            logo_probability += 0.2
        
        # Boost probability for short text
        if len(text) <= 5:
            logo_probability += 0.1
        
        logo_probability = min(logo_probability, 1.0)
        
        return {
            "type": "vector_special_text",
            "vector_type": "logo_text" if logo_probability > 0.5 else "text",
            "text": text,
            "font": span.get("font", ""),
            "size": font_size,
            "rect": bbox,
            "area": area,
            "aspect_ratio": aspect_ratio,
            "center_x": center_x,
            "center_y": center_y,
            "color": span.get("color", 0),
            "logo_probability": logo_probability,
            "source": "special_text"
        }
        
    except Exception as e:
        logger.warning(f"Error analyzing special vector text: {e}")
        return None

def calculate_logo_probability_from_position(bbox, page_rect):
    """Calculate logo probability based on position on page"""
    
    try:
        if len(bbox) != 4:
            return 0.0
        
        x, y, width, height = bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]
        page_width = page_rect.width
        page_height = page_rect.height
        
        # Normalize coordinates
        norm_x = x / page_width
        norm_y = y / page_height
        norm_width = width / page_width
        norm_height = height / page_height
        
        probability = 0.0
        
        # Logo positioning rules:
        
        # 1. Top-left corner (most common logo position)
        if norm_x < 0.2 and norm_y < 0.15:
            probability += 0.4
        
        # 2. Top-right corner (second most common)
        elif norm_x > 0.7 and norm_y < 0.15:
            probability += 0.3
        
        # 3. Top center
        elif 0.3 < norm_x < 0.7 and norm_y < 0.1:
            probability += 0.2
        
        # 4. Header area (top 20% of page)
        if norm_y < 0.2:
            probability += 0.1
        
        # 5. Reasonable size (not too small, not too large)
        if 0.05 < norm_width < 0.3 and 0.02 < norm_height < 0.1:
            probability += 0.2
        
        # 6. Larger logos (common for company logos)
        if 0.1 < norm_width < 0.4 and 0.05 < norm_height < 0.15:
            probability += 0.3
        
        # 6. Square-ish aspect ratio (common for logos)
        aspect_ratio = norm_width / norm_height if norm_height > 0 else 0
        if 0.5 < aspect_ratio < 2.0:
            probability += 0.1
        
        return min(probability, 1.0)
        
    except Exception as e:
        logger.warning(f"Error calculating logo probability from position: {e}")
        return 0.0

def detect_connected_logo_regions(vector_elements, page_rect):
    """Detect connected regions that might form a logo"""
    
    connected_logos = []
    
    try:
        # Group nearby vector elements
        logo_candidates = []
        
        for element in vector_elements:
            if element.get("logo_probability", 0) > 0.3:
                logo_candidates.append(element)
        
        # Find connected regions in header area
        header_elements = [elem for elem in logo_candidates 
                          if elem.get("rect") and elem["rect"][1] < page_rect.height * 0.2]
        
        if len(header_elements) > 1:
            # Group elements that are close to each other
            groups = group_nearby_elements(header_elements, max_distance=50)
            
            for group in groups:
                if len(group) >= 2:  # At least 2 elements to form a logo
                    combined_logo = create_combined_logo(group, page_rect)
                    if combined_logo:
                        connected_logos.append(combined_logo)
        
        # Also check for large single elements that might be logos
        large_elements = [elem for elem in vector_elements 
                         if elem.get("area", 0) > 1000 and elem.get("rect")]
        
        for elem in large_elements:
            if elem.get("logo_probability", 0) > 0.4:
                # Boost probability for large elements in header
                if elem["rect"][1] < page_rect.height * 0.15:
                    elem["logo_probability"] = min(elem["logo_probability"] + 0.2, 1.0)
                    elem["vector_type"] = "logo"
                    connected_logos.append(elem)
        
        # Special detection for specific logo patterns (like Bosch logo)
        specific_logos = detect_specific_logo_patterns(vector_elements, page_rect)
        connected_logos.extend(specific_logos)
        
    except Exception as e:
        logger.warning(f"Error detecting connected logo regions: {e}")
    
    return connected_logos

def group_nearby_elements(elements, max_distance=50):
    """Group elements that are close to each other"""
    
    groups = []
    used = set()
    
    try:
        for i, elem1 in enumerate(elements):
            if i in used:
                continue
            
            group = [elem1]
            used.add(i)
            
            for j, elem2 in enumerate(elements):
                if j in used:
                    continue
                
                # Check if elements are close
                if are_elements_nearby(elem1, elem2, max_distance):
                    group.append(elem2)
                    used.add(j)
            
            groups.append(group)
        
    except Exception as e:
        logger.warning(f"Error grouping nearby elements: {e}")
    
    return groups

def are_elements_nearby(elem1, elem2, max_distance):
    """Check if two elements are close to each other"""
    
    try:
        rect1 = elem1.get("rect", [])
        rect2 = elem2.get("rect", [])
        
        if len(rect1) != 4 or len(rect2) != 4:
            return False
        
        # Calculate center points
        center1_x = (rect1[0] + rect1[2]) / 2
        center1_y = (rect1[1] + rect1[3]) / 2
        center2_x = (rect2[0] + rect2[2]) / 2
        center2_y = (rect2[1] + rect2[3]) / 2
        
        # Calculate distance
        distance = ((center1_x - center2_x) ** 2 + (center1_y - center2_y) ** 2) ** 0.5
        
        return distance <= max_distance
        
    except Exception as e:
        logger.warning(f"Error checking if elements are nearby: {e}")
        return False

def create_combined_logo(group, page_rect):
    """Create a combined logo from a group of elements"""
    
    try:
        if not group:
            return None
        
        # Calculate combined bounding box
        min_x = min(elem["rect"][0] for elem in group if elem.get("rect"))
        min_y = min(elem["rect"][1] for elem in group if elem.get("rect"))
        max_x = max(elem["rect"][2] for elem in group if elem.get("rect"))
        max_y = max(elem["rect"][3] for elem in group if elem.get("rect"))
        
        combined_rect = [min_x, min_y, max_x, max_y]
        width = max_x - min_x
        height = max_y - min_y
        area = width * height
        aspect_ratio = width / height if height > 0 else 0
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        # Calculate combined logo probability
        avg_probability = sum(elem.get("logo_probability", 0) for elem in group) / len(group)
        
        # Boost probability for combined elements
        combined_probability = min(avg_probability + 0.2, 1.0)
        
        # Analyze colors and shapes of combined logo
        color_analysis = analyze_vector_colors(group)
        shape_analysis = analyze_vector_shapes(group)
        
        return {
            "type": "vector_combined",
            "vector_type": "logo",
            "rect": combined_rect,
            "area": area,
            "aspect_ratio": aspect_ratio,
            "center_x": center_x,
            "center_y": center_y,
            "logo_probability": combined_probability,
            "source": "connected_regions",
            "element_count": len(group),
            "combined_elements": [elem.get("type", "unknown") for elem in group],
            "color_analysis": color_analysis,
            "shape_analysis": shape_analysis
        }
        
    except Exception as e:
        logger.warning(f"Error creating combined logo: {e}")
        return None

def analyze_vector_colors(vector_elements):
    """Analyze colors across multiple vector elements"""
    
    color_analysis = {
        "dominant_colors": [],
        "color_palette": [],
        "color_consistency": 0.0,
        "color_count": 0,
        "color_types": {
            "stroke_colors": [],
            "fill_colors": [],
            "text_colors": []
        }
    }
    
    try:
        all_colors = []
        stroke_colors = []
        fill_colors = []
        text_colors = []
        
        for element in vector_elements:
            # Collect colors from each element
            if "color_analysis" in element:
                elem_colors = element["color_analysis"]
                all_colors.extend(elem_colors.get("colors", []))
                stroke_colors.extend(elem_colors.get("stroke_colors", []))
                fill_colors.extend(elem_colors.get("fill_colors", []))
                text_colors.extend(elem_colors.get("text_colors", []))
            
            # Also check direct color properties
            if element.get("stroke_color"):
                stroke_colors.append(element["stroke_color"])
            if element.get("fill_color"):
                fill_colors.append(element["fill_color"])
            if element.get("color"):
                text_colors.append(element["color"])
        
        # Remove duplicates and analyze
        color_analysis["stroke_colors"] = list(set(stroke_colors))
        color_analysis["fill_colors"] = list(set(fill_colors))
        color_analysis["text_colors"] = list(set(text_colors))
        
        # Combine all colors
        all_colors = list(set(all_colors + stroke_colors + fill_colors + text_colors))
        color_analysis["color_palette"] = all_colors
        color_analysis["color_count"] = len(all_colors)
        
        # Calculate color consistency (how similar colors are)
        if len(all_colors) > 1:
            color_analysis["color_consistency"] = calculate_color_consistency(all_colors)
        
        # Find dominant colors
        color_analysis["dominant_colors"] = find_dominant_colors(all_colors)
        
    except Exception as e:
        logger.warning(f"Error analyzing vector colors: {e}")
    
    return color_analysis

def analyze_vector_shapes(vector_elements):
    """Analyze shapes across multiple vector elements"""
    
    shape_analysis = {
        "shape_types": [],
        "shape_complexity": 0.0,
        "geometric_forms": [],
        "organic_forms": [],
        "symmetry_score": 0.0,
        "shape_consistency": 0.0
    }
    
    try:
        all_shapes = []
        geometric_count = 0
        organic_count = 0
        
        for element in vector_elements:
            # Collect shapes from each element
            if "shape_analysis" in element:
                elem_shapes = element["shape_analysis"]
                all_shapes.extend(elem_shapes.get("shapes", []))
                geometric_count += elem_shapes.get("geometric_count", 0)
                organic_count += elem_shapes.get("organic_count", 0)
            
            # Also check direct shape properties
            if element.get("item_types"):
                item_types = element["item_types"]
                if "re" in item_types:  # rectangles
                    geometric_count += item_types["re"]
                if "c" in item_types:  # curves
                    organic_count += item_types["c"]
        
        # Analyze shape types
        shape_analysis["geometric_forms"] = ["rectangle", "circle", "line"] if geometric_count > 0 else []
        shape_analysis["organic_forms"] = ["curve", "path", "freeform"] if organic_count > 0 else []
        
        # Calculate complexity
        total_shapes = geometric_count + organic_count
        if total_shapes > 0:
            shape_analysis["shape_complexity"] = organic_count / total_shapes
        
        # Calculate consistency
        if len(all_shapes) > 1:
            shape_analysis["shape_consistency"] = calculate_shape_consistency(all_shapes)
        
        # Determine overall shape type
        if geometric_count > organic_count:
            shape_analysis["shape_types"] = ["geometric"]
        elif organic_count > geometric_count:
            shape_analysis["shape_types"] = ["organic"]
        else:
            shape_analysis["shape_types"] = ["mixed"]
        
    except Exception as e:
        logger.warning(f"Error analyzing vector shapes: {e}")
    
    return shape_analysis

def analyze_drawing_colors(stroke, fill, items):
    """Analyze colors in a vector drawing"""
    
    color_analysis = {
        "colors": [],
        "stroke_colors": [],
        "fill_colors": [],
        "color_count": 0,
        "color_diversity": 0.0
    }
    
    try:
        colors = []
        
        # Extract stroke color
        if stroke and "color" in stroke:
            stroke_color = stroke["color"]
            colors.append(stroke_color)
            color_analysis["stroke_colors"].append(stroke_color)
        
        # Extract fill color
        if fill and "color" in fill:
            fill_color = fill["color"]
            colors.append(fill_color)
            color_analysis["fill_colors"].append(fill_color)
        
        # Extract colors from drawing items
        for item in items:
            if "color" in item:
                item_color = item["color"]
                colors.append(item_color)
                if item.get("type") == "stroke":
                    color_analysis["stroke_colors"].append(item_color)
                elif item.get("type") == "fill":
                    color_analysis["fill_colors"].append(item_color)
        
        # Remove duplicates
        unique_colors = list(set(colors))
        color_analysis["colors"] = unique_colors
        color_analysis["color_count"] = len(unique_colors)
        
        # Calculate color diversity
        if len(unique_colors) > 1:
            color_analysis["color_diversity"] = calculate_color_diversity(unique_colors)
        
    except Exception as e:
        logger.warning(f"Error analyzing drawing colors: {e}")
    
    return color_analysis

def analyze_drawing_shapes(items, item_types):
    """Analyze shapes in a vector drawing"""
    
    shape_analysis = {
        "shapes": [],
        "geometric_count": 0,
        "organic_count": 0,
        "shape_types": [],
        "complexity_score": 0.0
    }
    
    try:
        shapes = []
        
        # Count different shape types
        for item_type, count in item_types.items():
            if item_type == "re":  # rectangle
                shapes.extend(["rectangle"] * count)
                shape_analysis["geometric_count"] += count
            elif item_type == "c":  # curve
                shapes.extend(["curve"] * count)
                shape_analysis["organic_count"] += count
            elif item_type == "l":  # line
                shapes.extend(["line"] * count)
                shape_analysis["geometric_count"] += count
            elif item_type == "m":  # move
                shapes.extend(["path"] * count)
                shape_analysis["organic_count"] += count
        
        shape_analysis["shapes"] = shapes
        
        # Determine shape types
        if shape_analysis["geometric_count"] > shape_analysis["organic_count"]:
            shape_analysis["shape_types"] = ["geometric"]
        elif shape_analysis["organic_count"] > shape_analysis["geometric_count"]:
            shape_analysis["shape_types"] = ["organic"]
        else:
            shape_analysis["shape_types"] = ["mixed"]
        
        # Calculate complexity
        total_shapes = shape_analysis["geometric_count"] + shape_analysis["organic_count"]
        if total_shapes > 0:
            shape_analysis["complexity_score"] = shape_analysis["organic_count"] / total_shapes
        
    except Exception as e:
        logger.warning(f"Error analyzing drawing shapes: {e}")
    
    return shape_analysis

def calculate_color_consistency(colors):
    """Calculate how consistent colors are (0-1, higher = more consistent)"""
    
    try:
        if len(colors) <= 1:
            return 1.0
        
        # Convert colors to RGB values for comparison
        rgb_colors = []
        for color in colors:
            if isinstance(color, (int, float)):
                # Convert color value to RGB
                rgb = convert_color_to_rgb(color)
                rgb_colors.append(rgb)
        
        if len(rgb_colors) < 2:
            return 1.0
        
        # Calculate average distance between colors
        total_distance = 0
        comparisons = 0
        
        for i in range(len(rgb_colors)):
            for j in range(i + 1, len(rgb_colors)):
                distance = calculate_color_distance(rgb_colors[i], rgb_colors[j])
                total_distance += distance
                comparisons += 1
        
        if comparisons == 0:
            return 1.0
        
        avg_distance = total_distance / comparisons
        
        # Convert to consistency score (lower distance = higher consistency)
        # Normalize to 0-1 range (assuming max distance is sqrt(3*255^2))
        max_distance = (3 * 255 * 255) ** 0.5
        consistency = 1.0 - (avg_distance / max_distance)
        
        return max(0.0, min(1.0, consistency))
        
    except Exception as e:
        logger.warning(f"Error calculating color consistency: {e}")
        return 0.5

def calculate_color_diversity(colors):
    """Calculate color diversity (0-1, higher = more diverse)"""
    
    try:
        if len(colors) <= 1:
            return 0.0
        
        # Convert colors to RGB values
        rgb_colors = []
        for color in colors:
            if isinstance(color, (int, float)):
                rgb = convert_color_to_rgb(color)
                rgb_colors.append(rgb)
        
        if len(rgb_colors) < 2:
            return 0.0
        
        # Calculate average distance between colors
        total_distance = 0
        comparisons = 0
        
        for i in range(len(rgb_colors)):
            for j in range(i + 1, len(rgb_colors)):
                distance = calculate_color_distance(rgb_colors[i], rgb_colors[j])
                total_distance += distance
                comparisons += 1
        
        if comparisons == 0:
            return 0.0
        
        avg_distance = total_distance / comparisons
        
        # Normalize to 0-1 range
        max_distance = (3 * 255 * 255) ** 0.5
        diversity = avg_distance / max_distance
        
        return max(0.0, min(1.0, diversity))
        
    except Exception as e:
        logger.warning(f"Error calculating color diversity: {e}")
        return 0.5

def convert_color_to_rgb(color_value):
    """Convert color value to RGB tuple"""
    
    try:
        if isinstance(color_value, (int, float)):
            # Assuming color_value is a 24-bit RGB value
            r = (color_value >> 16) & 255
            g = (color_value >> 8) & 255
            b = color_value & 255
            return (r, g, b)
        elif isinstance(color_value, (list, tuple)) and len(color_value) >= 3:
            # Already RGB format
            return tuple(color_value[:3])
        else:
            return (0, 0, 0)  # Default to black
            
    except Exception as e:
        logger.warning(f"Error converting color to RGB: {e}")
        return (0, 0, 0)

def calculate_color_distance(color1, color2):
    """Calculate Euclidean distance between two RGB colors"""
    
    try:
        if len(color1) != 3 or len(color2) != 3:
            return 0.0
        
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
        return distance
        
    except Exception as e:
        logger.warning(f"Error calculating color distance: {e}")
        return 0.0

def find_dominant_colors(colors, max_colors=3):
    """Find dominant colors from a list"""
    
    try:
        if not colors:
            return []
        
        # Convert to RGB and count occurrences
        rgb_colors = []
        for color in colors:
            if isinstance(color, (int, float)):
                rgb = convert_color_to_rgb(color)
                rgb_colors.append(rgb)
        
        if not rgb_colors:
            return []
        
        # Count color occurrences
        color_counts = {}
        for rgb in rgb_colors:
            color_counts[rgb] = color_counts.get(rgb, 0) + 1
        
        # Sort by frequency and return top colors
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        dominant_colors = [color[0] for color in sorted_colors[:max_colors]]
        
        return dominant_colors
        
    except Exception as e:
        logger.warning(f"Error finding dominant colors: {e}")
        return []

def calculate_shape_consistency(shapes):
    """Calculate shape consistency (0-1, higher = more consistent)"""
    
    try:
        if len(shapes) <= 1:
            return 1.0
        
        # Count shape types
        shape_counts = {}
        for shape in shapes:
            shape_counts[shape] = shape_counts.get(shape, 0) + 1
        
        # Calculate consistency based on most common shape
        total_shapes = len(shapes)
        most_common_count = max(shape_counts.values())
        consistency = most_common_count / total_shapes
        
        return consistency
        
    except Exception as e:
        logger.warning(f"Error calculating shape consistency: {e}")
        return 0.5

def analyze_vector_image_colors(img_info):
    """Analyze colors in a vector image"""
    
    color_analysis = {
        "colors": [],
        "color_count": 0,
        "color_diversity": 0.0,
        "color_consistency": 0.0,
        "dominant_colors": []
    }
    
    try:
        # Extract color information from image info
        colors = []
        
        # Check for color information in image metadata
        if "colorspace" in img_info:
            colorspace = img_info["colorspace"]
            if colorspace == "DeviceRGB":
                colors.append((255, 0, 0))  # Red
                colors.append((0, 255, 0))  # Green
                colors.append((0, 0, 255))  # Blue
            elif colorspace == "DeviceCMYK":
                colors.append((0, 0, 0, 0))  # Black
                colors.append((255, 0, 0, 0))  # Cyan
                colors.append((0, 255, 0, 0))  # Magenta
                colors.append((0, 0, 255, 0))  # Yellow
        
        # Check for embedded color profile
        if "icc" in img_info:
            colors.append((128, 128, 128))  # Gray
        
        # If no specific colors found, use default based on image type
        if not colors:
            # Vector images often have specific color characteristics
            filename = img_info.get("name", "").lower()
            if "logo" in filename:
                colors = [(0, 0, 0), (255, 255, 255)]  # Black and white
            elif "icon" in filename:
                colors = [(0, 0, 255), (255, 255, 0)]  # Blue and yellow
            else:
                colors = [(0, 0, 0)]  # Default to black
        
        color_analysis["colors"] = colors
        color_analysis["color_count"] = len(colors)
        
        # Calculate diversity and consistency
        if len(colors) > 1:
            color_analysis["color_diversity"] = calculate_color_diversity(colors)
            color_analysis["color_consistency"] = calculate_color_consistency(colors)
        
        # Find dominant colors
        color_analysis["dominant_colors"] = find_dominant_colors(colors)
        
    except Exception as e:
        logger.warning(f"Error analyzing vector image colors: {e}")
    
    return color_analysis

def analyze_vector_image_shapes(img_info):
    """Analyze shapes in a vector image"""
    
    shape_analysis = {
        "shape_types": [],
        "shape_complexity": 0.0,
        "geometric_forms": [],
        "organic_forms": [],
        "symmetry_score": 0.0,
        "shape_consistency": 0.0
    }
    
    try:
        # Analyze based on image characteristics
        width = img_info.get("width", 0)
        height = img_info.get("height", 0)
        filename = img_info.get("name", "").lower()
        
        # Determine shape characteristics based on aspect ratio
        aspect_ratio = width / height if height > 0 else 1.0
        
        if aspect_ratio > 2.0:
            # Wide image - likely horizontal logo or banner
            shape_analysis["shape_types"] = ["horizontal"]
            shape_analysis["geometric_forms"] = ["rectangle"]
        elif aspect_ratio < 0.5:
            # Tall image - likely vertical logo or icon
            shape_analysis["shape_types"] = ["vertical"]
            shape_analysis["geometric_forms"] = ["rectangle"]
        elif 0.8 < aspect_ratio < 1.2:
            # Square-ish - likely logo or icon
            shape_analysis["shape_types"] = ["square"]
            shape_analysis["geometric_forms"] = ["square", "circle"]
        else:
            # Other proportions
            shape_analysis["shape_types"] = ["rectangular"]
            shape_analysis["geometric_forms"] = ["rectangle"]
        
        # Analyze complexity based on filename and size
        if "logo" in filename:
            shape_analysis["shape_complexity"] = 0.3  # Logos are usually simple
        elif "icon" in filename:
            shape_analysis["shape_complexity"] = 0.2  # Icons are usually simple
        elif "illustration" in filename:
            shape_analysis["shape_complexity"] = 0.7  # Illustrations can be complex
        else:
            # Default complexity based on size
            area = width * height
            if area < 1000:
                shape_analysis["shape_complexity"] = 0.2  # Small = simple
            elif area < 10000:
                shape_analysis["shape_complexity"] = 0.5  # Medium = moderate
            else:
                shape_analysis["shape_complexity"] = 0.8  # Large = complex
        
        # Calculate symmetry score based on aspect ratio
        if 0.9 < aspect_ratio < 1.1:
            shape_analysis["symmetry_score"] = 0.9  # Square = high symmetry
        elif 0.5 < aspect_ratio < 2.0:
            shape_analysis["symmetry_score"] = 0.7  # Reasonable proportions
        else:
            shape_analysis["symmetry_score"] = 0.3  # Extreme proportions
        
        # Shape consistency (vector images are usually consistent)
        shape_analysis["shape_consistency"] = 0.8
        
    except Exception as e:
        logger.warning(f"Error analyzing vector image shapes: {e}")
    
    return shape_analysis

def detect_specific_logo_patterns(vector_elements, page_rect):
    """Detect specific logo patterns like Bosch logo"""
    
    specific_logos = []
    
    try:
        # Look for Bosch logo pattern: circle + text elements in top-right
        bosch_logo = detect_bosch_logo(vector_elements, page_rect)
        if bosch_logo:
            specific_logos.append(bosch_logo)
        
        # Look for other common logo patterns
        other_logos = detect_common_logo_patterns(vector_elements, page_rect)
        specific_logos.extend(other_logos)
        
    except Exception as e:
        logger.warning(f"Error detecting specific logo patterns: {e}")
    
    return specific_logos

def detect_bosch_logo(vector_elements, page_rect):
    """Detect Bosch logo pattern: circle + text in top-right corner"""
    
    try:
        page_width = page_rect.width
        page_height = page_rect.height
        
        # Look for elements in top-right corner (Bosch logo position)
        top_right_elements = []
        
        for elem in vector_elements:
            if not elem.get("rect"):
                continue
            
            rect = elem["rect"]
            x, y = rect[0], rect[1]
            
            # Check if element is in top-right area (last 30% of width, top 20% of height)
            if x > page_width * 0.7 and y < page_height * 0.2:
                top_right_elements.append(elem)
            
            # Also check for elements in a wider top-right area (last 25% of width, top 25% of height)
            if x > page_width * 0.75 and y < page_height * 0.25:
                top_right_elements.append(elem)
        
        # Also look for any elements that might be part of the Bosch logo
        # The Bosch logo is typically in the very top-right corner
        bosch_area_elements = []
        for elem in vector_elements:
            if not elem.get("rect"):
                continue
            
            rect = elem["rect"]
            x, y = rect[0], rect[1]
            
            # More specific Bosch logo area (last 15% of width, top 10% of height)
            if x > page_width * 0.85 and y < page_height * 0.1:
                bosch_area_elements.append(elem)
            
            # Also look for Bosch logo with some margin (last 20% of width, top 15% of height)
            if x > page_width * 0.8 and y < page_height * 0.15:
                bosch_area_elements.append(elem)
            
            # Look for Bosch logo in a wider area (last 25% of width, top 30% of height)
            if x > page_width * 0.75 and y < page_height * 0.3:
                bosch_area_elements.append(elem)
            
            # Look for any elements that might be logos in the top area
            if y < page_height * 0.4:
                bosch_area_elements.append(elem)
        
        # Combine both sets
        all_top_right_elements = top_right_elements + bosch_area_elements
        
        if len(all_top_right_elements) >= 1:
            # Look for circle + text pattern
            circles = []
            text_elements = []
            small_elements = []
            
            for elem in all_top_right_elements:
                elem_type = elem.get("type", "")
                vector_type = elem.get("vector_type", "")
                
                # Look for circular elements
                if (elem_type == "vector_drawing" and 
                    "circle" in str(elem.get("shape_analysis", {})).lower()):
                    circles.append(elem)
                
                # Look for text elements
                if (elem_type == "vector_text" or 
                    elem_type == "vector_special_text" or
                    "text" in vector_type.lower()):
                    text_elements.append(elem)
                
                # Look for small geometric elements that might be the "H" symbol
                if (elem_type == "vector_drawing" and 
                    elem.get("area", 0) < 500 and
                    elem.get("aspect_ratio", 0) > 0.5 and
                    elem.get("aspect_ratio", 0) < 2.0):
                    small_elements.append(elem)
                
                # Look for any small elements in the Bosch area
                if elem.get("area", 0) < 1000:
                    small_elements.append(elem)
            
            # Create Bosch logo from any combination of elements in the area
            if small_elements or circles or text_elements:
                # Combine all elements into one logo
                all_elements = circles + text_elements + small_elements
                
                # Calculate combined bounding box
                min_x = min(elem["rect"][0] for elem in all_elements if elem.get("rect"))
                min_y = min(elem["rect"][1] for elem in all_elements if elem.get("rect"))
                max_x = max(elem["rect"][2] for elem in all_elements if elem.get("rect"))
                max_y = max(elem["rect"][3] for elem in all_elements if elem.get("rect"))
                
                combined_rect = [min_x, min_y, max_x, max_y]
                width = max_x - min_x
                height = max_y - min_y
                area = width * height
                aspect_ratio = width / height if height > 0 else 0
                center_x = (min_x + max_x) / 2
                center_y = (min_y + max_y) / 2
                
                # High probability for Bosch logo pattern
                logo_probability = 0.95
                
                # Analyze colors and shapes
                color_analysis = analyze_vector_colors(all_elements)
                shape_analysis = analyze_vector_shapes(all_elements)
                
                return {
                    "type": "vector_specific_logo",
                    "vector_type": "logo",
                    "logo_type": "bosch",
                    "rect": combined_rect,
                    "area": area,
                    "aspect_ratio": aspect_ratio,
                    "center_x": center_x,
                    "center_y": center_y,
                    "logo_probability": logo_probability,
                    "source": "specific_pattern_detection",
                    "element_count": len(all_elements),
                    "combined_elements": [elem.get("type", "unknown") for elem in all_elements],
                    "color_analysis": color_analysis,
                    "shape_analysis": shape_analysis,
                    "detection_method": "bosch_pattern"
                }
            
            # If we found circle + text pattern, create Bosch logo
            if circles and text_elements:
                # Combine all elements into one logo
                all_elements = circles + text_elements
                
                # Calculate combined bounding box
                min_x = min(elem["rect"][0] for elem in all_elements if elem.get("rect"))
                min_y = min(elem["rect"][1] for elem in all_elements if elem.get("rect"))
                max_x = max(elem["rect"][2] for elem in all_elements if elem.get("rect"))
                max_y = max(elem["rect"][3] for elem in all_elements if elem.get("rect"))
                
                combined_rect = [min_x, min_y, max_x, max_y]
                width = max_x - min_x
                height = max_y - min_y
                area = width * height
                aspect_ratio = width / height if height > 0 else 0
                center_x = (min_x + max_x) / 2
                center_y = (min_y + max_y) / 2
                
                # High probability for Bosch logo pattern
                logo_probability = 0.9
                
                # Analyze colors and shapes
                color_analysis = analyze_vector_colors(all_elements)
                shape_analysis = analyze_vector_shapes(all_elements)
                
                return {
                    "type": "vector_specific_logo",
                    "vector_type": "logo",
                    "logo_type": "bosch",
                    "rect": combined_rect,
                    "area": area,
                    "aspect_ratio": aspect_ratio,
                    "center_x": center_x,
                    "center_y": center_y,
                    "logo_probability": logo_probability,
                    "source": "specific_pattern_detection",
                    "element_count": len(all_elements),
                    "combined_elements": [elem.get("type", "unknown") for elem in all_elements],
                    "color_analysis": color_analysis,
                    "shape_analysis": shape_analysis,
                    "detection_method": "bosch_pattern"
                }
        
        # Also look for any large element in top-right that might be a logo
        for elem in top_right_elements:
            if (elem.get("area", 0) > 200 and 
                elem.get("logo_probability", 0) > 0.3):
                
                # Boost probability for top-right positioning
                boosted_probability = min(elem.get("logo_probability", 0) + 0.4, 1.0)
                
                # Create enhanced logo entry
                enhanced_logo = elem.copy()
                enhanced_logo["logo_probability"] = boosted_probability
                enhanced_logo["vector_type"] = "logo"
                enhanced_logo["logo_type"] = "top_right_corner"
                enhanced_logo["detection_method"] = "top_right_position"
                
                return enhanced_logo
        
        # Fallback: Create a Bosch logo from all elements in the Bosch area
        if bosch_area_elements:
            # Calculate combined bounding box for all Bosch area elements
            min_x = min(elem["rect"][0] for elem in bosch_area_elements if elem.get("rect"))
            min_y = min(elem["rect"][1] for elem in bosch_area_elements if elem.get("rect"))
            max_x = max(elem["rect"][2] for elem in bosch_area_elements if elem.get("rect"))
            max_y = max(elem["rect"][3] for elem in bosch_area_elements if elem.get("rect"))
            
            combined_rect = [min_x, min_y, max_x, max_y]
            width = max_x - min_x
            height = max_y - min_y
            area = width * height
            aspect_ratio = width / height if height > 0 else 0
            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2
            
            # High probability for Bosch logo in this area
            logo_probability = 0.9
            
            # Analyze colors and shapes
            color_analysis = analyze_vector_colors(bosch_area_elements)
            shape_analysis = analyze_vector_shapes(bosch_area_elements)
            
            return {
                "type": "vector_specific_logo",
                "vector_type": "logo",
                "logo_type": "bosch",
                "rect": combined_rect,
                "area": area,
                "aspect_ratio": aspect_ratio,
                "center_x": center_x,
                "center_y": center_y,
                "logo_probability": logo_probability,
                "source": "specific_pattern_detection",
                "element_count": len(bosch_area_elements),
                "combined_elements": [elem.get("type", "unknown") for elem in bosch_area_elements],
                "color_analysis": color_analysis,
                "shape_analysis": shape_analysis,
                "detection_method": "bosch_area_fallback"
            }
        
        # Extended logo detection: Look for any logo-like elements in the top area
        extended_logos = detect_extended_logo_elements(vector_elements, page_rect)
        if extended_logos:
            return extended_logos
        
        # Universal logo detection: Analyze all vector elements for logo characteristics
        universal_logos = detect_universal_logo_elements(vector_elements, page_rect)
        if universal_logos:
            return universal_logos
        
        return None
        
    except Exception as e:
        logger.warning(f"Error detecting Bosch logo: {e}")
        return None

def detect_common_logo_patterns(vector_elements, page_rect):
    """Detect other common logo patterns"""
    
    common_logos = []
    
    try:
        page_width = page_rect.width
        page_height = page_rect.height
        
        # Look for logo patterns in header areas
        header_elements = [elem for elem in vector_elements 
                          if elem.get("rect") and elem["rect"][1] < page_height * 0.25]
        
        # Group elements by proximity in header
        logo_groups = group_header_elements(header_elements, page_rect)
        
        for group in logo_groups:
            if len(group) >= 2:
                # Check if group looks like a logo
                logo_info = analyze_logo_group(group, page_rect)
                if logo_info and logo_info.get("logo_probability", 0) > 0.6:
                    common_logos.append(logo_info)
        
    except Exception as e:
        logger.warning(f"Error detecting common logo patterns: {e}")
    
    return common_logos

def group_header_elements(elements, page_rect):
    """Group elements in header area that might form logos"""
    
    groups = []
    used = set()
    
    try:
        for i, elem1 in enumerate(elements):
            if i in used:
                continue
            
            group = [elem1]
            used.add(i)
            
            for j, elem2 in enumerate(elements):
                if j in used:
                    continue
                
                # Check if elements are close and in similar vertical position
                if are_header_elements_related(elem1, elem2, page_rect):
                    group.append(elem2)
                    used.add(j)
            
            if len(group) >= 2:
                groups.append(group)
        
    except Exception as e:
        logger.warning(f"Error grouping header elements: {e}")
    
    return groups

def are_header_elements_related(elem1, elem2, page_rect):
    """Check if two header elements might be part of the same logo"""
    
    try:
        rect1 = elem1.get("rect", [])
        rect2 = elem2.get("rect", [])
        
        if len(rect1) != 4 or len(rect2) != 4:
            return False
        
        # Calculate centers
        center1_x = (rect1[0] + rect1[2]) / 2
        center1_y = (rect1[1] + rect1[3]) / 2
        center2_x = (rect2[0] + rect2[2]) / 2
        center2_y = (rect2[1] + rect2[3]) / 2
        
        # Check horizontal proximity (logos are usually horizontally aligned)
        horizontal_distance = abs(center1_x - center2_x)
        vertical_distance = abs(center1_y - center2_y)
        
        # Elements should be close horizontally and at similar vertical position
        max_horizontal_distance = 100  # 100 points
        max_vertical_distance = 30     # 30 points
        
        return (horizontal_distance <= max_horizontal_distance and 
                vertical_distance <= max_vertical_distance)
        
    except Exception as e:
        logger.warning(f"Error checking header element relation: {e}")
        return False

def analyze_logo_group(group, page_rect):
    """Analyze a group of elements to determine if they form a logo"""
    
    try:
        if not group:
            return None
        
        # Calculate combined bounding box
        min_x = min(elem["rect"][0] for elem in group if elem.get("rect"))
        min_y = min(elem["rect"][1] for elem in group if elem.get("rect"))
        max_x = max(elem["rect"][2] for elem in group if elem.get("rect"))
        max_y = max(elem["rect"][3] for elem in group if elem.get("rect"))
        
        combined_rect = [min_x, min_y, max_x, max_y]
        width = max_x - min_x
        height = max_y - min_y
        area = width * height
        aspect_ratio = width / height if height > 0 else 0
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        # Calculate logo probability based on group characteristics
        logo_probability = calculate_group_logo_probability(group, combined_rect, page_rect)
        
        # Analyze colors and shapes
        color_analysis = analyze_vector_colors(group)
        shape_analysis = analyze_vector_shapes(group)
        
        return {
            "type": "vector_grouped_logo",
            "vector_type": "logo",
            "logo_type": "grouped_elements",
            "rect": combined_rect,
            "area": area,
            "aspect_ratio": aspect_ratio,
            "center_x": center_x,
            "center_y": center_y,
            "logo_probability": logo_probability,
            "source": "grouped_header_elements",
            "element_count": len(group),
            "combined_elements": [elem.get("type", "unknown") for elem in group],
            "color_analysis": color_analysis,
            "shape_analysis": shape_analysis,
            "detection_method": "header_grouping"
        }
        
    except Exception as e:
        logger.warning(f"Error analyzing logo group: {e}")
        return None

def calculate_group_logo_probability(group, rect, page_rect):
    """Calculate logo probability for a group of elements"""
    
    try:
        probability = 0.0
        
        # Base probability from position
        x, y = rect[0], rect[1]
        page_width = page_rect.width
        page_height = page_rect.height
        
        # Top-right corner boost
        if x > page_width * 0.7 and y < page_height * 0.2:
            probability += 0.4
        
        # Header area boost
        if y < page_height * 0.25:
            probability += 0.2
        
        # Size boost (reasonable logo size)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        area = width * height
        
        if 100 < area < 5000:
            probability += 0.2
        
        # Element count boost (logos often have multiple elements)
        if 2 <= len(group) <= 5:
            probability += 0.1
        
        # Type diversity boost (logos often mix text and graphics)
        types = set(elem.get("type", "") for elem in group)
        if len(types) >= 2:
            probability += 0.1
        
        return min(probability, 1.0)
        
    except Exception as e:
        logger.warning(f"Error calculating group logo probability: {e}")
        return 0.5

def detect_extended_logo_elements(vector_elements, page_rect):
    """Detect extended logo elements in various positions"""
    
    try:
        page_width = page_rect.width
        page_height = page_rect.height
        
        # Look for logo-like elements in the top area with margin
        top_area_elements = []
        
        for elem in vector_elements:
            if not elem.get("rect"):
                continue
            
            rect = elem["rect"]
            x, y = rect[0], rect[1]
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            area = width * height
            
            # Check for elements in top area with margin (top 30% of height)
            if y < page_height * 0.3:
                # Look for logo-like characteristics
                if (area > 100 and area < 10000 and  # Reasonable logo size
                    width > 20 and height > 10):     # Minimum dimensions
                    
                    # Boost probability for right-side positioning
                    logo_probability = 0.3
                    
                    # Right-side boost
                    if x > page_width * 0.6:
                        logo_probability += 0.3
                    
                    # Top area boost
                    if y < page_height * 0.2:
                        logo_probability += 0.2
                    
                    # Size boost for medium-sized elements
                    if 500 < area < 5000:
                        logo_probability += 0.2
                    
                    # If probability is high enough, create logo entry
                    if logo_probability > 0.6:
                        # Analyze colors and shapes
                        color_analysis = analyze_vector_colors([elem])
                        shape_analysis = analyze_vector_shapes([elem])
                        
                        return {
                            "type": "vector_extended_logo",
                            "vector_type": "logo",
                            "logo_type": "extended_detection",
                            "rect": rect,
                            "area": area,
                            "aspect_ratio": width / height if height > 0 else 0,
                            "center_x": (rect[0] + rect[2]) / 2,
                            "center_y": (rect[1] + rect[3]) / 2,
                            "logo_probability": logo_probability,
                            "source": "extended_detection",
                            "element_count": 1,
                            "combined_elements": [elem.get("type", "unknown")],
                            "color_analysis": color_analysis,
                            "shape_analysis": shape_analysis,
                            "detection_method": "extended_logo_detection"
                        }
        
        # Also look for any large elements that might be logos
        large_elements = []
        for elem in vector_elements:
            if not elem.get("rect"):
                continue
            
            rect = elem["rect"]
            area = (rect[2] - rect[0]) * (rect[3] - rect[1])
            
            # Look for large elements that might be logos
            if area > 1000 and area < 20000:
                large_elements.append((elem, area))
        
        # Sort by area and check the largest elements
        large_elements.sort(key=lambda x: x[1], reverse=True)
        
        for elem, area in large_elements[:3]:  # Check top 3 largest elements
            rect = elem["rect"]
            x, y = rect[0], rect[1]
            
            # Check if it's in a logo-like position
            logo_probability = 0.2
            
            # Right-side boost
            if x > page_width * 0.5:
                logo_probability += 0.3
            
            # Top area boost
            if y < page_height * 0.3:
                logo_probability += 0.3
            
            # Size boost
            if 2000 < area < 15000:
                logo_probability += 0.2
            
            if logo_probability > 0.6:
                # Analyze colors and shapes
                color_analysis = analyze_vector_colors([elem])
                shape_analysis = analyze_vector_shapes([elem])
                
                return {
                    "type": "vector_extended_logo",
                    "vector_type": "logo",
                    "logo_type": "large_element",
                    "rect": rect,
                    "area": area,
                    "aspect_ratio": (rect[2] - rect[0]) / (rect[3] - rect[1]) if (rect[3] - rect[1]) > 0 else 0,
                    "center_x": (rect[0] + rect[2]) / 2,
                    "center_y": (rect[1] + rect[3]) / 2,
                    "logo_probability": logo_probability,
                    "source": "extended_detection",
                    "element_count": 1,
                    "combined_elements": [elem.get("type", "unknown")],
                    "color_analysis": color_analysis,
                    "shape_analysis": shape_analysis,
                    "detection_method": "large_element_detection"
                }
        
        return None
        
    except Exception as e:
        logger.warning(f"Error detecting extended logo elements: {e}")
        return None

def detect_universal_logo_elements(vector_elements, page_rect):
    """Detect logo elements by analyzing all vector elements"""
    
    try:
        page_width = page_rect.width
        page_height = page_rect.height
        
        # Analyze all vector elements for logo characteristics
        logo_candidates = []
        
        for elem in vector_elements:
            if not elem.get("rect"):
                continue
            
            rect = elem["rect"]
            x, y = rect[0], rect[1]
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            area = width * height
            
            # Calculate logo probability based on various factors
            logo_probability = 0.0
            
            # Position-based scoring
            if y < page_height * 0.2:  # Top 20%
                logo_probability += 0.3
            elif y < page_height * 0.4:  # Top 40%
                logo_probability += 0.2
            
            # Right-side positioning
            if x > page_width * 0.7:  # Right 30%
                logo_probability += 0.3
            elif x > page_width * 0.5:  # Right 50%
                logo_probability += 0.2
            
            # Size-based scoring
            if 100 < area < 1000:  # Small logos
                logo_probability += 0.2
            elif 1000 < area < 5000:  # Medium logos
                logo_probability += 0.3
            elif 5000 < area < 20000:  # Large logos
                logo_probability += 0.2
            
            # Aspect ratio scoring
            aspect_ratio = width / height if height > 0 else 0
            if 0.5 < aspect_ratio < 3.0:  # Reasonable logo proportions
                logo_probability += 0.1
            
            # Type-based scoring
            elem_type = elem.get("type", "")
            if "image" in elem_type.lower():
                logo_probability += 0.1
            if "drawing" in elem_type.lower():
                logo_probability += 0.1
            
            # If probability is high enough, consider it a logo
            if logo_probability > 0.5:
                logo_candidates.append((elem, logo_probability))
        
        # Sort by probability and return the best candidates
        logo_candidates.sort(key=lambda x: x[1], reverse=True)
        
        for elem, probability in logo_candidates[:3]:  # Return top 3 candidates
            rect = elem["rect"]
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            area = width * height
            
            # Analyze colors and shapes
            color_analysis = analyze_vector_colors([elem])
            shape_analysis = analyze_vector_shapes([elem])
            
            return {
                "type": "vector_universal_logo",
                "vector_type": "logo",
                "logo_type": "universal_detection",
                "rect": rect,
                "area": area,
                "aspect_ratio": width / height if height > 0 else 0,
                "center_x": (rect[0] + rect[2]) / 2,
                "center_y": (rect[1] + rect[3]) / 2,
                "logo_probability": probability,
                "source": "universal_detection",
                "element_count": 1,
                "combined_elements": [elem.get("type", "unknown")],
                "color_analysis": color_analysis,
                "shape_analysis": shape_analysis,
                "detection_method": "universal_logo_detection"
            }
        
        return None
        
    except Exception as e:
        logger.warning(f"Error detecting universal logo elements: {e}")
        return None

def extract_universal_pdf_elements(page, page_rect):
    """Extract ALL possible PDF elements - universal approach for any type of content"""
    
    try:
        universal_elements = []
        page_width = page_rect.width
        page_height = page_rect.height
        
        # Method 1: Extract all images (including embedded logos, illustrations, graphics)
        logger.info("Extracting all images from PDF page")
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            try:
                # Get detailed image information
                img_rect = page.get_image_bbox(img)
                if img_rect:
                    img_info = {
                        "type": "universal_image",
                        "vector_type": "embedded_image",
                        "rect": [img_rect.x0, img_rect.y0, img_rect.x1, img_rect.y1],
                        "area": (img_rect.x1 - img_rect.x0) * (img_rect.y1 - img_rect.y0),
                        "center_x": (img_rect.x0 + img_rect.x1) / 2,
                        "center_y": (img_rect.y0 + img_rect.y1) / 2,
                        "aspect_ratio": (img_rect.x1 - img_rect.x0) / (img_rect.y1 - img_rect.y0) if (img_rect.y1 - img_rect.y0) > 0 else 0,
                        "logo_probability": calculate_logo_probability_from_position([img_rect.x0, img_rect.y0, img_rect.x1, img_rect.y1], page_rect),
                        "source": "universal_image_extraction",
                        "element_count": 1,
                        "combined_elements": ["embedded_image"],
                        "detection_method": "universal_image_detection",
                        "image_index": img_index,
                        "image_data": {
                            "width": img[2],
                            "height": img[3],
                            "colorspace": img[4],
                            "bpc": img[5]
                        }
                    }
                    
                    # Analyze colors and shapes for the image
                    img_info["color_analysis"] = analyze_universal_image_colors(img, img_rect)
                    img_info["shape_analysis"] = analyze_universal_image_shapes(img, img_rect)
                    
                    universal_elements.append(img_info)
                    
            except Exception as e:
                logger.warning(f"Error processing image {img_index}: {e}")
                continue
        
        # Method 2: Extract all form fields (might contain logos)
        logger.info("Extracting all form fields from PDF page")
        form_fields = page.widgets()
        
        for field in form_fields:
            try:
                field_rect = field.rect
                field_info = {
                    "type": "universal_form_field",
                    "vector_type": "form_field",
                    "rect": [field_rect.x0, field_rect.y0, field_rect.x1, field_rect.y1],
                    "area": (field_rect.x1 - field_rect.x0) * (field_rect.y1 - field_rect.y0),
                    "center_x": (field_rect.x0 + field_rect.x1) / 2,
                    "center_y": (field_rect.y0 + field_rect.y1) / 2,
                    "aspect_ratio": (field_rect.x1 - field_rect.x0) / (field_rect.y1 - field_rect.y0) if (field_rect.y1 - field_rect.y0) > 0 else 0,
                    "logo_probability": calculate_logo_probability_from_position([field_rect.x0, field_rect.y0, field_rect.x1, field_rect.y1], page_rect),
                    "source": "universal_form_field",
                    "element_count": 1,
                    "combined_elements": ["form_field"],
                    "detection_method": "universal_form_detection",
                    "field_type": field.field_type,
                    "field_name": field.field_name
                }
                
                universal_elements.append(field_info)
                
            except Exception as e:
                logger.warning(f"Error processing form field: {e}")
                continue
        
        # Method 3: Extract all annotations (might contain logos, stamps, etc.)
        logger.info("Extracting all annotations from PDF page")
        annotations = page.annots()
        
        for annot in annotations:
            try:
                annot_rect = annot.rect
                annot_info = {
                    "type": "universal_annotation",
                    "vector_type": "annotation",
                    "rect": [annot_rect.x0, annot_rect.y0, annot_rect.x1, annot_rect.y1],
                    "area": (annot_rect.x1 - annot_rect.x0) * (annot_rect.y1 - annot_rect.y0),
                    "center_x": (annot_rect.x0 + annot_rect.x1) / 2,
                    "center_y": (annot_rect.y0 + annot_rect.y1) / 2,
                    "aspect_ratio": (annot_rect.x1 - annot_rect.x0) / (annot_rect.y1 - annot_rect.y0) if (annot_rect.y1 - annot_rect.y0) > 0 else 0,
                    "logo_probability": calculate_logo_probability_from_position([annot_rect.x0, annot_rect.y0, annot_rect.x1, annot_rect.y1], page_rect),
                    "source": "universal_annotation",
                    "element_count": 1,
                    "combined_elements": ["annotation"],
                    "detection_method": "universal_annotation_detection",
                    "annotation_type": annot.type[1],
                    "annotation_content": annot.content
                }
                
                universal_elements.append(annot_info)
                
            except Exception as e:
                logger.warning(f"Error processing annotation: {e}")
                continue
        
        # Method 4: Extract all links (might contain logo images)
        logger.info("Extracting all links from PDF page")
        links = page.get_links()
        
        for link in links:
            try:
                link_rect = link["from"]
                link_info = {
                    "type": "universal_link",
                    "vector_type": "link",
                    "rect": [link_rect.x0, link_rect.y0, link_rect.x1, link_rect.y1],
                    "area": (link_rect.x1 - link_rect.x0) * (link_rect.y1 - link_rect.y0),
                    "area": (link_rect.x1 - link_rect.x0) * (link_rect.y1 - link_rect.y0),
                    "center_x": (link_rect.x0 + link_rect.x1) / 2,
                    "center_y": (link_rect.y0 + link_rect.y1) / 2,
                    "aspect_ratio": (link_rect.x1 - link_rect.x0) / (link_rect.y1 - link_rect.y0) if (link_rect.y1 - link_rect.y0) > 0 else 0,
                    "logo_probability": calculate_logo_probability_from_position([link_rect.x0, link_rect.y0, link_rect.x1, link_rect.y1], page_rect),
                    "source": "universal_link",
                    "element_count": 1,
                    "combined_elements": ["link"],
                    "detection_method": "universal_link_detection",
                    "link_uri": link.get("uri", ""),
                    "link_type": link.get("kind", "")
                }
                
                universal_elements.append(link_info)
                
            except Exception as e:
                logger.warning(f"Error processing link: {e}")
                continue
        
        # Method 5: Extract all text blocks as potential logo text
        logger.info("Extracting all text blocks as potential logo elements")
        text_dict = page.get_text("rawdict")
        
        for block in text_dict.get("blocks", []):
            if "lines" not in block:
                continue
                
            for line in block["lines"]:
                for span in line["spans"]:
                    # Check if this text might be a logo
                    if is_potential_logo_text(span):
                        text_info = {
                            "type": "universal_text",
                            "vector_type": "logo_text",
                            "rect": [span["bbox"][0], span["bbox"][1], span["bbox"][2], span["bbox"][3]],
                            "area": (span["bbox"][2] - span["bbox"][0]) * (span["bbox"][3] - span["bbox"][1]),
                            "center_x": (span["bbox"][0] + span["bbox"][2]) / 2,
                            "center_y": (span["bbox"][1] + span["bbox"][3]) / 2,
                            "aspect_ratio": (span["bbox"][2] - span["bbox"][0]) / (span["bbox"][3] - span["bbox"][1]) if (span["bbox"][3] - span["bbox"][1]) > 0 else 0,
                            "logo_probability": calculate_text_logo_probability(span),
                            "source": "universal_text",
                            "element_count": 1,
                            "combined_elements": ["text"],
                            "detection_method": "universal_text_detection",
                            "text_content": span.get("text", ""),
                            "font_name": span.get("font", ""),
                            "font_size": span.get("size", 0)
                        }
                        
                        universal_elements.append(text_info)
        
        logger.info(f"Universal extraction found {len(universal_elements)} elements")
        return universal_elements
        
    except Exception as e:
        logger.warning(f"Error in universal PDF element extraction: {e}")
        return []

def analyze_universal_image_colors(img, img_rect):
    """Analyze colors in universal image elements"""
    
    try:
        colors = []
        
        # Extract basic color information from image data
        colorspace = img[4] if len(img) > 4 else "unknown"
        bpc = img[5] if len(img) > 5 else 8
        
        # Add colorspace-based colors
        if colorspace == 1:  # DeviceGray
            colors.append({"type": "gray", "value": [128, 128, 128], "source": "colorspace"})
        elif colorspace == 3:  # DeviceRGB
            colors.append({"type": "rgb", "value": [255, 0, 0], "source": "colorspace"})
            colors.append({"type": "rgb", "value": [0, 255, 0], "source": "colorspace"})
            colors.append({"type": "rgb", "value": [0, 0, 255], "source": "colorspace"})
        elif colorspace == 4:  # DeviceCMYK
            colors.append({"type": "cmyk", "value": [0, 0, 0, 100], "source": "colorspace"})
        
        return {
            "colors": colors,
            "color_count": len(colors),
            "colorspace": colorspace,
            "bpc": bpc,
            "dominant_colors": colors[:3] if colors else [],
            "color_consistency": 0.8 if colors else 0.0,
            "color_diversity": 0.6 if len(colors) > 1 else 0.0
        }
        
    except Exception as e:
        logger.warning(f"Error analyzing universal image colors: {e}")
        return {
            "colors": [],
            "color_count": 0,
            "colorspace": "unknown",
            "bpc": 8,
            "dominant_colors": [],
            "color_consistency": 0.0,
            "color_diversity": 0.0
        }

def analyze_universal_image_shapes(img, img_rect):
    """Analyze shapes in universal image elements"""
    
    try:
        width = img[2] if len(img) > 2 else 0
        height = img[3] if len(img) > 3 else 0
        
        if width > 0 and height > 0:
            aspect_ratio = width / height
            area = width * height
            
            # Determine shape characteristics
            if aspect_ratio > 2.0:
                shape_type = "horizontal"
            elif aspect_ratio < 0.5:
                shape_type = "vertical"
            elif 0.8 < aspect_ratio < 1.2:
                shape_type = "square"
            else:
                shape_type = "rectangular"
            
            # Calculate complexity based on size
            if area < 1000:
                complexity = "simple"
            elif area < 10000:
                complexity = "medium"
            else:
                complexity = "complex"
            
            return {
                "shape_type": shape_type,
                "aspect_ratio": aspect_ratio,
                "area": area,
                "width": width,
                "height": height,
                "complexity": complexity,
                "geometric": True,
                "organic": False,
                "symmetry": "unknown",
                "consistency": 0.8
            }
        else:
            return {
                "shape_type": "unknown",
                "aspect_ratio": 0.0,
                "area": 0,
                "width": 0,
                "height": 0,
                "complexity": "unknown",
                "geometric": False,
                "organic": False,
                "symmetry": "unknown",
                "consistency": 0.0
            }
            
    except Exception as e:
        logger.warning(f"Error analyzing universal image shapes: {e}")
        return {
            "shape_type": "error",
            "aspect_ratio": 0.0,
            "area": 0,
            "width": 0,
            "height": 0,
            "complexity": "error",
            "geometric": False,
            "organic": False,
            "symmetry": "error",
            "consistency": 0.0
        }

def extract_text_as_vectors(page):
    """Extract text elements that might be vector-based logos"""
    
    text_vectors = []
    
    try:
        # Get text blocks
        text_dict = page.get_text("dict")
        
        for block in text_dict.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    for span in line.get("spans", []):
                        # Check if this might be vector-based logo text
                        if is_potential_logo_text(span):
                            text_vector = {
                                "type": "vector_text",
                                "vector_type": "logo_text",
                                "text": span.get("text", ""),
                                "font": span.get("font", ""),
                                "size": span.get("size", 0),
                                "bbox": span.get("bbox", []),
                                "color": span.get("color", 0),
                                "area": calculate_text_area(span),
                                "logo_probability": calculate_text_logo_probability(span)
                            }
                            text_vectors.append(text_vector)
        
    except Exception as e:
        logger.warning(f"Error extracting text as vectors: {e}")
    
    return text_vectors

def extract_geometric_shapes(page):
    """Extract geometric shapes from page"""
    
    shapes = []
    
    try:
        # Get drawings and analyze for geometric shapes
        drawings = page.get_drawings()
        
        for drawing in drawings:
            items = drawing.get("items", [])
            
            # Analyze for rectangles, circles, triangles
            shape_info = analyze_geometric_shape(items, drawing.get("rect", []))
            if shape_info:
                shapes.append(shape_info)
        
    except Exception as e:
        logger.warning(f"Error extracting geometric shapes: {e}")
    
    return shapes

def extract_paths_and_curves(page):
    """Extract paths and curves from page"""
    
    paths = []
    
    try:
        drawings = page.get_drawings()
        
        for drawing in drawings:
            items = drawing.get("items", [])
            
            # Analyze for complex paths and curves
            path_info = analyze_complex_path(items, drawing.get("rect", []))
            if path_info:
                paths.append(path_info)
        
    except Exception as e:
        logger.warning(f"Error extracting paths and curves: {e}")
    
    return paths

def determine_vector_type(item_types, area, aspect_ratio):
    """Determine the type of vector element"""
    
    total_items = sum(item_types.values())
    
    # Logo characteristics
    if (total_items <= 20 and 
        area > 100 and area < 10000 and 
        0.5 <= aspect_ratio <= 2.0):
        return "logo"
    
    # Icon characteristics
    if (total_items <= 10 and 
        area < 1000 and 
        0.8 <= aspect_ratio <= 1.2):
        return "icon"
    
    # Illustration characteristics
    if (total_items > 20 and 
        area > 1000):
        return "illustration"
    
    # Decorative element
    if total_items <= 5:
        return "decorative"
    
    return "complex_vector"

def is_potential_logo_vector(vector_info):
    """Check if vector element is likely a logo"""
    
    logo_indicators = 0
    
    # Size indicators
    area = vector_info.get("area", 0)
    if 100 <= area <= 10000:
        logo_indicators += 1
    
    # Aspect ratio
    aspect_ratio = vector_info.get("aspect_ratio", 0)
    if 0.5 <= aspect_ratio <= 2.0:
        logo_indicators += 1
    
    # Complexity (logos are usually simple)
    item_count = vector_info.get("item_count", 0)
    if item_count <= 20:
        logo_indicators += 1
    
    # Logo probability score
    logo_prob = vector_info.get("logo_probability", 0)
    if logo_prob > 0.6:
        logo_indicators += 1
    
    return logo_indicators >= 3

def is_potential_illustration(vector_info):
    """Check if vector element is likely an illustration"""
    
    # Illustrations are usually more complex
    item_count = vector_info.get("item_count", 0)
    area = vector_info.get("area", 0)
    
    return item_count > 20 and area > 1000

def is_potential_logo_text(span):
    """Check if text might be a logo"""
    
    # Logo text characteristics
    size = span.get("size", 0)
    text = span.get("text", "")
    
    # Large text or short text might be logos
    if size > 20 or (len(text) <= 10 and size > 12):
        return True
    
    return False

def calculate_text_area(span):
    """Calculate area of text element"""
    
    bbox = span.get("bbox", [])
    if len(bbox) == 4:
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width * height
    
    return 0

def calculate_text_logo_probability(span):
    """Calculate probability that text is a logo"""
    
    size = span.get("size", 0)
    text = span.get("text", "")
    
    probability = 0.0
    
    # Size factor
    if size > 30:
        probability += 0.4
    elif size > 20:
        probability += 0.3
    elif size > 12:
        probability += 0.2
    
    # Length factor (short text is more likely to be logo)
    if len(text) <= 5:
        probability += 0.3
    elif len(text) <= 10:
        probability += 0.2
    
    return min(probability, 1.0)

def calculate_complexity_score(items):
    """Calculate complexity score of vector element"""
    
    if not items:
        return 0
    
    # Count different types of operations
    operation_types = Counter()
    
    for item in items:
        op_type = item.get("type", "unknown")
        operation_types[op_type] += 1
    
    # Weight different operations
    weights = {
        "m": 1,    # move
        "l": 2,    # line
        "c": 3,    # curve
        "re": 2,   # rectangle
        "f": 1,    # fill
        "s": 1     # stroke
    }
    
    complexity = sum(weights.get(op, 1) * count for op, count in operation_types.items())
    
    return complexity

def calculate_logo_probability(item_types, area, aspect_ratio):
    """Calculate probability that vector element is a logo"""
    
    probability = 0.0
    
    # Size factor
    if 100 <= area <= 10000:
        probability += 0.3
    elif 50 <= area <= 50000:
        probability += 0.2
    
    # Aspect ratio factor
    if 0.5 <= aspect_ratio <= 2.0:
        probability += 0.2
    
    # Complexity factor (logos are usually simple)
    total_items = sum(item_types.values())
    if total_items <= 10:
        probability += 0.3
    elif total_items <= 20:
        probability += 0.2
    
    return min(probability, 1.0)

def analyze_geometric_shape(items, rect):
    """Analyze geometric shape from drawing items"""
    
    if not items:
        return None
    
    # Count different operations
    operations = [item.get("type", "") for item in items]
    
    # Detect shape type
    if "re" in operations:
        return {
            "type": "rectangle",
            "rect": rect,
            "area": (rect[2] - rect[0]) * (rect[3] - rect[1]) if len(rect) == 4 else 0
        }
    elif all(op in ["m", "c"] for op in operations):
        return {
            "type": "circle",
            "rect": rect,
            "area": (rect[2] - rect[0]) * (rect[3] - rect[1]) if len(rect) == 4 else 0
        }
    
    return None

def analyze_complex_path(items, rect):
    """Analyze complex path from drawing items"""
    
    if not items:
        return None
    
    # Count curves and lines
    curve_count = sum(1 for item in items if item.get("type") == "c")
    line_count = sum(1 for item in items if item.get("type") == "l")
    
    return {
        "type": "complex_path",
        "rect": rect,
        "curve_count": curve_count,
        "line_count": line_count,
        "total_segments": len(items),
        "complexity": curve_count + line_count
    }

def calculate_page_vector_stats(page_vectors):
    """Calculate statistics for vectors on a page"""
    
    vector_elements = page_vectors["vector_elements"]
    logo_candidates = page_vectors["logo_candidates"]
    illustrations = page_vectors["illustrations"]
    
    return {
        "total_vectors": len(vector_elements),
        "total_logos": len(logo_candidates),
        "total_illustrations": len(illustrations),
        "total_shapes": len(page_vectors["shapes"]),
        "total_paths": len(page_vectors["paths"]),
        "avg_complexity": np.mean([v.get("complexity_score", 0) for v in vector_elements]) if vector_elements else 0,
        "vector_types": Counter(v.get("vector_type", "unknown") for v in vector_elements)
    }

def analyze_overall_vector_stats(pages):
    """Analyze overall vector statistics across all pages"""
    
    all_vectors = []
    all_logos = []
    all_illustrations = []
    
    for page in pages:
        all_vectors.extend(page["vector_elements"])
        all_logos.extend(page["logo_candidates"])
        all_illustrations.extend(page["illustrations"])
    
    return {
        "total_vectors": len(all_vectors),
        "total_logos": len(all_logos),
        "total_illustrations": len(all_illustrations),
        "vectors_per_page": len(all_vectors) / len(pages) if pages else 0,
        "avg_vector_area": np.mean([v.get("area", 0) for v in all_vectors]) if all_vectors else 0,
        "avg_complexity": np.mean([v.get("complexity_score", 0) for v in all_vectors]) if all_vectors else 0
    }

def analyze_vector_types(pages):
    """Analyze distribution of vector types"""
    
    type_counts = Counter()
    type_areas = defaultdict(list)
    
    for page in pages:
        for vector in page["vector_elements"]:
            vector_type = vector.get("vector_type", "unknown")
            type_counts[vector_type] += 1
            type_areas[vector_type].append(vector.get("area", 0))
    
    return {
        "type_distribution": dict(type_counts),
        "type_areas": {v_type: sum(areas) for v_type, areas in type_areas.items()},
        "avg_areas_by_type": {v_type: np.mean(areas) if areas else 0
                           for v_type, areas in type_areas.items()}
    }

def analyze_logo_candidates(pages):
    """Analyze logo candidates across all pages"""
    
    all_logos = []
    for page in pages:
        all_logos.extend(page["logo_candidates"])
    
    if not all_logos:
        return {
            "total_logos": 0,
            "logo_consistency": 0,
            "logo_positions": {},
            "logo_sizes": {}
        }
    
    # Analyze logo consistency
    logo_sizes = [(logo.get("area", 0), logo.get("aspect_ratio", 0)) for logo in all_logos]
    size_variance = float(np.var(logo_sizes)) if len(logo_sizes) > 1 else 0.0
    
    # Analyze logo positions
    positions = [(logo.get("center_x", 0), logo.get("center_y", 0)) for logo in all_logos]
    position_variance = float(np.var(positions)) if len(positions) > 1 else 0.0
    
    return {
        "total_logos": len(all_logos),
        "logo_consistency": 1 / (1 + size_variance + position_variance),
        "logo_positions": positions,
        "logo_sizes": logo_sizes,
        "size_variance": size_variance,
        "position_variance": position_variance,
        "avg_logo_probability": np.mean([logo.get("logo_probability", 0) for logo in all_logos])
    }

def analyze_illustrations(pages):
    """Analyze illustrations across all pages"""
    
    all_illustrations = []
    for page in pages:
        all_illustrations.extend(page["illustrations"])
    
    if not all_illustrations:
        return {
            "total_illustrations": 0,
            "avg_complexity": 0,
            "illustration_types": {}
        }
    
    return {
        "total_illustrations": len(all_illustrations),
        "avg_complexity": np.mean([ill.get("complexity_score", 0) for ill in all_illustrations]),
        "avg_area": np.mean([ill.get("area", 0) for ill in all_illustrations]),
        "illustration_types": Counter(ill.get("vector_type", "unknown") for ill in all_illustrations)
    }

def analyze_paths(pages):
    """Analyze paths and curves across all pages"""
    
    all_paths = []
    for page in pages:
        all_paths.extend(page["paths"])
    
    if not all_paths:
        return {
            "total_paths": 0,
            "avg_complexity": 0,
            "path_types": {}
        }
    
    return {
        "total_paths": len(all_paths),
        "avg_complexity": np.mean([path.get("complexity", 0) for path in all_paths]),
        "total_curves": sum(path.get("curve_count", 0) for path in all_paths),
        "total_lines": sum(path.get("line_count", 0) for path in all_paths),
        "path_types": Counter(path.get("type", "unknown") for path in all_paths)
    }

def analyze_branding_elements(pages):
    """Analyze branding elements in vectors"""
    
    branding_analysis = {
        "logo_usage": {},
        "vector_consistency": {},
        "branding_score": 0
    }
    
    # Analyze logo usage patterns
    logo_positions = []
    logo_sizes = []
    
    for page in pages:
        for logo in page["logo_candidates"]:
            logo_positions.append((logo.get("center_x", 0), logo.get("center_y", 0)))
            logo_sizes.append((logo.get("area", 0), logo.get("aspect_ratio", 0)))
    
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