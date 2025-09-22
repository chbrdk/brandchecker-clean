import os
import re
import json
import logging
from collections import Counter, defaultdict
import tempfile
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_fonts_from_pdf_comprehensive(pdf_path):
    """Comprehensive font extraction from PDF using multiple methods"""
    
    # Import libraries here to avoid import issues
    import fitz  # PyMuPDF
    import pdfplumber
    
    all_fonts = []
    font_sources = {
        "text_fonts": [],
        "embedded_fonts": [],
        "system_fonts": [],
        "font_metrics": []
    }
    
    try:
        # Method 1: PyMuPDF for detailed font analysis
        logger.info("Starting PyMuPDF font analysis...")
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get text dictionary with font information
            text_dict = page.get_text("dict")
            
            for block in text_dict.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line.get("spans", []):
                            if "font" in span and "size" in span:
                                font_name = span["font"]
                                font_size = span["size"]
                                font_color = span.get("color", 0)
                                text_content = span.get("text", "")
                                
                                # Get font flags and properties
                                font_flags = span.get("flags", 0)
                                is_bold = bool(font_flags & 2**4)  # Bit 4 indicates bold
                                is_italic = bool(font_flags & 2**1)  # Bit 1 indicates italic
                                
                                font_info = {
                                    "name": font_name,
                                    "size": font_size,
                                    "color": font_color,
                                    "text_sample": text_content[:50],  # First 50 chars
                                    "is_bold": is_bold,
                                    "is_italic": is_italic,
                                    "flags": font_flags,
                                    "page": page_num + 1,
                                    "source": "pymupdf_text",
                                    "usage_count": 1
                                }
                                
                                all_fonts.append(font_info)
                                font_sources["text_fonts"].append(font_info)
        
        # Method 2: pdfplumber for additional font details
        logger.info("Starting pdfplumber font analysis...")
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract characters with font information
                chars = page.chars
                
                for char in chars:
                    if "fontname" in char and "size" in char:
                        font_name = char["fontname"]
                        font_size = char["size"]
                        text_content = char.get("text", "")
                        
                        # Get additional font properties
                        font_info = {
                            "name": font_name,
                            "size": font_size,
                            "text_sample": text_content,
                            "page": page_num + 1,
                            "source": "pdfplumber_char",
                            "usage_count": 1,
                            "x": char.get("x0", 0),
                            "y": char.get("y0", 0)
                        }
                        
                        all_fonts.append(font_info)
                        font_sources["text_fonts"].append(font_info)
        
        # Method 3: Extract embedded fonts from PDF resources
        logger.info("Starting embedded font analysis...")
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get page resources
            if hasattr(page, 'get') and page.get('Resources'):
                resources = page.get('Resources')
                
                # Check for font resources
                if 'Font' in resources:
                    fonts = resources['Font']
                    for font_name, font_obj in fonts.items():
                        if hasattr(font_obj, 'get'):
                            font_type = font_obj.get('Subtype', 'Unknown')
                            font_base = font_obj.get('BaseFont', font_name)
                            
                            embedded_font_info = {
                                "name": font_name,
                                "base_font": font_base,
                                "type": font_type,
                                "page": page_num + 1,
                                "source": "embedded_font",
                                "usage_count": 1
                            }
                            
                            all_fonts.append(embedded_font_info)
                            font_sources["embedded_fonts"].append(embedded_font_info)
        
        doc.close()
        
    except Exception as e:
        logger.error(f"Error in comprehensive font extraction: {e}")
        return {"error": str(e)}
    
    # Aggregate and analyze all fonts
    font_analysis = aggregate_fonts(all_fonts, font_sources)
    
    return font_analysis

def aggregate_fonts(all_fonts, font_sources):
    """Aggregate and analyze all extracted fonts"""
    
    # Group fonts by name and size
    font_groups = {}
    
    for font in all_fonts:
        font_key = f"{font['name']}_{font.get('size', 'unknown')}"
        
        if font_key not in font_groups:
            font_groups[font_key] = {
                "name": font["name"],
                "size": font.get("size", "unknown"),
                "total_count": 0,
                "sources": set(),
                "pages": set(),
                "text_samples": [],
                "properties": {
                    "is_bold": False,
                    "is_italic": False,
                    "colors": set(),
                    "flags": set()
                },
                "details": []
            }
        
        font_groups[font_key]["total_count"] += font.get("usage_count", 1)
        font_groups[font_key]["sources"].add(font["source"])
        font_groups[font_key]["pages"].add(font["page"])
        
        # Collect text samples
        if "text_sample" in font and font["text_sample"]:
            font_groups[font_key]["text_samples"].append(font["text_sample"])
        
        # Collect properties
        if font.get("is_bold"):
            font_groups[font_key]["properties"]["is_bold"] = True
        if font.get("is_italic"):
            font_groups[font_key]["properties"]["is_italic"] = True
        if "color" in font:
            font_groups[font_key]["properties"]["colors"].add(font["color"])
        if "flags" in font:
            font_groups[font_key]["properties"]["flags"].add(font["flags"])
        
        font_groups[font_key]["details"].append(font)
    
    # Calculate total usage
    total_usage = sum(group["total_count"] for group in font_groups.values())
    
    # Create final font list
    final_fonts = []
    for font_key, group in font_groups.items():
        percentage = (group["total_count"] / total_usage * 100) if total_usage > 0 else 0
        
        # Get most common text sample
        text_samples = group["text_samples"]
        most_common_sample = ""
        if text_samples:
            sample_counter = Counter(text_samples)
            most_common_sample = sample_counter.most_common(1)[0][0]
        
        final_font = {
            "name": group["name"],
            "size": group["size"],
            "usage_count": group["total_count"],
            "usage_percentage": round(percentage, 2),
            "sources": list(group["sources"]),
            "pages": list(group["pages"]),
            "text_sample": most_common_sample,
            "properties": {
                "is_bold": group["properties"]["is_bold"],
                "is_italic": group["properties"]["is_italic"],
                "colors": list(group["properties"]["colors"]),
                "flags": list(group["properties"]["flags"])
            },
            "description": f"Font '{group['name']}' (size {group['size']}) used {group['total_count']} times ({percentage:.1f}%) across {len(group['sources'])} sources"
        }
        final_fonts.append(final_font)
    
    # Sort by usage
    final_fonts.sort(key=lambda x: x["usage_count"], reverse=True)
    
    # Create summary
    summary = {
        "total_fonts": len(final_fonts),
        "total_usage": total_usage,
        "font_sources": {
            "text_fonts": len(font_sources["text_fonts"]),
            "embedded_fonts": len(font_sources["embedded_fonts"]),
            "system_fonts": len(font_sources["system_fonts"]),
            "font_metrics": len(font_sources["font_metrics"])
        },
        "fonts": final_fonts
    }
    
    return summary

def analyze_font_usage_patterns(font_analysis):
    """Analyze font usage patterns and provide insights"""
    
    if "fonts" not in font_analysis:
        return {"error": "No font data available"}
    
    fonts = font_analysis["fonts"]
    
    # Analyze font families
    font_families = defaultdict(list)
    for font in fonts:
        # Extract font family name (remove size and style suffixes)
        family_name = re.sub(r'[-\d]+$', '', font["name"]).strip()
        font_families[family_name].append(font)
    
    # Analyze size distribution
    size_distribution = defaultdict(int)
    for font in fonts:
        size = font.get("size", "unknown")
        size_distribution[size] += font["usage_count"]
    
    # Analyze style distribution
    style_stats = {
        "bold": 0,
        "italic": 0,
        "regular": 0
    }
    
    for font in fonts:
        if font["properties"]["is_bold"]:
            style_stats["bold"] += font["usage_count"]
        elif font["properties"]["is_italic"]:
            style_stats["italic"] += font["usage_count"]
        else:
            style_stats["regular"] += font["usage_count"]
    
    # Create insights
    insights = {
        "font_families": {
            "count": len(font_families),
            "families": dict(font_families)
        },
        "size_distribution": dict(size_distribution),
        "style_distribution": style_stats,
        "most_used_font": fonts[0] if fonts else None,
        "font_variety": len(fonts)
    }
    
    return insights 