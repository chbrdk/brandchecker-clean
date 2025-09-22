import os
import json
import logging
import tempfile
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import io
from global_graphic_detector import GlobalGraphicDetector
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_visual_report_with_ai_graphics(pdf_path, output_path, openai_api_key):
    """Generate visual report with AI-analyzed graphics marked"""
    
    try:
        logger.info("Generating visual report with AI graphics analysis...")
        
        # Step 1: Detect graphics with AI analysis
        detector = GlobalGraphicDetector(openai_api_key)
        graphic_results = detector.detect_all_graphics(pdf_path)
        
        if "error" in graphic_results:
            logger.error(f"Error in graphic detection: {graphic_results['error']}")
            return {"error": graphic_results["error"]}
        
        # Step 2: Generate visual report with graphics marked using PIL
        report_result = create_visual_report_with_pil(pdf_path, output_path, graphic_results)
        
        return {
            "visual_report_path": output_path,
            "graphic_analysis": graphic_results,
            "report_generated": True
        }
        
    except Exception as e:
        logger.error(f"Error generating visual report with AI graphics: {e}")
        return {"error": str(e)}

def create_visual_report_with_pil(pdf_path, output_path, graphic_results):
    """Create visual report with AI-analyzed graphics marked using PIL"""
    
    try:
        # Open PDF
        doc = fitz.open(pdf_path)
        
        # Create new PDF for report
        report_doc = fitz.open()
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Convert page to image with high resolution
            mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            pil_image = Image.open(io.BytesIO(img_data))
            
            # Draw annotations on the image
            annotated_image = draw_annotations_on_image(pil_image, graphic_results, page_num + 1)
            
            # Convert back to PDF page
            img_bytes = io.BytesIO()
            annotated_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Create new page in report
            report_page = report_doc.new_page(width=page.rect.width, height=page.rect.height)
            
            # Insert the annotated image
            report_page.insert_image(report_page.rect, stream=img_bytes.getvalue())
        
        # Save report
        report_doc.save(output_path)
        report_doc.close()
        doc.close()
        
        return {"success": True, "output_path": output_path}
        
    except Exception as e:
        logger.error(f"Error creating visual report with PIL: {e}")
        return {"error": str(e)}

def draw_annotations_on_image(pil_image, graphic_results, page_num):
    """Draw annotations on PIL image"""
    
    try:
        logger.info(f"Drawing annotations for page {page_num}")
        logger.info(f"Graphic results keys: {list(graphic_results.keys())}")
        
        # Create a copy of the image for drawing
        annotated_image = pil_image.copy()
        draw = ImageDraw.Draw(annotated_image)
        
        # Try to load a font, fallback to default if not available
        try:
            font_large = ImageFont.truetype("arial.ttf", 16)
            font_medium = ImageFont.truetype("arial.ttf", 12)
            font_small = ImageFont.truetype("arial.ttf", 10)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # SIMPLIFIED APPROACH: Direct access to data
        graphic_regions = graphic_results.get("graphic_regions", [])
        ai_analyses = graphic_results.get("ai_analysis", [])
        
        logger.info(f"Total graphic regions: {len(graphic_regions)}")
        logger.info(f"Total AI analyses: {len(ai_analyses)}")
        
        # Process each AI analysis and find corresponding region
        valid_annotations = []
        
        for i, analysis in enumerate(ai_analyses):
            logger.info(f"Processing AI analysis {i+1}: {type(analysis)}")
            
            if not isinstance(analysis, dict):
                logger.warning(f"Analysis {i+1} is not a dict: {type(analysis)}")
                continue
                
            if not analysis.get("success"):
                logger.info(f"Analysis {i+1} not successful, skipping")
                continue
            
            # Get the corresponding region by index
            if i < len(graphic_regions):
                region = graphic_regions[i]
                logger.info(f"Found region {i+1}: {type(region)}")
                
                if not isinstance(region, dict):
                    logger.warning(f"Region {i+1} is not a dict: {type(region)}")
                    continue
                
                if region.get("page") == page_num:
                    ai_data = analysis.get("ai_analysis", {})
                    logger.info(f"Region {i+1} is on page {page_num}, AI data type: {type(ai_data)}")
                    
                    if isinstance(ai_data, dict):
                        valid_annotations.append({
                            "region": region,
                            "ai_data": ai_data,
                            "index": i + 1
                        })
                        logger.info(f"Added valid annotation {i+1}")
                    else:
                        logger.warning(f"AI data for region {i+1} is not a dict: {type(ai_data)}")
        
        logger.info(f"Found {len(valid_annotations)} valid annotations for page {page_num}")
        
        # Draw annotations for each valid graphic
        for annotation in valid_annotations:
            region = annotation["region"]
            ai_data = annotation["ai_data"]
            graphic_number = annotation["index"]
            
            logger.info(f"Drawing annotation {graphic_number} for region: {region.get('bbox', 'NO_BBOX')}")
            draw_single_annotation_safe(draw, region, ai_data, graphic_number, font_large, font_medium, font_small)
        
        # Add legend if we have annotations
        if valid_annotations:
            draw_legend_simple(draw, valid_annotations, annotated_image.size, font_medium, font_small)
        
        return annotated_image
        
    except Exception as e:
        logger.error(f"Error drawing annotations on image: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return pil_image

def draw_single_annotation_safe(draw, region, ai_data, graphic_number, font_large, font_medium, font_small):
    """Draw annotation for a single graphic with extensive safety checks"""
    
    try:
        logger.info(f"Starting to draw annotation {graphic_number}")
        
        # Ensure region is a dictionary
        if not isinstance(region, dict):
            logger.error(f"Region is not a dictionary: {type(region)}")
            return
            
        # Get bbox safely
        bbox = region.get("bbox")
        if not bbox or not isinstance(bbox, list) or len(bbox) != 4:
            logger.error(f"Invalid bbox: {bbox}")
            return
            
        x1, y1, x2, y2 = bbox
        logger.info(f"Drawing annotation at coordinates: ({x1}, {y1}) to ({x2}, {y2})")
        
        # Ensure ai_data is a dictionary
        if not isinstance(ai_data, dict):
            logger.error(f"AI data is not a dictionary: {type(ai_data)}")
            return
        
        # Get color based on graphic type
        graphic_type = ai_data.get("graphic_type", "unknown")
        color = get_graphic_type_color_pil(graphic_type)
        logger.info(f"Using color {color} for graphic type: {graphic_type}")
        
        # Draw rectangle border with thicker line
        draw.rectangle([x1, y1, x2, y2], outline=color, width=5)
        logger.info(f"Drew rectangle with color {color}")
        
        # Add graphic number above with background
        number_text = f"#{graphic_number}"
        # Draw background for number
        text_bbox = draw.textbbox((x1, y1 - 25), number_text, font=font_medium)
        draw.rectangle(text_bbox, fill=color)
        draw.text((x1, y1 - 25), number_text, fill=(255, 255, 255), font=font_medium)  # White text
        logger.info(f"Added number label: {number_text}")
        
        # Add graphic type below with background
        graphic_type_upper = graphic_type.upper()
        # Draw background for type
        type_bbox = draw.textbbox((x1, y2 + 5), graphic_type_upper, font=font_medium)
        draw.rectangle(type_bbox, fill=color)
        draw.text((x1, y2 + 5), graphic_type_upper, fill=(255, 255, 255), font=font_medium)  # White text
        logger.info(f"Added type label: {graphic_type_upper}")
        
        # Add brand if available
        brand = ai_data.get("brand_company")
        if brand and brand != "null":
            # Draw background for brand
            brand_bbox = draw.textbbox((x1, y2 + 25), brand, font=font_small)
            draw.rectangle(brand_bbox, fill=color)
            draw.text((x1, y2 + 25), brand, fill=(255, 255, 255), font=font_small)  # White text
            logger.info(f"Added brand label: {brand}")
        
        # Add confidence score
        confidence = ai_data.get("confidence", 0)
        if confidence > 0:
            conf_text = f"Conf: {confidence:.1%}"
            # Draw background for confidence
            conf_bbox = draw.textbbox((x1, y2 + 45), conf_text, font=font_small)
            draw.rectangle(conf_bbox, fill=color)
            draw.text((x1, y2 + 45), conf_text, fill=(255, 255, 255), font=font_small)  # White text
            logger.info(f"Added confidence label: {conf_text}")
        
        logger.info(f"Successfully completed annotation {graphic_number}")
        
    except Exception as e:
        logger.error(f"Error drawing single annotation {graphic_number}: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")

def get_graphic_type_color_pil(graphic_type):
    """Get PIL color for different graphic types"""
    
    color_map = {
        "logo": (255, 0, 0),      # Red
        "icon": (0, 0, 255),      # Blue
        "illustration": (0, 255, 0),  # Green
        "diagram": (255, 255, 0),   # Yellow
        "chart": (255, 0, 255),     # Magenta
        "other": (128, 128, 128)  # Gray
    }
    
    return color_map.get(graphic_type.lower(), (255, 0, 0))  # Red as default

def draw_legend_simple(draw, valid_annotations, image_size, font_medium, font_small):
    """Draw simple legend"""
    
    try:
        if not valid_annotations:
            return
        
        # Position legend in bottom-left
        legend_x = 10
        legend_y = image_size[1] - 200
        
        # Draw legend background
        legend_bg = [(legend_x - 10, legend_y - 10), (legend_x + 240, legend_y + 150)]
        draw.rectangle(legend_bg, fill=(255, 255, 255), outline=(0, 0, 0), width=2)
        
        # Add legend title
        draw.text((legend_x, legend_y), "AI Graphics Analysis", fill=(0, 0, 0), font=font_medium)
        
        # Add legend entries
        y_offset = 30
        for annotation in valid_annotations:
            region = annotation["region"]
            ai_data = annotation["ai_data"]
            graphic_number = annotation["index"]
            
            graphic_type = ai_data.get("graphic_type", "unknown").upper()
            color = get_graphic_type_color_pil(graphic_type)
            
            # Add description
            description = f"#{graphic_number}: {graphic_type}"
            brand = ai_data.get("brand_company")
            if brand and brand != "null":
                description += f" ({brand})"
            
            draw.text((legend_x, legend_y + y_offset), description, fill=color, font=font_small)
            y_offset += 20
        
        logger.info("Drew simple legend successfully")
        
    except Exception as e:
        logger.error(f"Error drawing simple legend: {e}")

def create_detailed_report_with_ai_graphics(pdf_path, output_path, openai_api_key):
    """Create detailed text report with AI graphics analysis"""
    
    try:
        logger.info("Creating detailed report with AI graphics analysis...")
        
        # Get AI graphics analysis
        detector = GlobalGraphicDetector(openai_api_key)
        graphic_results = detector.detect_all_graphics(pdf_path)
        
        if "error" in graphic_results:
            logger.error(f"Error in graphic detection: {graphic_results['error']}")
            return {"error": graphic_results["error"]}
        
        # Create detailed report
        report_content = generate_detailed_report_content(graphic_results)
        
        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return {
            "detailed_report_path": output_path,
            "graphic_analysis": graphic_results,
            "report_generated": True
        }
        
    except Exception as e:
        logger.error(f"Error creating detailed report with AI graphics: {e}")
        return {"error": str(e)}

def generate_detailed_report_content(graphic_results):
    """Generate detailed report content with AI graphics analysis"""
    
    try:
        content = []
        content.append("=" * 80)
        content.append("AI GRAPHICS ANALYSIS REPORT")
        content.append("=" * 80)
        content.append("")
        
        # Summary
        summary = graphic_results.get("analysis_summary", {})
        content.append("EXECUTIVE SUMMARY")
        content.append("-" * 40)
        content.append(f"Total Graphics Detected: {summary.get('total_regions', 0)}")
        content.append(f"High Confidence Regions: {summary.get('high_confidence_regions', 0)}")
        content.append(f"Medium Confidence Regions: {summary.get('medium_confidence_regions', 0)}")
        content.append(f"Low Confidence Regions: {summary.get('low_confidence_regions', 0)}")
        content.append("")
        
        # AI Analysis Summary
        ai_summary = summary.get("ai_analysis_summary", {})
        content.append("AI ANALYSIS SUMMARY")
        content.append("-" * 40)
        
        # Graphic types
        graphic_types = ai_summary.get("graphic_types", {})
        content.append("Graphic Types Found:")
        for gtype, count in graphic_types.items():
            content.append(f"  - {gtype.title()}: {count}")
        content.append("")
        
        # Brands/Companies
        brands = ai_summary.get("brands_companies", [])
        if brands:
            content.append("Brands/Companies Identified:")
            for brand in brands:
                if brand and brand != "null":
                    content.append(f"  - {brand}")
            content.append("")
        
        # Quality distribution
        quality_dist = ai_summary.get("quality_distribution", {})
        content.append("Quality Distribution:")
        for quality, count in quality_dist.items():
            content.append(f"  - {quality.title()}: {count}")
        content.append("")
        
        # Detailed Analysis
        content.append("DETAILED GRAPHICS ANALYSIS")
        content.append("=" * 40)
        content.append("")
        
        # Get recommended graphics
        recommended = graphic_results.get("recommended_graphics", [])
        
        for i, rec in enumerate(recommended, 1):
            region = rec["region"]
            ai_data = rec["ai_analysis"]
            
            content.append(f"GRAPHIC #{i}")
            content.append("-" * 20)
            content.append(f"Page: {region['page']}")
            content.append(f"Position: ({region['center_x']}, {region['center_y']})")
            content.append(f"Size: {region['width']} x {region['height']} pixels")
            content.append(f"Area: {region['area']} pixels²")
            content.append(f"Detection Method: {region['detection_method']}")
            content.append(f"Detection Confidence: {region['confidence']:.1%}")
            content.append("")
            
            # AI Analysis
            content.append("AI Analysis:")
            content.append(f"  Graphic Type: {ai_data.get('graphic_type', 'unknown').title()}")
            content.append(f"  Content: {ai_data.get('content_description', 'No description')}")
            content.append(f"  Colors: {', '.join(ai_data.get('colors', []))}")
            
            brand = ai_data.get("brand_company")
            if brand and brand != "null":
                content.append(f"  Brand/Company: {brand}")
            
            content.append(f"  Quality: {ai_data.get('quality', 'unknown').title()}")
            content.append(f"  AI Confidence: {ai_data.get('confidence', 0):.1%}")
            content.append(f"  Overall Score: {rec['overall_score']:.1%}")
            content.append("")
            
            # Recommendation reasons
            reasons = rec.get("recommendation_reason", [])
            if reasons:
                content.append("Recommendation Reasons:")
                for reason in reasons:
                    content.append(f"  - {reason}")
                content.append("")
            
            content.append("-" * 40)
            content.append("")
        
        # Detection Methods Summary
        content.append("DETECTION METHODS USED")
        content.append("-" * 40)
        detection_methods = summary.get("detection_methods", {})
        for method, count in detection_methods.items():
            content.append(f"  - {method.replace('_', ' ').title()}: {count}")
        content.append("")
        
        # Conclusion
        content.append("CONCLUSION")
        content.append("-" * 40)
        content.append("This report provides a comprehensive analysis of all graphics")
        content.append("found in the PDF document, using advanced AI vision analysis")
        content.append("to identify logos, illustrations, icons, and other visual elements.")
        content.append("")
        content.append("The AI analysis provides detailed insights into:")
        content.append("  - Graphic types and classifications")
        content.append("  - Brand and company identification")
        content.append("  - Color analysis and visual characteristics")
        content.append("  - Quality assessment and confidence scores")
        content.append("")
        content.append("=" * 80)
        
        return "\n".join(content)
        
    except Exception as e:
        logger.error(f"Error generating detailed report content: {e}")
        return f"Error generating report: {str(e)}"

def generate_visual_report_with_ai_graphics_and_text(pdf_path, graphic_results, text_results):
    """Generate visual report with AI-analyzed graphics AND text annotations"""
    
    try:
        # Open the PDF
        pdf_document = fitz.open(pdf_path)
        
        # Create output PDF
        output_pdf = fitz.open()
        
        # Use PIL's default font instead of PyMuPDF fonts
        from PIL import ImageFont
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        except:
            # Fallback to default font
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Process each page
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Convert PDF page to PIL image
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Higher resolution
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            draw = ImageDraw.Draw(img)
            
            logger.info(f"Drawing annotations for page {page_num + 1} (graphics + text)")
            
            # Draw graphics annotations
            graphic_annotations = draw_graphics_annotations(draw, graphic_results, page_num + 1, font_large, font_medium, font_small)
            
            # Draw text annotations
            text_elements = text_results.get("text_elements", [])
            # Filter text elements for current page
            page_texts = [elem for elem in text_elements if elem.get("page") == page_num + 1]
            text_annotations = draw_text_annotations(draw, page_texts, page_num + 1, font_large, font_medium, font_small)
            
            # Draw combined legend (fixed function call)
            draw_combined_legend(draw, graphic_annotations, text_annotations, font_medium)
            
            # Convert back to PDF page
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Create new page in output PDF
            output_page = output_pdf.new_page(width=page.rect.width, height=page.rect.height)
            output_page.insert_image(page.rect, stream=img_bytes.getvalue())
        
        # Save the output PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_visual_report_with_text_{os.path.basename(pdf_path).replace('.pdf', '')}_{timestamp}.pdf"
        output_path = f"/app/shared/reports/{filename}"
        
        # Ensure directory exists
        os.makedirs("/app/shared/reports", exist_ok=True)
        
        output_pdf.save(output_path)
        output_pdf.close()
        pdf_document.close()
        
        logger.info(f"Generated visual report with AI graphics and text: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error generating visual report with AI graphics and text: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None

def extract_text_elements(pdf_path):
    """Extract text elements from PDF using PyMuPDF"""
    
    try:
        doc = fitz.open(pdf_path)
        text_elements = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get text blocks
            text_blocks = page.get_text("dict")
            
            for block in text_blocks.get("blocks", []):
                if "lines" in block:  # Text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text_element = {
                                "page": page_num + 1,
                                "bbox": span["bbox"],
                                "text": span["text"],
                                "font": span["font"],
                                "size": span["size"],
                                "color": span["color"],
                                "flags": span["flags"]
                            }
                            text_elements.append(text_element)
        
        doc.close()
        
        logger.info(f"Extracted {len(text_elements)} text elements")
        return {"text_elements": text_elements, "total_elements": len(text_elements)}
        
    except Exception as e:
        logger.error(f"Error extracting text elements: {e}")
        return {"error": str(e)}

def create_visual_report_with_graphics_and_text(pdf_path, output_path, graphic_results, text_results):
    """Create visual report with both graphics and text marked"""
    
    try:
        # Open PDF
        doc = fitz.open(pdf_path)
        
        # Create new PDF for report
        report_doc = fitz.open()
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Convert page to image with high resolution
            mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            pil_image = Image.open(io.BytesIO(img_data))
            
            # Draw annotations on the image (both graphics and text)
            annotated_image = draw_annotations_with_graphics_and_text(pil_image, graphic_results, text_results, page_num + 1)
            
            # Convert back to PDF page
            img_bytes = io.BytesIO()
            annotated_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Create new page in report
            report_page = report_doc.new_page(width=page.rect.width, height=page.rect.height)
            
            # Insert the annotated image
            report_page.insert_image(report_page.rect, stream=img_bytes.getvalue())
        
        # Save report
        report_doc.save(output_path)
        report_doc.close()
        doc.close()
        
        return {"success": True, "output_path": output_path}
        
    except Exception as e:
        logger.error(f"Error creating visual report with graphics and text: {e}")
        return {"error": str(e)}

def draw_annotations_with_graphics_and_text(pil_image, graphic_results, text_results, page_num):
    """Draw annotations for both graphics and text on PIL image"""
    
    try:
        logger.info(f"Drawing annotations for page {page_num} (graphics + text)")
        
        # Create a copy of the image for drawing
        annotated_image = pil_image.copy()
        draw = ImageDraw.Draw(annotated_image)
        
        # Try to load a font, fallback to default if not available
        try:
            font_large = ImageFont.truetype("arial.ttf", 16)
            font_medium = ImageFont.truetype("arial.ttf", 12)
            font_small = ImageFont.truetype("arial.ttf", 10)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw graphics annotations
        graphic_annotations = draw_graphics_annotations(draw, graphic_results, page_num, font_large, font_medium, font_small)
        
        # Draw text annotations
        text_annotations = draw_text_annotations(draw, text_results, page_num, font_large, font_medium, font_small)
        
        # Combine all annotations for legend
        all_annotations = graphic_annotations + text_annotations
        
        # Add legend if we have annotations
        if all_annotations:
            draw_combined_legend(draw, all_annotations, annotated_image.size, font_medium, font_small)
        
        return annotated_image
        
    except Exception as e:
        logger.error(f"Error drawing annotations with graphics and text: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return pil_image

def draw_graphics_annotations(draw, graphic_results, page_num, font_large, font_medium, font_small):
    """Draw graphics annotations and return list of annotations"""
    
    try:
        graphic_regions = graphic_results.get("graphic_regions", [])
        ai_analyses = graphic_results.get("ai_analysis", [])
        
        valid_annotations = []
        
        # Step 1: Identify the main large image (likely the product photo)
        main_image_regions = []
        other_regions = []
        
        for i, analysis in enumerate(ai_analyses):
            if not isinstance(analysis, dict) or not analysis.get("success"):
                continue
                
            if i < len(graphic_regions):
                region = graphic_regions[i]
                
                if not isinstance(region, dict) or region.get("page") != page_num:
                    continue
                
                bbox = region.get("bbox", [])
                if len(bbox) == 4:
                    width = bbox[2] - bbox[0]
                    height = bbox[3] - bbox[1]
                    area = width * height
                    
                    # Consider regions larger than 30% of page as potential main images (more aggressive)
                    page_area = 595 * 842  # A4 page size in points
                    if area > (page_area * 0.3):
                        main_image_regions.append({
                            "region": region,
                            "analysis": analysis,
                            "area": area,
                            "index": i
                        })
                    else:
                        other_regions.append({
                            "region": region,
                            "analysis": analysis,
                            "area": area,
                            "index": i
                        })
        
        # Step 2: Sort main images by area (largest first)
        main_image_regions.sort(key=lambda x: x["area"], reverse=True)
        
        # Step 3: Filter out small objects that are contained within main images
        filtered_regions = []
        filtered_analyses = []
        
        # Always include the largest main image
        if main_image_regions:
            largest_main = main_image_regions[0]
            filtered_regions.append(largest_main["region"])
            filtered_analyses.append(largest_main["analysis"])
            logger.info(f"Including main image with area {largest_main['area']} pixels")
        
        # MUCH MORE AGGRESSIVE FILTERING for other regions
        for other in other_regions:
            region = other["region"]
            analysis = other["analysis"]
            bbox = region.get("bbox", [])
            
            # Check if this region is contained within any main image
            is_contained = False
            for main_img in main_image_regions:
                main_bbox = main_img["region"].get("bbox", [])
                if len(main_bbox) == 4 and len(bbox) == 4:
                    # Check if this region is mostly contained within the main image
                    overlap_x = max(0, min(bbox[2], main_bbox[2]) - max(bbox[0], main_bbox[0]))
                    overlap_y = max(0, min(bbox[3], main_bbox[3]) - max(bbox[1], main_bbox[1]))
                    overlap_area = overlap_x * overlap_y
                    region_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                    
                    # If more than 50% of this region is within the main image, filter it out (more aggressive)
                    if overlap_area > (region_area * 0.5):
                        is_contained = True
                        logger.info(f"Filtering out region {other['index']+1} (contained within main image)")
                        break
            
            # MUCH MORE RESTRICTIVE: Only include very large, independent regions
            if not is_contained and other["area"] > 20000:  # Increased minimum area
                # Additional check: must be a logo or very high confidence
                ai_data = analysis.get("ai_analysis", {})
                if isinstance(ai_data, dict):
                    graphic_type = ai_data.get("graphic_type", "")
                    confidence = ai_data.get("confidence", 0)
                    
                    # Only include if it's a logo or has very high confidence
                    if graphic_type == "logo" or confidence > 0.8:
                        filtered_regions.append(region)
                        filtered_analyses.append(analysis)
                        logger.info(f"Including high-confidence region {other['index']+1} with area {other['area']} pixels (type: {graphic_type}, confidence: {confidence})")
        
        logger.info(f"Filtered {len(ai_analyses)} graphics down to {len(filtered_regions)} main graphics")
        
        # Step 4: Draw annotations for filtered regions
        for i, (region, analysis) in enumerate(zip(filtered_regions, filtered_analyses)):
            ai_data = analysis.get("ai_analysis", {})
            
            if isinstance(ai_data, dict):
                annotation_info = {
                    "region": region,
                    "ai_data": ai_data,
                    "index": i + 1,
                    "type": "graphic"
                }
                valid_annotations.append(annotation_info)
                
                # Draw the annotation
                draw_single_graphic_annotation(draw, region, ai_data, i + 1, font_large, font_medium, font_small)
        
        return valid_annotations
        
    except Exception as e:
        logger.error(f"Error drawing graphics annotations: {e}")
        return []

def draw_text_annotations(draw, text_elements, page_num, font_large, font_medium, font_small):
    """Draw text annotations and return list of annotations"""
    
    try:
        valid_annotations = []
        marked_count = 0
        
        logger.info(f"Found {len(text_elements)} text elements on page {page_num}")
        
        for i, text_element in enumerate(text_elements):
            if marked_count >= 20:  # Limit to 20 text elements per page for clarity
                break
                
            if not isinstance(text_element, dict):
                continue
                
            bbox = text_element.get("bbox", [])
            text_content = text_element.get("text", "").strip()
            
            # Skip empty text
            if not text_content:
                continue
            
            # Convert bbox coordinates to integers and ensure they're valid
            try:
                if len(bbox) == 4:
                    # Convert float coordinates to integers
                    x1, y1, x2, y2 = [int(round(coord)) for coord in bbox]
                    
                    # Validate coordinates
                    if x1 >= x2 or y1 >= y2:
                        logger.warning(f"Invalid bbox for text element: {bbox}")
                        continue
                    
                    # Ensure coordinates are within reasonable bounds
                    if x1 < 0 or y1 < 0 or x2 > 1000 or y2 > 1000:
                        logger.warning(f"Bbox out of bounds for text element: {bbox}")
                        continue
                    
                    # Draw the text annotation
                    draw_single_text_annotation_enhanced(draw, x1, y1, x2, y2, text_content, i + 1, font_medium)
                    
                    valid_annotations.append({
                        "bbox": [x1, y1, x2, y2],
                        "text": text_content,
                        "index": i + 1,
                        "type": "text"
                    })
                    
                    marked_count += 1
                    logger.info(f"Successfully processed text element {i+1}: {text_content[:20]}...")
                else:
                    logger.warning(f"Invalid bbox format for text element: {bbox}")
                    
            except (ValueError, TypeError) as e:
                logger.warning(f"Error processing text element {i+1}: {e}")
                continue
        
        logger.info(f"Successfully marked {marked_count} text elements")
        return valid_annotations
        
    except Exception as e:
        logger.error(f"Error drawing text annotations: {e}")
        return []

def draw_single_graphic_annotation(draw, region, ai_data, graphic_number, font_large, font_medium, font_small):
    """Draw annotation for a single graphic"""
    
    try:
        if not isinstance(region, dict):
            return
            
        bbox = region.get("bbox")
        if not bbox or not isinstance(bbox, list) or len(bbox) != 4:
            return
            
        if not isinstance(ai_data, dict):
            return
        
        # Get graphic type and color
        graphic_type = ai_data.get("graphic_type", "unknown")
        color = get_graphic_type_color_pil(graphic_type)
        
        # Draw rectangle
        x1, y1, x2, y2 = bbox
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        
        # Draw label
        label_text = f"#{graphic_number} {graphic_type}"
        brand = ai_data.get("brand_company")
        if brand:
            label_text += f" ({brand})"
        
        # Calculate label position
        label_x = x1
        label_y = y1 - 25
        
        # Draw label background
        bbox_text = draw.textbbox((label_x, label_y), label_text, font=font_small)
        draw.rectangle(bbox_text, fill=color)
        draw.text((label_x, label_y), label_text, fill="white", font=font_small)
        
    except Exception as e:
        logger.error(f"Error drawing single graphic annotation: {e}")

def draw_single_text_annotation_enhanced(draw, x1, y1, x2, y2, text_content, annotation_index, font_medium):
    """Draw enhanced annotation for a single text element with better visibility"""
    
    try:
        # Use bright red color for text annotations (more visible than orange)
        color = (255, 0, 0)  # Bright red
        
        # Draw rectangle with very thick lines
        # Outer rectangle (thick border)
        draw.rectangle([x1-2, y1-2, x2+2, y2+2], outline=(0, 0, 0), width=6)  # Black border
        # Inner rectangle (colored)
        draw.rectangle([x1, y1, x2, y2], outline=color, width=4)  # Red border
        
        # Draw label with better visibility
        label_text = f"TEXT#{annotation_index} {text_content[:20]}..."
        
        # Calculate label position (above the text)
        label_x = x1
        label_y = y1 - 25
        
        # Draw label background with better contrast
        bbox_text = draw.textbbox((label_x, label_y), label_text, font=font_medium)
        # Draw black outline first
        draw.rectangle([bbox_text[0]-1, bbox_text[1]-1, bbox_text[2]+1, bbox_text[3]+1], fill=(0, 0, 0))
        # Then draw colored background
        draw.rectangle(bbox_text, fill=color)
        draw.text((label_x, label_y), label_text, fill="white", font=font_medium)
        
        logger.info(f"Drew enhanced text annotation {annotation_index} for font {text_content[:20]} at {x1, y1, x2, y2}")
        
    except Exception as e:
        logger.error(f"Error drawing enhanced text annotation: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")

def draw_combined_legend(draw, graphic_annotations, text_annotations, font_medium):
    """Draw combined legend for graphics and text"""
    
    try:
        # Get image size from draw object
        image_size = draw.im.size
        
        legend_x = 10
        legend_y = image_size[1] - 150
        
        # Draw legend background
        legend_width = 300
        legend_height = 140
        draw.rectangle([legend_x, legend_y, legend_x + legend_width, legend_y + legend_height], 
                      fill="white", outline="black", width=2)
        
        # Draw title
        title = "AI Analysis Legend"
        draw.text((legend_x + 5, legend_y + 5), title, fill="black", font=font_medium)
        
        y_offset = 30
        
        # Graphics section
        if graphic_annotations:
            draw.text((legend_x + 5, legend_y + y_offset), "Graphics:", fill="black", font=font_medium)
            y_offset += 15
            
            for annotation in graphic_annotations[:5]:  # Show first 5
                ai_data = annotation.get("ai_data", {})
                graphic_type = ai_data.get("graphic_type", "unknown")
                color = get_graphic_type_color_pil(graphic_type)
                
                # Draw color indicator
                draw.rectangle([legend_x + 5, legend_y + y_offset, legend_x + 15, legend_y + y_offset + 8], 
                              fill=color)
                
                # Draw text
                label = f"#{annotation['index']}: {graphic_type}"
                brand = ai_data.get("brand_company")
                if brand:
                    label += f" ({brand})"
                
                draw.text((legend_x + 20, legend_y + y_offset), label, fill="black", font=font_medium)
                y_offset += 12
        
        # Text section
        if text_annotations:
            y_offset += 5
            draw.text((legend_x + 5, legend_y + y_offset), "Text Elements:", fill="black", font=font_medium)
            y_offset += 15
            
            for annotation in text_annotations[:5]:  # Show first 5
                text_content = annotation.get("text", "")
                
                # Draw color indicator (red for text)
                draw.rectangle([legend_x + 5, legend_y + y_offset, legend_x + 15, legend_y + y_offset + 8], 
                              fill=(255, 0, 0))
                
                # Draw text
                label = f"T#{annotation['index']}: {text_content[:15]}..."
                draw.text((legend_x + 20, legend_y + y_offset), label, fill="black", font=font_medium)
                y_offset += 12
        
    except Exception as e:
        logger.error(f"Error drawing combined legend: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")

# Keep existing functions for backward compatibility
def generate_visual_report(pdf_path, output_path, analysis_results):
    """Legacy function for backward compatibility"""
    logger.warning("Using legacy visual report function. Consider using generate_visual_report_with_ai_graphics instead.")
    return generate_visual_report_with_ai_graphics(pdf_path, output_path, "legacy_key")

def create_detailed_report_pdf(pdf_path, output_path, analysis_results):
    """Legacy function for backward compatibility"""
    logger.warning("Using legacy detailed report function. Consider using create_detailed_report_with_ai_graphics instead.")
    return create_detailed_report_with_ai_graphics(pdf_path, output_path, "legacy_key") 