import os
import json
import logging
import numpy as np
from collections import defaultdict, Counter
import fitz  # PyMuPDF
import pdfplumber
from PIL import Image
import cv2
import io

# Optional imports - will be None if not available
try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import pikepdf
except ImportError:
    pikepdf = None

try:
    import pdfrw
except ImportError:
    pdfrw = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_pdf_with_multiple_libraries(pdf_path):
    """Analyze PDF using multiple libraries for maximum detail extraction"""
    
    enhanced_data = {
        "pymupdf_analysis": {},
        "pdfplumber_analysis": {},
        "pypdf_analysis": {},
        "image_analysis": {},
        "combined_results": {}
    }
    
    try:
        logger.info("Starting enhanced PDF analysis with multiple libraries...")
        
        # Method 1: PyMuPDF detailed analysis
        enhanced_data["pymupdf_analysis"] = analyze_with_pymupdf(pdf_path)
        
        # Method 2: pdfplumber detailed analysis
        enhanced_data["pdfplumber_analysis"] = analyze_with_pdfplumber(pdf_path)
        
        # Method 3: pypdf detailed analysis (if available)
        if pypdf is not None:
            enhanced_data["pypdf_analysis"] = analyze_with_pypdf(pdf_path)
        else:
            enhanced_data["pypdf_analysis"] = {"error": "pypdf not available"}
        
        # Method 4: pikepdf detailed analysis (if available)
        if pikepdf is not None:
            enhanced_data["pikepdf_analysis"] = analyze_with_pikepdf(pdf_path)
        else:
            enhanced_data["pikepdf_analysis"] = {"error": "pikepdf not available"}
        
        # Method 5: pdfrw detailed analysis (if available)
        if pdfrw is not None:
            enhanced_data["pdfrw_analysis"] = analyze_with_pdfrw(pdf_path)
        else:
            enhanced_data["pdfrw_analysis"] = {"error": "pdfrw not available"}
        
        # Method 6: Image-based analysis
        enhanced_data["image_analysis"] = analyze_as_images(pdf_path)
        
        # Combine all results
        enhanced_data["combined_results"] = combine_analysis_results(enhanced_data)
        
        return enhanced_data
        
    except Exception as e:
        logger.error(f"Error in enhanced PDF analysis: {e}")
        return enhanced_data

def analyze_with_pymupdf(pdf_path):
    """Detailed PyMuPDF analysis with all available methods"""
    
    try:
        doc = fitz.open(pdf_path)
        pymupdf_data = {
            "pages": [],
            "document_info": {},
            "metadata": {},
            "content_streams": [],
            "resources": {}
        }
        
        # Get document info
        pymupdf_data["document_info"] = {
            "title": doc.metadata.get("title", ""),
            "author": doc.metadata.get("author", ""),
            "subject": doc.metadata.get("subject", ""),
            "creator": doc.metadata.get("creator", ""),
            "producer": doc.metadata.get("producer", ""),
            "creation_date": doc.metadata.get("creationDate", ""),
            "modification_date": doc.metadata.get("modDate", "")
        }
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_data = {
                "page_number": page_num + 1,
                "rect": [page.rect.x0, page.rect.y0, page.rect.x1, page.rect.y1],
                "rotation": page.rotation,
                "images": [],
                "drawings": [],
                "text_blocks": [],
                "annotations": [],
                "links": [],
                "form_fields": [],
                "content_stream": "",
                "resources": {}
            }
            
            # Extract all images with detailed info
            image_list = page.get_images()
            for img_index, img in enumerate(image_list):
                try:
                    img_rect = page.get_image_bbox(img)
                    if img_rect:
                        img_info = {
                            "index": img_index,
                            "rect": [img_rect.x0, img_rect.y0, img_rect.x1, img_rect.y1],
                            "width": img[2],
                            "height": img[3],
                            "colorspace": img[4],
                            "bpc": img[5],
                            "name": img[7] if len(img) > 7 else "",
                            "type": "image"
                        }
                        page_data["images"].append(img_info)
                except Exception as e:
                    logger.warning(f"Error processing image {img_index}: {e}")
            
            # Extract all drawings with detailed info
            drawings = page.get_drawings()
            for drawing in drawings:
                drawing_info = {
                    "rect": drawing.get("rect", []),
                    "items": len(drawing.get("items", [])),
                    "stroke": drawing.get("stroke", {}),
                    "fill": drawing.get("fill", {}),
                    "type": "drawing"
                }
                page_data["drawings"].append(drawing_info)
            
            # Extract text with detailed info
            text_dict = page.get_text("rawdict")
            for block in text_dict.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text_info = {
                                "text": span.get("text", ""),
                                "bbox": [float(x) for x in span.get("bbox", [])],
                                "font": span.get("font", ""),
                                "size": float(span.get("size", 0)),
                                "color": int(span.get("color", 0)),
                                "flags": int(span.get("flags", 0)),
                                "type": "text"
                            }
                            page_data["text_blocks"].append(text_info)
            
            # Extract annotations
            annotations = page.annots()
            for annot in annotations:
                annot_info = {
                    "type": annot.type[1],
                    "rect": [annot.rect.x0, annot.rect.y0, annot.rect.x1, annot.rect.y1],
                    "content": annot.content,
                    "flags": annot.flags
                }
                page_data["annotations"].append(annot_info)
            
            # Extract links
            links = page.get_links()
            for link in links:
                link_info = {
                    "kind": link.get("kind", ""),
                    "uri": link.get("uri", ""),
                    "from": [float(link["from"].x0), float(link["from"].y0), float(link["from"].x1), float(link["from"].y1)]
                }
                page_data["links"].append(link_info)
            
            # Extract form fields
            form_fields = page.widgets()
            for field in form_fields:
                field_info = {
                    "field_type": field.field_type,
                    "field_name": field.field_name,
                    "rect": [field.rect.x0, field.rect.y0, field.rect.x1, field.rect.y1]
                }
                page_data["form_fields"].append(field_info)
            
            # Get content stream (raw PDF commands)
            try:
                page_data["content_stream"] = page.get_contents()
            except:
                page_data["content_stream"] = ""
            
            pymupdf_data["pages"].append(page_data)
        
        doc.close()
        return pymupdf_data
        
    except Exception as e:
        logger.error(f"Error in PyMuPDF analysis: {e}")
        return {}

def analyze_with_pdfplumber(pdf_path):
    """Detailed pdfplumber analysis"""
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pdfplumber_data = {
                "pages": [],
                "metadata": pdf.metadata
            }
            
            for page_num, page in enumerate(pdf.pages):
                page_data = {
                    "page_number": page_num + 1,
                    "width": page.width,
                    "height": page.height,
                    "images": [],
                    "shapes": [],
                    "text_blocks": [],
                    "lines": [],
                    "words": [],
                    "chars": []
                }
                
                # Extract images
                if page.images:
                    for img in page.images:
                        img_info = {
                            "x0": img["x0"],
                            "y0": img["y0"],
                            "x1": img["x1"],
                            "y1": img["y1"],
                            "width": img["width"],
                            "height": img["height"],
                            "type": img.get("name", "unknown")
                        }
                        page_data["images"].append(img_info)
                
                            # Extract shapes (if available)
            try:
                if hasattr(page, 'shapes') and page.shapes:
                    for shape in page.shapes:
                        shape_info = {
                            "x0": float(shape["x0"]),
                            "y0": float(shape["y0"]),
                            "x1": float(shape["x1"]),
                            "y1": float(shape["y1"]),
                            "type": shape.get("type", "unknown")
                        }
                        page_data["shapes"].append(shape_info)
            except:
                pass
                
                # Extract text blocks
                text_blocks = page.extract_text_blocks()
                for block in text_blocks:
                    block_info = {
                        "text": block.get("text", ""),
                        "x0": block["x0"],
                        "y0": block["y0"],
                        "x1": block["x1"],
                        "y1": block["y1"]
                    }
                    page_data["text_blocks"].append(block_info)
                
                # Extract lines
                lines = page.lines
                for line in lines:
                    line_info = {
                        "x0": line["x0"],
                        "y0": line["y0"],
                        "x1": line["x1"],
                        "y1": line["y1"],
                        "width": line["width"],
                        "height": line["height"]
                    }
                    page_data["lines"].append(line_info)
                
                # Extract words
                words = page.extract_words()
                for word in words:
                    word_info = {
                        "text": word["text"],
                        "x0": word["x0"],
                        "y0": word["y0"],
                        "x1": word["x1"],
                        "y1": word["y1"],
                        "fontname": word.get("fontname", ""),
                        "size": word.get("size", 0)
                    }
                    page_data["words"].append(word_info)
                
                # Extract characters
                chars = page.chars
                for char in chars:
                    char_info = {
                        "text": char["text"],
                        "x0": char["x0"],
                        "y0": char["y0"],
                        "x1": char["x1"],
                        "y1": char["y1"],
                        "fontname": char.get("fontname", ""),
                        "size": char.get("size", 0),
                        "color": char.get("non_stroking_color", "")
                    }
                    page_data["chars"].append(char_info)
                
                pdfplumber_data["pages"].append(page_data)
            
            return pdfplumber_data
            
    except Exception as e:
        logger.error(f"Error in pdfplumber analysis: {e}")
        return {}

def analyze_with_pypdf(pdf_path):
    """Detailed pypdf analysis"""
    
    if pypdf is None:
        return {"error": "pypdf not available"}
    
    try:
        with open(pdf_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            pypdf_data = {
                "pages": [],
                "metadata": reader.metadata if hasattr(reader, 'metadata') else {},
                "info": reader.info if hasattr(reader, 'info') else {},
                "is_encrypted": reader.is_encrypted if hasattr(reader, 'is_encrypted') else False,
                "number_of_pages": len(reader.pages)
            }
            
            for page_num, page in enumerate(reader.pages):
                page_data = {
                    "page_number": page_num + 1,
                    "media_box": list(page.mediabox) if page.mediabox else [],
                    "crop_box": list(page.cropbox) if page.cropbox else [],
                    "rotation": page.get("/Rotate", 0),
                    "resources": {},
                    "content_stream": "",
                    "images": [],
                    "fonts": []
                }
                
                # Extract resources
                try:
                    if "/Resources" in page:
                        resources = page["/Resources"]
                        if "/XObject" in resources:
                            xobjects = resources["/XObject"]
                            for name, obj in xobjects.items():
                                if obj.get("/Subtype") == "/Image":
                                    img_info = {
                                        "name": str(name),
                                        "width": int(obj.get("/Width", 0)),
                                        "height": int(obj.get("/Height", 0)),
                                        "color_space": str(obj.get("/ColorSpace", "")),
                                        "bits_per_component": int(obj.get("/BitsPerComponent", 0)),
                                        "filter": str(obj.get("/Filter", ""))
                                    }
                                    page_data["images"].append(img_info)
                except:
                    pass
                
                # Extract fonts
                try:
                    if "/Resources" in page and "/Font" in page["/Resources"]:
                        fonts = page["/Resources"]["/Font"]
                        for name, font in fonts.items():
                            font_info = {
                                "name": str(name),
                                "type": str(font.get("/Subtype", "")),
                                "base_font": str(font.get("/BaseFont", ""))
                            }
                            page_data["fonts"].append(font_info)
                except:
                    pass
                
                # Get content stream
                try:
                    page_data["content_stream"] = page.get_contents().get_data().decode('utf-8', errors='ignore')
                except:
                    page_data["content_stream"] = ""
                
                pypdf_data["pages"].append(page_data)
            
            return pypdf_data
            
    except Exception as e:
        logger.error(f"Error in pypdf analysis: {e}")
        return {}

def analyze_with_pikepdf(pdf_path):
    """Detailed pikepdf analysis"""
    
    if pikepdf is None:
        return {"error": "pikepdf not available"}
    
    try:
        with pikepdf.open(pdf_path) as pdf:
            pikepdf_data = {
                "pages": [],
                "metadata": dict(pdf.docinfo),
                "version": str(pdf.pdf_version),
                "is_encrypted": pdf.is_encrypted,
                "number_of_pages": len(pdf.pages)
            }
            
            for page_num, page in enumerate(pdf.pages):
                page_data = {
                    "page_number": page_num + 1,
                    "media_box": list(page.MediaBox) if page.MediaBox else [],
                    "crop_box": list(page.CropBox) if page.CropBox else [],
                    "rotation": int(page.Rotate) if page.Rotate else 0,
                    "images": [],
                    "fonts": [],
                    "content_stream": "",
                    "resources": {}
                }
                
                # Extract images from XObject
                if "/XObject" in page.Contents:
                    xobjects = page.Contents["/XObject"]
                    for name, obj in xobjects.items():
                        if obj.get("/Subtype") == "/Image":
                            img_info = {
                                "name": str(name),
                                "width": int(obj.get("/Width", 0)),
                                "height": int(obj.get("/Height", 0)),
                                "color_space": str(obj.get("/ColorSpace", "")),
                                "bits_per_component": int(obj.get("/BitsPerComponent", 0)),
                                "filter": str(obj.get("/Filter", ""))
                            }
                            page_data["images"].append(img_info)
                
                # Extract fonts
                if "/Font" in page.Contents:
                    fonts = page.Contents["/Font"]
                    for name, font in fonts.items():
                        font_info = {
                            "name": str(name),
                            "type": str(font.get("/Subtype", "")),
                            "base_font": str(font.get("/BaseFont", ""))
                        }
                        page_data["fonts"].append(font_info)
                
                # Get content stream
                try:
                    page_data["content_stream"] = page.Contents.read_bytes().decode('utf-8', errors='ignore')
                except:
                    page_data["content_stream"] = ""
                
                pikepdf_data["pages"].append(page_data)
            
            return pikepdf_data
            
    except Exception as e:
        logger.error(f"Error in pikepdf analysis: {e}")
        return {}

def analyze_with_pdfrw(pdf_path):
    """Detailed pdfrw analysis"""
    
    if pdfrw is None:
        return {"error": "pdfrw not available"}
    
    try:
        pdf = pdfrw.PdfReader(pdf_path)
        pdfrw_data = {
            "pages": [],
            "metadata": pdf.Info,
            "version": pdf.Version,
            "number_of_pages": len(pdf.pages)
        }
        
        for page_num, page in enumerate(pdf.pages):
            page_data = {
                "page_number": page_num + 1,
                "media_box": list(page.MediaBox) if page.MediaBox else [],
                "crop_box": list(page.CropBox) if page.CropBox else [],
                "rotation": int(page.Rotate) if page.Rotate else 0,
                "images": [],
                "fonts": [],
                "content_stream": "",
                "resources": {}
            }
            
            # Extract resources
            if "/Resources" in page:
                resources = page["/Resources"]
                if "/XObject" in resources:
                    xobjects = resources["/XObject"]
                    for name, obj in xobjects.items():
                        if obj.get("/Subtype") == "/Image":
                            img_info = {
                                "name": str(name),
                                "width": int(obj.get("/Width", 0)),
                                "height": int(obj.get("/Height", 0)),
                                "color_space": str(obj.get("/ColorSpace", "")),
                                "bits_per_component": int(obj.get("/BitsPerComponent", 0))
                            }
                            page_data["images"].append(img_info)
                
                if "/Font" in resources:
                    fonts = resources["/Font"]
                    for name, font in fonts.items():
                        font_info = {
                            "name": str(name),
                            "type": str(font.get("/Subtype", "")),
                            "base_font": str(font.get("/BaseFont", ""))
                        }
                        page_data["fonts"].append(font_info)
            
            # Get content stream
            try:
                if "/Contents" in page:
                    contents = page["/Contents"]
                    if hasattr(contents, 'read'):
                        page_data["content_stream"] = contents.read().decode('utf-8', errors='ignore')
                    else:
                        page_data["content_stream"] = str(contents)
            except:
                page_data["content_stream"] = ""
            
            pdfrw_data["pages"].append(page_data)
        
        return pdfrw_data
        
    except Exception as e:
        logger.error(f"Error in pdfrw analysis: {e}")
        return {}

def analyze_as_images(pdf_path):
    """Convert PDF pages to images and analyze them"""
    
    try:
        # Convert PDF to images
        doc = fitz.open(pdf_path)
        image_data = {
            "pages": []
        }
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Convert page to image
            mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            pil_image = Image.open(io.BytesIO(img_data))
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Analyze image
            page_image_data = {
                "page_number": page_num + 1,
                "width": cv_image.shape[1],
                "height": cv_image.shape[0],
                "channels": cv_image.shape[2],
                "contours": [],
                "edges": [],
                "color_regions": []
            }
            
            # Find contours (potential logo regions)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # Filter small contours
                    x, y, w, h = cv2.boundingRect(contour)
                    contour_info = {
                        "area": area,
                        "bbox": [x, y, x + w, y + h],
                        "width": w,
                        "height": h,
                        "aspect_ratio": w / h if h > 0 else 0
                    }
                    page_image_data["contours"].append(contour_info)
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            edge_contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in edge_contours:
                area = cv2.contourArea(contour)
                if area > 50:  # Filter small edge contours
                    x, y, w, h = cv2.boundingRect(contour)
                    edge_info = {
                        "area": area,
                        "bbox": [x, y, x + w, y + h],
                        "width": w,
                        "height": h
                    }
                    page_image_data["edges"].append(edge_info)
            
            # Color region analysis
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            
            # Define color ranges for logo colors (blue, red, etc.)
            color_ranges = {
                "blue": ([100, 50, 50], [130, 255, 255]),
                "red": ([0, 50, 50], [10, 255, 255]),
                "red2": ([170, 50, 50], [180, 255, 255])
            }
            
            for color_name, (lower, upper) in color_ranges.items():
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                color_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in color_contours:
                    area = cv2.contourArea(contour)
                    if area > 100:  # Filter small color regions
                        x, y, w, h = cv2.boundingRect(contour)
                        color_info = {
                            "color": color_name,
                            "area": area,
                            "bbox": [x, y, x + w, y + h],
                            "width": w,
                            "height": h
                        }
                        page_image_data["color_regions"].append(color_info)
            
            image_data["pages"].append(page_image_data)
        
        doc.close()
        return image_data
        
    except Exception as e:
        logger.error(f"Error in image analysis: {e}")
        return {}

def combine_analysis_results(enhanced_data):
    """Combine results from all analysis methods"""
    
    try:
        combined = {
            "total_elements": 0,
            "logo_candidates": [],
            "image_elements": [],
            "text_elements": [],
            "shape_elements": [],
            "analysis_summary": {}
        }
        
        # Count elements from different sources
        pymupdf = enhanced_data.get("pymupdf_analysis", {})
        pdfplumber = enhanced_data.get("pdfplumber_analysis", {})
        pypdf = enhanced_data.get("pypdf_analysis", {})
        image_analysis = enhanced_data.get("image_analysis", {})
        
        # Count PyMuPDF elements
        pymupdf_count = 0
        for page in pymupdf.get("pages", []):
            pymupdf_count += len(page.get("images", []))
            pymupdf_count += len(page.get("drawings", []))
            pymupdf_count += len(page.get("text_blocks", []))
        
        # Count pdfplumber elements
        pdfplumber_count = 0
        for page in pdfplumber.get("pages", []):
            pdfplumber_count += len(page.get("images", []))
            pdfplumber_count += len(page.get("shapes", []))
            pdfplumber_count += len(page.get("text_blocks", []))
        
        # Count pypdf elements
        pypdf_count = 0
        for page in pypdf.get("pages", []):
            pypdf_count += len(page.get("images", []))
            pypdf_count += len(page.get("fonts", []))
        
        # Count pikepdf elements
        pikepdf_count = 0
        pikepdf = enhanced_data.get("pikepdf_analysis", {})
        for page in pikepdf.get("pages", []):
            pikepdf_count += len(page.get("images", []))
            pikepdf_count += len(page.get("fonts", []))
        
        # Count pdfrw elements
        pdfrw_count = 0
        pdfrw = enhanced_data.get("pdfrw_analysis", {})
        for page in pdfrw.get("pages", []):
            pdfrw_count += len(page.get("images", []))
            pdfrw_count += len(page.get("fonts", []))
        
        # Count image analysis elements
        image_count = 0
        for page in image_analysis.get("pages", []):
            image_count += len(page.get("contours", []))
            image_count += len(page.get("edges", []))
            image_count += len(page.get("color_regions", []))
        
        combined["total_elements"] = pymupdf_count + pdfplumber_count + pypdf_count + pikepdf_count + pdfrw_count + image_count
        
        combined["analysis_summary"] = {
            "pymupdf_elements": pymupdf_count,
            "pdfplumber_elements": pdfplumber_count,
            "pypdf_elements": pypdf_count,
            "pikepdf_elements": pikepdf_count,
            "pdfrw_elements": pdfrw_count,
            "image_analysis_elements": image_count,
            "total_pages": len(pymupdf.get("pages", []))
        }
        
        return combined
        
    except Exception as e:
        logger.error(f"Error combining analysis results: {e}")
        return {} 