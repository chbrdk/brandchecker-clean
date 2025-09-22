import os
import re
import json
import logging
import numpy as np
from collections import defaultdict, Counter
import tempfile
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_layout_from_pdf_comprehensive(pdf_path):
    """Comprehensive layout extraction from PDF using multiple methods"""
    
    # Import libraries here to avoid import issues
    import fitz  # PyMuPDF
    import pdfplumber
    
    layout_data = {
        "pages": [],
        "overall_stats": {},
        "layout_patterns": {},
        "spacing_analysis": {},
        "alignment_analysis": {},
        "grid_system": {},
        "visual_hierarchy": {}
    }
    
    try:
        # Method 1: PyMuPDF for overall page structure
        logger.info("Starting PyMuPDF layout analysis...")
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_rect = page.rect
            
            page_layout = {
                "page_number": page_num + 1,
                "dimensions": {
                    "width": page_rect.width,
                    "height": page_rect.height,
                    "aspect_ratio": page_rect.width / page_rect.height
                },
                "text_blocks": [],
                "images": [],
                "shapes": [],
                "margins": {},
                "columns": [],
                "headers": [],
                "footers": []
            }
            
            # Get text blocks with positioning
            text_dict = page.get_text("dict")
            
            for block in text_dict.get("blocks", []):
                if "lines" in block:
                    block_bbox = block.get("bbox", [0, 0, 0, 0])
                    block_text = ""
                    
                    for line in block["lines"]:
                        line_bbox = line.get("bbox", [0, 0, 0, 0])
                        line_text = ""
                        
                        for span in line.get("spans", []):
                            span_text = span.get("text", "")
                            line_text += span_text
                            
                            # Analyze individual spans for positioning
                            span_bbox = span.get("bbox", [0, 0, 0, 0])
                            span_info = {
                                "text": span_text,
                                "bbox": span_bbox,
                                "font": span.get("font", ""),
                                "size": span.get("size", 0),
                                "color": span.get("color", 0),
                                "x": span_bbox[0],
                                "y": span_bbox[1],
                                "width": span_bbox[2] - span_bbox[0],
                                "height": span_bbox[3] - span_bbox[1]
                            }
                        
                        block_text += line_text + "\n"
                        
                        # Analyze line positioning
                        line_info = {
                            "text": line_text,
                            "bbox": line_bbox,
                            "x": line_bbox[0],
                            "y": line_bbox[1],
                            "width": line_bbox[2] - line_bbox[0],
                            "height": line_bbox[3] - line_bbox[1],
                            "center_x": (line_bbox[0] + line_bbox[2]) / 2,
                            "center_y": (line_bbox[1] + line_bbox[3]) / 2
                        }
                    
                    # Analyze block positioning
                    block_info = {
                        "text": block_text.strip(),
                        "bbox": block_bbox,
                        "x": block_bbox[0],
                        "y": block_bbox[1],
                        "width": block_bbox[2] - block_bbox[0],
                        "height": block_bbox[3] - block_bbox[1],
                        "center_x": (block_bbox[0] + block_bbox[2]) / 2,
                        "center_y": (block_bbox[1] + block_bbox[3]) / 2,
                        "lines": [line_info for line in block["lines"]]
                    }
                    
                    page_layout["text_blocks"].append(block_info)
            
            # Calculate margins based on text block positions
            if page_layout["text_blocks"]:
                left_margins = [block["x"] for block in page_layout["text_blocks"]]
                right_margins = [page_rect.width - (block["x"] + block["width"]) for block in page_layout["text_blocks"]]
                top_margins = [block["y"] for block in page_layout["text_blocks"]]
                bottom_margins = [page_rect.height - (block["y"] + block["height"]) for block in page_layout["text_blocks"]]
                
                page_layout["margins"] = {
                    "left": min(left_margins) if left_margins else 0,
                    "right": min(right_margins) if right_margins else 0,
                    "top": min(top_margins) if top_margins else 0,
                    "bottom": min(bottom_margins) if bottom_margins else 0
                }
            
            layout_data["pages"].append(page_layout)
        
        doc.close()
        
        # Method 2: pdfplumber for detailed layout analysis
        logger.info("Starting pdfplumber layout analysis...")
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_layout = layout_data["pages"][page_num]
                
                # Get page dimensions
                page_width = page.width
                page_height = page.height
                
                # Analyze text positioning and alignment
                chars = page.chars
                words = page.extract_words()
                
                # Group characters by lines
                lines = defaultdict(list)
                for char in chars:
                    y_pos = round(char["y0"], 2)
                    lines[y_pos].append(char)
                
                # Analyze line alignment
                line_alignments = []
                for y_pos, line_chars in lines.items():
                    if line_chars:
                        x_positions = [char["x0"] for char in line_chars]
                        line_width = max(char["x1"] for char in line_chars) - min(char["x0"] for char in line_chars)
                        
                        # Determine alignment
                        left_x = min(x_positions)
                        right_x = max(char["x1"] for char in line_chars)
                        center_x = (left_x + right_x) / 2
                        
                        # Check if centered (within 10% of page center)
                        page_center = page_width / 2
                        is_centered = abs(center_x - page_center) < (page_width * 0.1)
                        
                        # Check if left-aligned (within 5% of left margin)
                        left_margin = page_layout["margins"]["left"]
                        is_left_aligned = abs(left_x - left_margin) < (page_width * 0.05)
                        
                        # Check if right-aligned (within 5% of right margin)
                        right_margin = page_layout["margins"]["right"]
                        is_right_aligned = abs(right_x - (page_width - right_margin)) < (page_width * 0.05)
                        
                        alignment = "unknown"
                        if is_centered:
                            alignment = "center"
                        elif is_left_aligned:
                            alignment = "left"
                        elif is_right_aligned:
                            alignment = "right"
                        else:
                            alignment = "justified"
                        
                        line_alignments.append({
                            "y_position": y_pos,
                            "alignment": alignment,
                            "width": line_width,
                            "left_x": left_x,
                            "right_x": right_x,
                            "center_x": center_x
                        })
                
                page_layout["line_alignments"] = line_alignments
                
                # Analyze word spacing
                word_spacings = []
                for word in words:
                    word_width = word["x1"] - word["x0"]
                    word_height = word["top"] - word["bottom"]
                    word_spacings.append({
                        "text": word["text"],
                        "width": word_width,
                        "height": word_height,
                        "x": word["x0"],
                        "y": word["top"],
                        "bbox": [word["x0"], word["top"], word["x1"], word["bottom"]]
                    })
                
                page_layout["word_spacings"] = word_spacings
                
                # Detect columns
                if page_layout["text_blocks"]:
                    column_analysis = detect_columns(page_layout["text_blocks"], page_width)
                    page_layout["columns"] = column_analysis
                
                # Detect headers and footers
                header_footer_analysis = detect_headers_footers(page_layout["text_blocks"], page_height)
                page_layout["headers"] = header_footer_analysis["headers"]
                page_layout["footers"] = header_footer_analysis["footers"]
        
        # Analyze overall layout patterns
        layout_data["overall_stats"] = analyze_overall_layout(layout_data["pages"])
        layout_data["layout_patterns"] = analyze_layout_patterns(layout_data["pages"])
        layout_data["spacing_analysis"] = analyze_spacing(layout_data["pages"])
        layout_data["alignment_analysis"] = analyze_alignments(layout_data["pages"])
        layout_data["grid_system"] = detect_grid_system(layout_data["pages"])
        layout_data["visual_hierarchy"] = analyze_visual_hierarchy(layout_data["pages"])
        
    except Exception as e:
        logger.error(f"Error in comprehensive layout extraction: {e}")
        return {"error": str(e)}
    
    return layout_data

def detect_columns(text_blocks, page_width):
    """Detect column layout in text blocks"""
    
    if not text_blocks:
        return []
    
    # Group blocks by vertical position (within 20px tolerance)
    y_groups = defaultdict(list)
    tolerance = 20
    
    for block in text_blocks:
        y_pos = round(block["y"] / tolerance) * tolerance
        y_groups[y_pos].append(block)
    
    # Analyze each horizontal level for columns
    columns = []
    for y_pos, blocks in y_groups.items():
        if len(blocks) > 1:
            # Sort blocks by x position
            sorted_blocks = sorted(blocks, key=lambda b: b["x"])
            
            # Check for clear column separation
            column_gaps = []
            for i in range(len(sorted_blocks) - 1):
                gap = sorted_blocks[i + 1]["x"] - (sorted_blocks[i]["x"] + sorted_blocks[i]["width"])
                column_gaps.append(gap)
            
            # If there are significant gaps, consider as columns
            avg_gap = sum(column_gaps) / len(column_gaps) if column_gaps else 0
            if avg_gap > 50:  # Minimum 50px gap for columns
                columns.append({
                    "y_position": y_pos,
                    "num_columns": len(sorted_blocks),
                    "blocks": sorted_blocks,
                    "gaps": column_gaps,
                    "avg_gap": avg_gap
                })
    
    return columns

def detect_headers_footers(text_blocks, page_height):
    """Detect headers and footers based on position"""
    
    headers = []
    footers = []
    
    # Define header/footer zones (top/bottom 10% of page)
    header_zone = page_height * 0.1
    footer_zone = page_height * 0.9
    
    for block in text_blocks:
        if block["y"] < header_zone:
            headers.append(block)
        elif block["y"] > footer_zone:
            footers.append(block)
    
    return {
        "headers": headers,
        "footers": footers
    }

def analyze_overall_layout(pages):
    """Analyze overall layout statistics"""
    
    if not pages:
        return {}
    
    # Collect statistics across all pages
    all_dimensions = [page["dimensions"] for page in pages]
    all_margins = [page["margins"] for page in pages if page["margins"]]
    all_text_blocks = [block for page in pages for block in page["text_blocks"]]
    
    # Calculate averages
    avg_width = sum(d["width"] for d in all_dimensions) / len(all_dimensions)
    avg_height = sum(d["height"] for d in all_dimensions) / len(all_dimensions)
    avg_aspect_ratio = sum(d["aspect_ratio"] for d in all_dimensions) / len(all_dimensions)
    
    avg_margins = {}
    if all_margins:
        avg_margins = {
            "left": sum(m["left"] for m in all_margins) / len(all_margins),
            "right": sum(m["right"] for m in all_margins) / len(all_margins),
            "top": sum(m["top"] for m in all_margins) / len(all_margins),
            "bottom": sum(m["bottom"] for m in all_margins) / len(all_margins)
        }
    
    # Text block statistics
    text_block_sizes = [(block["width"], block["height"]) for block in all_text_blocks]
    avg_block_width = sum(w for w, h in text_block_sizes) / len(text_block_sizes) if text_block_sizes else 0
    avg_block_height = sum(h for w, h in text_block_sizes) / len(text_block_sizes) if text_block_sizes else 0
    
    return {
        "total_pages": len(pages),
        "avg_page_width": avg_width,
        "avg_page_height": avg_height,
        "avg_aspect_ratio": avg_aspect_ratio,
        "avg_margins": avg_margins,
        "total_text_blocks": len(all_text_blocks),
        "avg_text_block_width": avg_block_width,
        "avg_text_block_height": avg_block_height
    }

def analyze_layout_patterns(pages):
    """Analyze recurring layout patterns"""
    
    patterns = {
        "consistent_margins": False,
        "consistent_spacing": False,
        "grid_based": False,
        "asymmetric": False,
        "centered_layout": False
    }
    
    if not pages:
        return patterns
    
    # Check for consistent margins
    margins = [page["margins"] for page in pages if page["margins"]]
    if margins:
        left_margins = [m["left"] for m in margins]
        right_margins = [m["right"] for m in margins]
        top_margins = [m["top"] for m in margins]
        bottom_margins = [m["bottom"] for m in margins]
        
        # Check if margins are consistent (within 10px tolerance)
        tolerance = 10
        patterns["consistent_margins"] = (
            max(left_margins) - min(left_margins) < tolerance and
            max(right_margins) - min(right_margins) < tolerance and
            max(top_margins) - min(top_margins) < tolerance and
            max(bottom_margins) - min(bottom_margins) < tolerance
        )
    
    # Check for centered layout
    center_alignments = 0
    total_alignments = 0
    
    for page in pages:
        if "line_alignments" in page:
            for alignment in page["line_alignments"]:
                total_alignments += 1
                if alignment["alignment"] == "center":
                    center_alignments += 1
    
    if total_alignments > 0:
        center_percentage = (center_alignments / total_alignments) * 100
        patterns["centered_layout"] = center_percentage > 50
    
    return patterns

def analyze_spacing(pages):
    """Analyze spacing patterns"""
    
    spacing_data = {
        "line_spacing": [],
        "paragraph_spacing": [],
        "section_spacing": [],
        "margin_consistency": {}
    }
    
    for page in pages:
        if "text_blocks" in page and len(page["text_blocks"]) > 1:
            # Sort blocks by y position
            sorted_blocks = sorted(page["text_blocks"], key=lambda b: b["y"])
            
            # Calculate spacing between blocks
            for i in range(len(sorted_blocks) - 1):
                current_block = sorted_blocks[i]
                next_block = sorted_blocks[i + 1]
                
                spacing = next_block["y"] - (current_block["y"] + current_block["height"])
                spacing_data["paragraph_spacing"].append(spacing)
    
    # Calculate spacing statistics
    if spacing_data["paragraph_spacing"]:
        spacing_data["paragraph_spacing_stats"] = {
            "min": min(spacing_data["paragraph_spacing"]),
            "max": max(spacing_data["paragraph_spacing"]),
            "avg": sum(spacing_data["paragraph_spacing"]) / len(spacing_data["paragraph_spacing"]),
            "median": sorted(spacing_data["paragraph_spacing"])[len(spacing_data["paragraph_spacing"]) // 2]
        }
    
    return spacing_data

def analyze_alignments(pages):
    """Analyze text alignment patterns"""
    
    alignment_counts = {
        "left": 0,
        "center": 0,
        "right": 0,
        "justified": 0,
        "unknown": 0
    }
    
    alignment_by_page = []
    
    for page in pages:
        page_alignments = {"page": page["page_number"], "alignments": alignment_counts.copy()}
        
        if "line_alignments" in page:
            for alignment in page["line_alignments"]:
                align_type = alignment["alignment"]
                alignment_counts[align_type] += 1
                page_alignments["alignments"][align_type] += 1
        
        alignment_by_page.append(page_alignments)
    
    # Calculate percentages
    total_alignments = sum(alignment_counts.values())
    alignment_percentages = {}
    if total_alignments > 0:
        alignment_percentages = {
            align_type: (count / total_alignments) * 100
            for align_type, count in alignment_counts.items()
        }
    
    return {
        "total_alignments": total_alignments,
        "alignment_counts": alignment_counts,
        "alignment_percentages": alignment_percentages,
        "alignment_by_page": alignment_by_page
    }

def detect_grid_system(pages):
    """Detect if document uses a grid system"""
    
    grid_analysis = {
        "uses_grid": False,
        "grid_columns": 0,
        "grid_rows": 0,
        "grid_consistency": 0.0
    }
    
    if not pages:
        return grid_analysis
    
    # Analyze column patterns across pages
    all_columns = []
    for page in pages:
        if "columns" in page:
            all_columns.extend(page["columns"])
    
    if all_columns:
        # Check for consistent column count
        column_counts = [col["num_columns"] for col in all_columns]
        most_common_columns = Counter(column_counts).most_common(1)[0]
        
        grid_analysis["uses_grid"] = most_common_columns[1] > len(all_columns) * 0.5
        grid_analysis["grid_columns"] = most_common_columns[0]
        grid_analysis["grid_consistency"] = most_common_columns[1] / len(all_columns)
    
    return grid_analysis

def analyze_visual_hierarchy(pages):
    """Analyze visual hierarchy based on font sizes and positioning"""
    
    hierarchy_data = {
        "title_levels": [],
        "heading_levels": [],
        "body_text": [],
        "caption_text": [],
        "hierarchy_consistency": 0.0
    }
    
    # Collect font sizes across all pages
    all_font_sizes = []
    for page in pages:
        if "text_blocks" in page:
            for block in page["text_blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        # Extract font size from line data if available
                        if "font_size" in line:
                            all_font_sizes.append(line["font_size"])
    
    if all_font_sizes:
        # Categorize by size
        sorted_sizes = sorted(set(all_font_sizes), reverse=True)
        
        # Define hierarchy levels
        if len(sorted_sizes) >= 3:
            hierarchy_data["title_levels"] = sorted_sizes[:2]  # Largest sizes
            hierarchy_data["heading_levels"] = sorted_sizes[2:4] if len(sorted_sizes) >= 4 else []
            hierarchy_data["body_text"] = sorted_sizes[4:6] if len(sorted_sizes) >= 6 else []
            hierarchy_data["caption_text"] = sorted_sizes[6:] if len(sorted_sizes) >= 7 else []
    
    return hierarchy_data 