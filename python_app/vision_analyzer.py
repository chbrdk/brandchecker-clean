import os
import json
import logging
import base64
import requests
from PIL import Image
import io
import tempfile
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_image_with_gpt_vision(image_path, openai_api_key=None):
    """
    Analyze image using GPT Vision API for content, contrast, colors, depth, perspective, people, and overall impression
    
    Args:
        image_path: Path to the image file
        openai_api_key: OpenAI API key (if None, will try to get from environment)
    
    Returns:
        dict: Analysis results with detailed insights
    """
    
    if not openai_api_key:
        openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if not openai_api_key:
        return {"error": "OpenAI API key not provided"}
    
    try:
        # Read and encode image
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Determine image format
        image_format = os.path.splitext(image_path)[1].lower()
        if image_format in ['.jpg', '.jpeg']:
            mime_type = "image/jpeg"
        elif image_format == '.png':
            mime_type = "image/png"
        elif image_format == '.gif':
            mime_type = "image/gif"
        elif image_format == '.webp':
            mime_type = "image/webp"
        else:
            mime_type = "image/jpeg"  # Default fallback
        
        # Prepare the analysis prompt
        analysis_prompt = """
        Analysiere dieses Bild detailliert für eine Brand-Analyse. Bitte bewerte folgende Aspekte:

        1. **Inhalt & Komposition:**
           - Was ist das Hauptmotiv des Bildes?
           - Wie ist die Bildkomposition aufgebaut?
           - Welche visuellen Elemente dominieren?

        2. **Kontrast & Helligkeit:**
           - Wie ist der Kontrast zwischen hellen und dunklen Bereichen?
           - Ist das Bild eher hell, dunkel oder ausgewogen?
           - Gibt es überbelichtete oder unterbelichtete Bereiche?

        3. **Farbgebung:**
           - Welche Farben dominieren im Bild?
           - Ist die Farbpalette warm, kalt oder neutral?
           - Gibt es auffällige Akzentfarben?
           - Wie ist die Farbharmonie?

        4. **Fototiefe & Schärfe:**
           - Wie ist die Schärfentiefe (Tiefenschärfe)?
           - Ist das Bild scharf oder unscharf?
           - Gibt es Unschärfe-Effekte (Bokeh)?

        5. **Perspektive & Blickwinkel:**
           - Aus welcher Perspektive wurde das Bild aufgenommen?
           - Gibt es interessante Blickwinkel oder Kamerapositionen?
           - Wie ist die räumliche Tiefe dargestellt?

        6. **Personen & Emotionen:**
           - Sind Personen im Bild zu sehen?
           - Welche Emotionen oder Stimmungen werden vermittelt?
           - Wie ist die Körpersprache und Mimik?

        7. **Ausstrahlung & Stimmung:**
           - Welche Gesamtstimmung vermittelt das Bild?
           - Ist es professionell, freundlich, seriös, modern, etc.?
           - Welche Markenwerte könnten damit vermittelt werden?

        8. **Technische Qualität:**
           - Wie ist die Bildqualität?
           - Gibt es technische Mängel?
           - Ist das Bild für professionelle Nutzung geeignet?

        Bitte antworte strukturiert in JSON-Format mit folgenden Feldern:
        {
            "content_analysis": {
                "main_subject": "...",
                "composition": "...",
                "dominant_elements": [...]
            },
            "contrast_analysis": {
                "contrast_level": "high/medium/low",
                "brightness": "bright/balanced/dark",
                "exposure_issues": [...]
            },
            "color_analysis": {
                "dominant_colors": [...],
                "color_temperature": "warm/cool/neutral",
                "accent_colors": [...],
                "color_harmony": "good/moderate/poor"
            },
            "depth_analysis": {
                "depth_of_field": "shallow/medium/deep",
                "sharpness": "sharp/moderate/soft",
                "bokeh_effects": true/false
            },
            "perspective_analysis": {
                "camera_angle": "...",
                "viewpoint": "...",
                "spatial_depth": "good/moderate/poor"
            },
            "people_analysis": {
                "people_present": true/false,
                "emotions": [...],
                "body_language": "..."
            },
            "mood_analysis": {
                "overall_mood": "...",
                "brand_values": [...],
                "professional_impression": "high/medium/low"
            },
            "technical_quality": {
                "image_quality": "excellent/good/moderate/poor",
                "technical_issues": [...],
                "professional_suitability": "high/medium/low"
            },
            "recommendations": {
                "strengths": [...],
                "improvements": [...],
                "brand_alignment": "..."
            }
        }
        """
        
        # Prepare the request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }
        
        payload = {
            "model": "gpt-4o",  # Use GPT-4o for vision capabilities
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": analysis_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.3
        }
        
        # Make the API request
        logger.info("Sending request to OpenAI Vision API...")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Try to parse JSON response
            try:
                analysis_result = json.loads(content)
                logger.info("Successfully analyzed image with GPT Vision")
                return {
                    "success": True,
                    "analysis": analysis_result,
                    "raw_response": content
                }
            except json.JSONDecodeError:
                logger.warning("GPT Vision response is not valid JSON, returning raw text")
                return {
                    "success": True,
                    "analysis": {"raw_analysis": content},
                    "raw_response": content
                }
        else:
            logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
            return {
                "error": f"OpenAI API error: {response.status_code}",
                "details": response.text
            }
            
    except Exception as e:
        logger.error(f"Error in GPT Vision analysis: {e}")
        return {"error": str(e)}

def extract_and_analyze_images_from_pdf(pdf_path, openai_api_key=None):
    """
    Extract images from PDF and analyze each with GPT Vision
    Uses multiple extraction methods to find all visual content
    
    Args:
        pdf_path: Path to the PDF file
        openai_api_key: OpenAI API key
    
    Returns:
        dict: Analysis results for all images
    """
    
    try:
        import fitz  # PyMuPDF
        
        # Extract images from PDF using multiple methods
        doc = fitz.open(pdf_path)
        image_analyses = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            logger.info(f"Processing page {page_num+1} for images...")
            
            # Method 1: Direct image extraction
            image_list = page.get_images()
            logger.info(f"Found {len(image_list)} direct images on page {page_num+1}")
            
            for img_index, img in enumerate(image_list):
                try:
                    logger.info(f"Processing direct image {img_index+1} on page {page_num+1}...")
                    
                    # Get image data
                    xref = img[0]
                    logger.info(f"Image xref: {xref}")
                    pix = fitz.Pixmap(doc, xref)
                    logger.info(f"Pixmap created: {pix.width}x{pix.height}, colorspace: {pix.n}, alpha: {pix.alpha}")
                    
                    # Convert to PIL Image - support CMYK and other colorspaces
                    logger.info(f"Converting pixmap to PNG...")
                    
                    # Convert CMYK to RGB if needed
                    if pix.n == 4:  # CMYK
                        logger.info(f"Converting CMYK to RGB...")
                        # Create RGB pixmap from CMYK
                        rgb_pix = fitz.Pixmap(fitz.csRGB, pix)
                        img_data = rgb_pix.tobytes("png")
                        rgb_pix = None
                    else:
                        img_data = pix.tobytes("png")
                    
                    pil_image = Image.open(io.BytesIO(img_data))
                    logger.info(f"PIL Image created: {pil_image.size}, mode: {pil_image.mode}")
                    
                    # Save temporary image
                    temp_dir = tempfile.mkdtemp()
                    temp_image_path = os.path.join(temp_dir, f"page_{page_num+1}_img_{img_index+1}.png")
                    pil_image.save(temp_image_path)
                    logger.info(f"Temporary image saved: {temp_image_path}")
                    
                    # Analyze with GPT Vision
                    logger.info(f"Analyzing direct image {img_index+1} from page {page_num+1}...")
                    analysis = analyze_image_with_gpt_vision(temp_image_path, openai_api_key)
                    logger.info(f"Vision analysis result: {analysis}")
                    
                    # Add metadata
                    analysis["metadata"] = {
                        "page_number": page_num + 1,
                        "image_index": img_index + 1,
                        "image_size": pil_image.size,
                        "image_format": "PNG",
                        "extraction_method": "direct",
                        "original_colorspace": pix.n,
                        "converted_from_cmyk": pix.n == 4
                    }
                    
                    image_analyses.append(analysis)
                    logger.info(f"Added analysis to results. Total analyses: {len(image_analyses)}")
                    
                    # Clean up
                    shutil.rmtree(temp_dir)
                        
                    pix = None
                    
                except Exception as e:
                    logger.error(f"Error processing direct image {img_index+1} on page {page_num+1}: {e}")
                    logger.error(f"Exception type: {type(e)}")
                    import traceback
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    image_analyses.append({
                        "error": f"Error processing direct image: {str(e)}",
                        "metadata": {
                            "page_number": page_num + 1,
                            "image_index": img_index + 1,
                            "extraction_method": "direct"
                        }
                    })
            
            # Method 2: Render page as image and analyze
            if len(image_list) == 0:  # Only if no direct images found
                try:
                    logger.info(f"No direct images found on page {page_num+1}, rendering page as image...")
                    
                    # Render page as image
                    mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
                    pix = page.get_pixmap(matrix=mat)
                    img_data = pix.tobytes("png")
                    pil_image = Image.open(io.BytesIO(img_data))
                    
                    # Save temporary image
                    temp_dir = tempfile.mkdtemp()
                    temp_image_path = os.path.join(temp_dir, f"page_{page_num+1}_rendered.png")
                    pil_image.save(temp_image_path)
                    
                    # Analyze with GPT Vision
                    logger.info(f"Analyzing rendered page {page_num+1}...")
                    analysis = analyze_image_with_gpt_vision(temp_image_path, openai_api_key)
                    
                    # Add metadata
                    analysis["metadata"] = {
                        "page_number": page_num + 1,
                        "image_index": 0,
                        "image_size": pil_image.size,
                        "image_format": "PNG",
                        "extraction_method": "page_render"
                    }
                    
                    image_analyses.append(analysis)
                    
                    # Clean up
                    shutil.rmtree(temp_dir)
                    pix = None
                    
                except Exception as e:
                    logger.error(f"Error rendering page {page_num+1} as image: {e}")
                    image_analyses.append({
                        "error": f"Error rendering page as image: {str(e)}",
                        "metadata": {
                            "page_number": page_num + 1,
                            "image_index": 0,
                            "extraction_method": "page_render"
                        }
                    })
        
        doc.close()
        
        logger.info(f"Vision analysis completed: {len(image_analyses)} images processed")
        
        return {
            "success": True,
            "total_images": len(image_analyses),
            "image_analyses": image_analyses,
            "summary": {
                "successful_analyses": len([a for a in image_analyses if "error" not in a]),
                "failed_analyses": len([a for a in image_analyses if "error" in a])
            }
        }
        
    except Exception as e:
        logger.error(f"Error extracting and analyzing images from PDF: {e}")
        return {"error": str(e)}

def analyze_single_image(image_path, openai_api_key=None):
    """
    Analyze a single image file with GPT Vision
    
    Args:
        image_path: Path to the image file
        openai_api_key: OpenAI API key
    
    Returns:
        dict: Analysis results
    """
    
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return {"error": f"Image file not found: {image_path}"}
        
        # Check if it's a valid image
        try:
            with Image.open(image_path) as img:
                img.verify()
        except Exception:
            return {"error": f"Invalid image file: {image_path}"}
        
        # Analyze with GPT Vision
        analysis = analyze_image_with_gpt_vision(image_path, openai_api_key)
        
        # Add metadata
        with Image.open(image_path) as img:
            analysis["metadata"] = {
                "image_size": img.size,
                "image_format": img.format,
                "image_mode": img.mode
            }
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing single image: {e}")
        return {"error": str(e)}
