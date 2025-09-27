import os
import re
import json
import logging
import numpy as np
import colorsys
import io
import time
from collections import Counter
from flask import Flask, request, jsonify, make_response, send_file
from werkzeug.utils import secure_filename
import tempfile
import shutil

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our custom analyzers
from color_analyzer import extract_colors_from_pdf_comprehensive
from font_analyzer import extract_fonts_from_pdf_comprehensive, analyze_font_usage_patterns
from layout_analyzer import extract_layout_from_pdf_comprehensive
from image_analyzer import extract_images_from_pdf_comprehensive
from vision_analyzer import analyze_image_with_gpt_vision, extract_and_analyze_images_from_pdf, analyze_single_image
from vector_analyzer import extract_vector_graphics_from_pdf_comprehensive
from enhanced_pdf_analyzer import analyze_pdf_with_multiple_libraries
from custom_logo_detector import CustomLogoDetector
from intelligent_logo_detector import IntelligentLogoDetector
from global_graphic_detector import GlobalGraphicDetector
from visual_report_generator import generate_visual_report, create_detailed_report_pdf, generate_visual_report_with_ai_graphics, generate_visual_report_with_ai_graphics_and_text
from enhanced_ai_analyzer import EnhancedAIAnalyzer

# Import database manager
try:
    from database import db_manager
    DATABASE_AVAILABLE = True
    logger.info("Database integration enabled")
except ImportError as e:
    logger.warning(f"Database integration not available: {e}")
    DATABASE_AVAILABLE = False

# Import knowledge database manager
try:
    from knowledge_database import knowledge_db_manager
    KNOWLEDGE_DB_AVAILABLE = True
    logger.info("Knowledge database integration enabled")
except ImportError as e:
    logger.warning(f"Knowledge database integration not available: {e}")
    KNOWLEDGE_DB_AVAILABLE = False

# Import the new libraries for comprehensive analysis
try:
    import fitz  # PyMuPDF
    import cv2
    from PIL import Image
    import pdfplumber
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
except ImportError as e:
    print(f"Missing library: {e}")
    print("Please install: pip install PyMuPDF opencv-python Pillow pdfplumber scikit-learn")

app = Flask(__name__)
from flask_cors import CORS
CORS(app, origins=["http://localhost:8005", "http://localhost:3001", "http://brandchecker-app:3001", "*"], supports_credentials=True)

# OpenAI API Key - Use environment variable for security
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Brandchecker Analysis",
        "version": "3.0"
    })

@app.route('/extract-colors', methods=['POST'])
def extract_pdf_colors():
    """Extract all colors from PDF using comprehensive analysis"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)
        
        logger.info(f"Processing PDF for colors: {filename}")
        
        # Extract colors using comprehensive method
        color_analysis = extract_colors_from_pdf_comprehensive(temp_path)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        if "error" in color_analysis:
            return jsonify({"error": color_analysis["error"]}), 500
        
        return jsonify({
            "success": True,
            "filename": filename,
            "color_analysis": color_analysis
        })
        
    except Exception as e:
        logger.error(f"Error processing PDF for colors: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/extract-colors-path', methods=['POST'])
def extract_pdf_colors_by_path():
    """Extract all colors from PDF using file path - for n8n integration"""
    
    try:
        data = request.get_json()
        if not data or 'filepath' not in data:
            return jsonify({"error": "No filepath provided in JSON body"}), 400
        
        filepath = data['filepath']
        
        # Validate filepath
        if not os.path.exists(filepath):
            return jsonify({"error": f"File not found: {filepath}"}), 404
        
        if not filepath.lower().endswith('.pdf'):
            return jsonify({"error": "File must be a PDF"}), 400
        
        filename = os.path.basename(filepath)
        logger.info(f"Processing PDF for colors by path: {filepath}")
        
        # Extract colors using comprehensive method
        color_analysis = extract_colors_from_pdf_comprehensive(filepath)
        
        if "error" in color_analysis:
            return jsonify({"error": color_analysis["error"]}), 500
        
        return jsonify({
            "success": True,
            "filename": filename,
            "filepath": filepath,
            "color_analysis": color_analysis
        })
        
    except Exception as e:
        logger.error(f"Error processing PDF for colors by path: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/extract-fonts', methods=['POST'])
def extract_pdf_fonts():
    """Extract all fonts from PDF using comprehensive analysis"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)
        
        logger.info(f"Processing PDF for fonts: {filename}")
        
        # Extract fonts using comprehensive method
        font_analysis = extract_fonts_from_pdf_comprehensive(temp_path)
        
        # Get additional font insights
        font_insights = analyze_font_usage_patterns(font_analysis)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        if "error" in font_analysis:
            return jsonify({"error": font_analysis["error"]}), 500
        
        return jsonify({
            "success": True,
            "filename": filename,
            "font_analysis": font_analysis,
            "font_insights": font_insights
        })
        
    except Exception as e:
        logger.error(f"Error processing PDF for fonts: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/extract-layout', methods=['POST'])
def extract_pdf_layout():
    """Extract layout information from PDF using comprehensive analysis"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)
        
        logger.info(f"Processing PDF for layout analysis: {filename}")
        
        # Extract layout using comprehensive method
        layout_analysis = extract_layout_from_pdf_comprehensive(temp_path)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        if "error" in layout_analysis:
            return jsonify({"error": layout_analysis["error"]}), 500
        
        return jsonify({
            "success": True,
            "filename": filename,
            "layout_analysis": layout_analysis
        })
        
    except Exception as e:
        logger.error(f"Error processing PDF for layout analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/extract-images', methods=['POST'])
def extract_pdf_images():
    """Extract image and graphic information from PDF using comprehensive analysis"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)
        
        logger.info(f"Processing PDF for image analysis: {filename}")
        
        # Extract images using comprehensive method
        image_analysis = extract_images_from_pdf_comprehensive(temp_path)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        if "error" in image_analysis:
            return jsonify({"error": image_analysis["error"]}), 500
        
        return jsonify({
            "success": True,
            "filename": filename,
            "image_analysis": image_analysis
        })
        
    except Exception as e:
        logger.error(f"Error processing PDF for image analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze-images-vision', methods=['POST'])
def analyze_images_with_vision():
    """Analyze images from PDF using GPT Vision API for content, contrast, colors, depth, perspective, people, and mood"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Check if it's a PDF or image file
    filename_lower = file.filename.lower()
    is_pdf = filename_lower.endswith('.pdf')
    is_image = filename_lower.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))
    
    if not (is_pdf or is_image):
        return jsonify({"error": "File must be a PDF or image (JPG, PNG, GIF, WebP)"}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)
        
        logger.info(f"Processing file for GPT Vision analysis: {filename}")
        
        # Get OpenAI API key from request or environment
        openai_api_key = request.form.get('openai_api_key') or os.getenv('OPENAI_API_KEY')
        
        if not openai_api_key:
            return jsonify({"error": "OpenAI API key not provided. Please provide it in the request or set OPENAI_API_KEY environment variable."}), 400
        
        # Analyze based on file type
        if is_pdf:
            # Extract and analyze images from PDF
            vision_analysis = extract_and_analyze_images_from_pdf(temp_path, openai_api_key)
        else:
            # Analyze single image
            vision_analysis = analyze_single_image(temp_path, openai_api_key)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        if "error" in vision_analysis:
            return jsonify({"error": "Vision analysis error: " + str(vision_analysis["error"])}), 500
        
        return jsonify(vision_analysis)
        
    except Exception as e:
        logger.error(f"Error in vision analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/extract-vectors', methods=['POST'])
def extract_pdf_vectors():
    """Extract vector graphics, logos, and illustrations from PDF using comprehensive analysis"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)
        
        logger.info(f"Processing PDF for vector analysis: {filename}")
        
        # Extract vectors using comprehensive method
        vector_analysis = extract_vector_graphics_from_pdf_comprehensive(temp_path)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        if "error" in vector_analysis:
            return jsonify({"error": vector_analysis["error"]}), 500
        
        return jsonify({
            "success": True,
            "filename": filename,
            "vector_analysis": vector_analysis
        })
        
    except Exception as e:
        logger.error(f"Error processing PDF for vector analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate-visual-report', methods=['POST'])
def generate_visual_pdf_report():
    """Generate a visual PDF report with annotations showing all detected elements"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)
        
        logger.info(f"Generating visual report for: {filename}")
        
        # Perform complete analysis first
        color_analysis = extract_colors_from_pdf_comprehensive(temp_path)
        font_analysis = extract_fonts_from_pdf_comprehensive(temp_path)
        layout_analysis = extract_layout_from_pdf_comprehensive(temp_path)
        image_analysis = extract_images_from_pdf_comprehensive(temp_path)
        vector_analysis = extract_vector_graphics_from_pdf_comprehensive(temp_path)
        
        # Combine analysis results
        analysis_results = {
            "color_analysis": color_analysis,
            "font_analysis": font_analysis,
            "layout_analysis": layout_analysis,
            "image_analysis": image_analysis,
            "vector_analysis": vector_analysis,
            "summary": {
                "total_colors": color_analysis.get("total_colors", 0),
                "total_fonts": font_analysis.get("total_fonts", 0),
                "total_pages": layout_analysis.get("overall_stats", {}).get("total_pages", 0),
                "total_images": image_analysis.get("overall_stats", {}).get("total_images", 0),
                "total_vectors": vector_analysis.get("overall_stats", {}).get("total_vectors", 0),
                "total_usage": color_analysis.get("total_usage", 0) + font_analysis.get("total_usage", 0)
            }
        }
        
        # Generate visual report
        output_filename = f"visual_report_{filename}"
        output_path = os.path.join(temp_dir, output_filename)
        
        report_result = generate_visual_report(temp_path, analysis_results, output_path)
        
        if "error" in report_result:
            shutil.rmtree(temp_dir)
            return jsonify({"error": report_result["error"]}), 500
        
        # Read the generated PDF
        with open(output_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        # Return the PDF as response
        response = make_response(pdf_content)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{output_filename}"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating visual report: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate-detailed-report', methods=['POST'])
def generate_detailed_pdf_report():
    """Generate a detailed text-based PDF report with all analysis results"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)
        
        logger.info(f"Generating detailed report for: {filename}")
        
        # Perform complete analysis first
        color_analysis = extract_colors_from_pdf_comprehensive(temp_path)
        font_analysis = extract_fonts_from_pdf_comprehensive(temp_path)
        layout_analysis = extract_layout_from_pdf_comprehensive(temp_path)
        image_analysis = extract_images_from_pdf_comprehensive(temp_path)
        vector_analysis = extract_vector_graphics_from_pdf_comprehensive(temp_path)
        
        # Combine analysis results
        analysis_results = {
            "color_analysis": color_analysis,
            "font_analysis": font_analysis,
            "layout_analysis": layout_analysis,
            "image_analysis": image_analysis,
            "vector_analysis": vector_analysis,
            "summary": {
                "total_colors": color_analysis.get("total_colors", 0),
                "total_fonts": font_analysis.get("total_fonts", 0),
                "total_pages": layout_analysis.get("overall_stats", {}).get("total_pages", 0),
                "total_images": image_analysis.get("overall_stats", {}).get("total_images", 0),
                "total_vectors": vector_analysis.get("overall_stats", {}).get("total_vectors", 0),
                "total_usage": color_analysis.get("total_usage", 0) + font_analysis.get("total_usage", 0)
            }
        }
        
        # Generate detailed report
        output_filename = f"detailed_report_{filename}"
        output_path = os.path.join(temp_dir, output_filename)
        
        report_result = create_detailed_report_pdf(analysis_results, output_path)
        
        if "error" in report_result:
            shutil.rmtree(temp_dir)
            return jsonify({"error": report_result["error"]}), 500
        
        # Read the generated PDF
        with open(output_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        # Return the PDF as response
        response = make_response(pdf_content)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{output_filename}"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating detailed report: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/enhanced-analysis', methods=['POST'])
def enhanced_analysis():
    """Enhanced PDF analysis using multiple libraries for maximum detail extraction"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Save uploaded file temporarily
        temp_path = os.path.join(tempfile.gettempdir(), file.filename)
        file.save(temp_path)
        
        # Perform enhanced analysis
        enhanced_analysis = analyze_pdf_with_multiple_libraries(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({"enhanced_analysis": enhanced_analysis})
        
    except Exception as e:
        logger.error(f"Error in enhanced analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/custom-logo-detection', methods=['POST'])
def custom_logo_detection():
    """Custom logo detection using proprietary algorithms"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Save uploaded file temporarily
        temp_path = os.path.join(tempfile.gettempdir(), file.filename)
        file.save(temp_path)
        
        # Initialize custom logo detector
        detector = CustomLogoDetector()
        
        # Perform custom logo detection
        logo_detection = detector.detect_logos_in_pdf(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({"custom_logo_detection": logo_detection})
        
    except Exception as e:
        logger.error(f"Error in custom logo detection: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/intelligent-logo-detection', methods=['POST'])
def intelligent_logo_detection():
    """Intelligent logo region detection with screenshot generation"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Save uploaded file temporarily
        temp_path = os.path.join(tempfile.gettempdir(), file.filename)
        file.save(temp_path)
        
        # Initialize intelligent logo detector
        detector = IntelligentLogoDetector()
        
        # Perform intelligent logo region detection
        logo_regions = detector.detect_logo_regions(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({"intelligent_logo_detection": logo_regions})
        
    except Exception as e:
        logger.error(f"Error in intelligent logo detection: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/global-graphic-detection', methods=['POST'])
def global_graphic_detection():
    """Global graphic/illustration detection with OpenAI AI analysis"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Save uploaded file temporarily
        temp_path = os.path.join(tempfile.gettempdir(), file.filename)
        file.save(temp_path)
        
        # OpenAI API Key - Use environment variable for security
        openai_api_key = os.getenv('OPENAI_API_KEY', '')
        
        # Initialize global graphic detector
        detector = GlobalGraphicDetector(openai_api_key)
        
        # Perform global graphic detection with AI analysis
        graphic_detection = detector.detect_all_graphics(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({"global_graphic_detection": graphic_detection})
        
    except Exception as e:
        logger.error(f"Error in global graphic detection: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate-ai-visual-report', methods=['POST'])
def generate_ai_visual_report():
    """Generate visual report with AI-analyzed graphics marked"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join('/app/shared', filename)
        file.save(file_path)
        
        # Generate report filename
        report_filename = f"ai_visual_report_{os.path.splitext(filename)[0]}.pdf"
        report_path = os.path.join('/app/shared/reports', report_filename)
        
        # Generate visual report
        result = generate_visual_report_with_ai_graphics(
            file_path, report_path, OPENAI_API_KEY
        )
        
        if "error" in result:
            return jsonify({"error": result["error"]}), 500
        
        return jsonify({
            "visual_report": {
                "report_path": report_path,
                "graphic_analysis": result.get("graphic_analysis", {}),
                "report_generated": True
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-ai-visual-report-with-text', methods=['POST'])
def generate_ai_visual_report_with_text():
    """Generate visual report with AI-analyzed graphics AND text marked"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join('/app/shared', filename)
        file.save(file_path)
        
        # Step 1: Detect graphics with AI analysis
        from global_graphic_detector import GlobalGraphicDetector
        detector = GlobalGraphicDetector(OPENAI_API_KEY)
        graphic_results = detector.detect_all_graphics(file_path)
        
        if "error" in graphic_results:
            return jsonify({"error": graphic_results["error"]}), 500
        
        # Step 2: Extract text elements using PyMuPDF
        from visual_report_generator import extract_text_elements
        text_results = extract_text_elements(file_path)
        
        # Step 3: Generate visual report with both graphics and text marked
        from visual_report_generator import generate_visual_report_with_ai_graphics_and_text
        report_path = generate_visual_report_with_ai_graphics_and_text(file_path, graphic_results, text_results)
        
        if not report_path:
            return jsonify({"error": "Failed to generate visual report"}), 500
        
        return jsonify({
            "visual_report_with_text": {
                "report_path": report_path,
                "graphic_analysis": graphic_results,
                "text_analysis": text_results,
                "report_generated": True
            }
        })
        
    except Exception as e:
        logger.error(f"Error generating AI visual report with text: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate-ai-detailed-report', methods=['POST'])
def generate_ai_detailed_report():
    """Generate detailed text report with AI graphics analysis"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Save uploaded file temporarily
        temp_path = os.path.join(tempfile.gettempdir(), file.filename)
        file.save(temp_path)
        
        # OpenAI API Key - Use environment variable for security
        openai_api_key = os.getenv('OPENAI_API_KEY', '')
        
        # Generate output path in shared volume
        output_filename = f"ai_detailed_report_{file.filename}.txt"
        output_path = os.path.join("/app/shared/reports", output_filename)
        
        # Ensure reports directory exists
        os.makedirs("/app/shared/reports", exist_ok=True)
        
        # Generate AI detailed report
        from visual_report_generator import create_detailed_report_with_ai_graphics
        report_result = create_detailed_report_with_ai_graphics(temp_path, output_path, openai_api_key)
        
        # Clean up input file
        os.remove(temp_path)
        
        if "error" in report_result:
            return jsonify({"error": report_result["error"]}), 500
        
        # Read report content
        with open(output_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        # Return success with download link
        return jsonify({
            "ai_detailed_report": {
                "report_path": output_path,
                "filename": output_filename,
                "download_url": f"/download-report/{output_filename}",
                "content": report_content,
                "graphic_analysis": report_result.get("graphic_analysis", {})
            }
        })
        
    except Exception as e:
        logger.error(f"Error generating AI detailed report: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/comprehensive-ai-analysis', methods=['POST'])
def comprehensive_ai_analysis():
    """Comprehensive AI analysis including graphics, fonts, and layout"""
    
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        # Initialize OpenAI API key - Use environment variable for security
        openai_api_key = os.getenv('OPENAI_API_KEY', '')
        
        # Perform comprehensive AI analysis
        analyzer = EnhancedAIAnalyzer(openai_api_key)
        comprehensive_results = analyzer.analyze_pdf_comprehensive(temp_path)
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        if "error" in comprehensive_results:
            return jsonify({"error": comprehensive_results["error"]}), 500
        
        return jsonify({
            "comprehensive_ai_analysis": {
                "filename": file.filename,
                "analysis_results": comprehensive_results,
                "success": True
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-comprehensive-report', methods=['POST'])
def generate_comprehensive_report():
    """Generate comprehensive report with graphics, fonts, and layout analysis"""
    
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        # Initialize OpenAI API key - Use environment variable for security
        openai_api_key = os.getenv('OPENAI_API_KEY', '')
        
        # Perform comprehensive AI analysis
        analyzer = EnhancedAIAnalyzer(openai_api_key)
        comprehensive_results = analyzer.analyze_pdf_comprehensive(temp_path)
        
        if "error" in comprehensive_results:
            return jsonify({"error": comprehensive_results["error"]}), 500
        
        # Generate comprehensive report
        output_filename = f"comprehensive_report_{file.filename}.txt"
        output_path = os.path.join("/app/shared/reports", output_filename)
        os.makedirs("/app/shared/reports", exist_ok=True)
        
        report_content = _generate_comprehensive_report_content(comprehensive_results)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        return jsonify({
            "comprehensive_report": {
                "filename": output_filename,
                "download_url": f"/download-report/{output_filename}",
                "content_preview": report_content[:500] + "..." if len(report_content) > 500 else report_content,
                "analysis_results": comprehensive_results
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def _generate_comprehensive_report_content(comprehensive_results):
    """Generate comprehensive report content"""
    
    try:
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE AI-POWERED PDF ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Executive Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 40)
        summary = comprehensive_results.get("summary", {})
        
        report.append(f"Total Pages: {summary.get('total_pages', 0)}")
        report.append(f"Graphics Found: {summary.get('graphics_summary', {}).get('total_graphics', 0)}")
        report.append(f"Fonts Found: {summary.get('fonts_summary', {}).get('total_fonts', 0)}")
        report.append(f"Font Families: {summary.get('fonts_summary', {}).get('font_families', 0)}")
        report.append("")
        
        # Graphics Analysis
        graphics = comprehensive_results.get("graphics_analysis", {})
        if "graphic_regions" in graphics:
            report.append("GRAPHICS ANALYSIS")
            report.append("=" * 40)
            report.append(f"Total Graphics: {len(graphics['graphic_regions'])}")
            
            brands = graphics.get("analysis_summary", {}).get("ai_analysis_summary", {}).get("brands_companies", [])
            if brands:
                report.append(f"Brands Found: {', '.join(brands)}")
            
            graphic_types = graphics.get("analysis_summary", {}).get("ai_analysis_summary", {}).get("graphic_types", {})
            if graphic_types:
                report.append("Graphic Types:")
                for gtype, count in graphic_types.items():
                    report.append(f"  - {gtype}: {count}")
            report.append("")
        
        # Font Analysis
        fonts = comprehensive_results.get("font_analysis", {})
        if "total_fonts" in fonts:
            report.append("FONT ANALYSIS")
            report.append("=" * 40)
            report.append("Total Fonts: " + str(fonts.get("total_fonts", "")))
            report.append(f"Font Families: {len(fonts.get('font_families', {}))}")
            
            font_families = fonts.get("font_families", {})
            if font_families:
                report.append("Font Families Found:")
                for family, count in font_families.items():
                    report.append(f"  - {family}: {count} uses")
            
            ai_fonts = fonts.get("ai_analysis", {})
            if ai_fonts:
                report.append(f"Typography Quality: {ai_fonts.get('typography_quality', 'unknown')}")
                if "typography_hierarchy" in ai_fonts:
                    report.append("Typography Hierarchy:")
                    for hierarchy in ai_fonts["typography_hierarchy"]:
                        report.append(f"  - {hierarchy}")
            report.append("")
        
        # Layout Analysis
        layout = comprehensive_results.get("layout_analysis", {})
        if "total_pages" in layout:
            report.append("LAYOUT ANALYSIS")
            report.append("=" * 40)
            report.append("Total Pages: " + str(layout.get("total_pages", "")))
            
            ai_layout = layout.get("ai_analysis", {})
            if ai_layout:
                layout_types = ai_layout.get("layout_types", [])
                if layout_types:
                    report.append(f"Layout Types: {', '.join(layout_types)}")
                
                report.append(f"Design Quality: {ai_layout.get('design_quality', 'unknown')}")
                report.append(f"Average Composition Score: {ai_layout.get('avg_composition_score', 0):.2f}")
            report.append("")
        
        # Overall Assessment
        report.append("OVERALL ASSESSMENT")
        report.append("=" * 40)
        report.append("This comprehensive analysis provides:")
        report.append("  - AI-powered graphics detection and classification")
        report.append("  - Advanced typography analysis with quality assessment")
        report.append("  - Layout structure and design quality evaluation")
        report.append("  - Brand and company identification")
        report.append("  - Detailed recommendations for improvements")
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
        
    except Exception as e:
        return f"Error generating comprehensive report: {str(e)}"

@app.route('/download-report/<filename>')
def download_report(filename):
    """Download generated report files"""
    
    try:
        report_path = os.path.join("/app/shared/reports", filename)
        
        if not os.path.exists(report_path):
            return jsonify({"error": "Report file not found"}), 404
        
        # Determine content type
        if filename.endswith('.pdf'):
            content_type = 'application/pdf'
        elif filename.endswith('.txt'):
            content_type = 'text/plain'
        else:
            content_type = 'application/octet-stream'
        
        # Return file for download
        return send_file(
            report_path,
            as_attachment=True,
            download_name=filename,
            mimetype=content_type
        )
        
    except Exception as e:
        logger.error(f"Error downloading report: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/list-reports')
def list_reports():
    """List all available reports"""
    
    try:
        reports_dir = "/app/shared/reports"
        
        if not os.path.exists(reports_dir):
            return jsonify({"reports": []})
        
        reports = []
        for filename in os.listdir(reports_dir):
            file_path = os.path.join(reports_dir, filename)
            if os.path.isfile(file_path):
                file_stats = os.stat(file_path)
                reports.append({
                    "filename": filename,
                    "size": file_stats.st_size,
                    "created": file_stats.st_ctime,
                    "download_url": f"/download-report/{filename}"
                })
        
        # Sort by creation time (newest first)
        reports.sort(key=lambda x: x["created"], reverse=True)
        
        return jsonify({"reports": reports})
        
    except Exception as e:
        logger.error(f"Error listing reports: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/extract-all', methods=['POST'])
def extract_pdf_all():
    """Extract ALL analyses from PDF: colors, fonts, layout, images, vectors, intelligent colors, design colors, color profiles"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)
        
        logger.info(f"Processing PDF for COMPLETE analysis: {filename}")
        
        # === STANDARD ANALYSES ===
        # Extract colors (standard)
        color_analysis = extract_colors_from_pdf_comprehensive(temp_path)
        
        # Extract fonts
        font_analysis = extract_fonts_from_pdf_comprehensive(temp_path)
        
        # Extract layout
        layout_analysis = extract_layout_from_pdf_comprehensive(temp_path)
        
        # Extract images
        image_analysis = extract_images_from_pdf_comprehensive(temp_path)
        
        # Extract vectors
        vector_analysis = extract_vector_graphics_from_pdf_comprehensive(temp_path)
        
        # Get font insights
        font_insights = analyze_font_usage_patterns(font_analysis)
        
        # === INTELLIGENT COLOR ANALYSES ===
        # Import the new color analysis functions
        from color_analyzer import extract_design_colors_only, extract_color_profiles, extract_colors_with_proper_color_space
        
        # Extract intelligent colors (CMYK/RGB/Pantone/RAL)
        intelligent_color_analysis = extract_colors_with_proper_color_space(temp_path)
        
        # Extract design colors (without product images)
        design_color_analysis = extract_design_colors_only(temp_path)
        
        # Extract color profiles (ICC, color spaces)
        color_profile_analysis = extract_color_profiles(temp_path)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        # Check for errors
        if "error" in color_analysis:
            return jsonify({"error": "Color analysis error: " + str(color_analysis.get("error", ""))}), 500
        
        if "error" in font_analysis:
            return jsonify({"error": "Font analysis error: " + str(font_analysis.get("error", ""))}), 500
        
        if "error" in layout_analysis:
            return jsonify({"error": "Layout analysis error: " + str(layout_analysis.get("error", ""))}), 500
        
        if "error" in image_analysis:
            return jsonify({"error": "Image analysis error: " + str(image_analysis.get("error", ""))}), 500
        
        if "error" in vector_analysis:
            return jsonify({"error": "Vector analysis error: " + str(vector_analysis.get("error", ""))}), 500
        
        return jsonify({
            "success": True,
            "filename": filename,
            "complete_analysis": {
                # Standard analyses
                "color_analysis": color_analysis,
                "font_analysis": font_analysis,
                "layout_analysis": layout_analysis,
                "image_analysis": image_analysis,
                "vector_analysis": vector_analysis,
                "font_insights": font_insights,
                
                # Intelligent color analyses
                "intelligent_color_analysis": intelligent_color_analysis,
                "design_color_analysis": design_color_analysis,
                "color_profile_analysis": color_profile_analysis,
                
                # GPT Vision analysis
                "vision_analysis": vision_analysis
            },
            "summary": {
                "total_colors": color_analysis.get("total_colors", 0),
                "total_fonts": font_analysis.get("total_fonts", 0),
                "total_pages": layout_analysis.get("overall_stats", {}).get("total_pages", 0),
                "total_images": image_analysis.get("overall_stats", {}).get("total_images", 0),
                "total_vectors": vector_analysis.get("overall_stats", {}).get("total_vectors", 0),
                "total_usage": color_analysis.get("total_usage", 0) + font_analysis.get("total_usage", 0),
                "primary_color_space": intelligent_color_analysis.get("primary_color_space", "Unknown"),
                "total_design_colors": design_color_analysis.get("total_design_colors", 0),
                "color_management_strategy": color_profile_analysis.get("overall_color_management", {}).get("color_management_strategy", "Unknown"),
                "vision_analysis_available": vision_analysis is not None and "error" not in vision_analysis,
                "vision_images_analyzed": vision_analysis.get("total_images", 0) if vision_analysis and "error" not in vision_analysis else 0
            }
        })
        
    except Exception as e:
        logger.error(f"Error processing PDF for complete analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/extract-all-path", methods=["POST"])
@app.route("/extract-all-path", methods=["POST"])
@app.route("/extract-all-path", methods=["POST"])
def extract_all_path():
    """Extract all data from PDF file - returns raw extraction data without scoring"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        filepath = data.get("filepath")
        if not filepath:
            return jsonify({"error": "No filepath provided in JSON body"}), 400
        
        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({"error": f"File not found: {filepath}"}), 404
        
        logger.info(f"Processing PDF for extraction: {filepath}")
        
        # === STANDARD EXTRACTIONS ===
        # Extract colors (design-only, not from images)
        try:
            from color_analyzer import extract_design_colors_only
            color_analysis = extract_design_colors_only(filepath)
        except Exception as e:
            logger.warning(f"Design colors extraction failed, falling back to comprehensive: {e}")
            color_analysis = extract_colors_from_pdf_comprehensive(filepath)
        
        # Extract fonts
        font_analysis = extract_fonts_from_pdf_comprehensive(filepath)
        
        # Extract layout
        layout_analysis = extract_layout_from_pdf_comprehensive(filepath)
        
        # Extract images
        image_analysis = extract_images_from_pdf_comprehensive(filepath)
        
        # Extract vectors
        vector_analysis = extract_vector_graphics_from_pdf_comprehensive(filepath)
        
        # Get font insights (not scores, just patterns)
        font_insights = analyze_font_usage_patterns(font_analysis)
        
        # === GPT VISION ANALYSIS ===
        vision_analysis = None
        try:
            # Check if OpenAI API key is available
            openai_api_key = os.getenv('OPENAI_API_KEY')
            logger.info(f"OpenAI API key available: {bool(openai_api_key)}")
            if openai_api_key:
                logger.info("Starting GPT Vision analysis...")
                vision_analysis = extract_and_analyze_images_from_pdf(filepath, openai_api_key)
                logger.info(f"GPT Vision analysis completed: {vision_analysis}")
            else:
                logger.warning("OpenAI API key not available, skipping vision analysis")
                vision_analysis = {"error": "OpenAI API key not configured"}
        except Exception as e:
            logger.error(f"Vision analysis error: {e}")
            vision_analysis = {"error": str(e)}
        
        # === INTELLIGENT COLOR EXTRACTIONS ===
        try:
            from color_analyzer import extract_design_colors_only, extract_color_profiles, extract_colors_with_proper_color_space
            
            # Extract intelligent colors (CMYK/RGB/Pantone/RAL)
            intelligent_color_analysis = extract_colors_with_proper_color_space(filepath)
            
            # Extract design colors (without product images)
            design_color_analysis = extract_design_colors_only(filepath)
            
            # Extract color profiles
            color_profile_analysis = extract_color_profiles(filepath)
        except ImportError:
            logger.warning("Color analyzer not available, using basic extraction")
            intelligent_color_analysis = {"error": "Color analyzer not available"}
            design_color_analysis = {"error": "Color analyzer not available"}
            color_profile_analysis = {"error": "Color analyzer not available"}
        
        # Check for errors in extractions
        if "error" in color_analysis:
            return jsonify({"error": "Color extraction error: " + str(color_analysis.get("error", ""))}), 500
        
        if "error" in font_analysis:
            return jsonify({"error": "Font extraction error: " + str(font_analysis.get("error", ""))}), 500
        
        if "error" in layout_analysis:
            return jsonify({"error": "Layout extraction error: " + str(layout_analysis.get("error", ""))}), 500
        
        if "error" in image_analysis:
            return jsonify({"error": "Image extraction error: " + str(image_analysis.get("error", ""))}), 500
        
        if "error" in vector_analysis:
            return jsonify({"error": "Vector extraction error: " + str(vector_analysis.get("error", ""))}), 500
        
        # Create extraction result (NO SCORING, just raw data)
        extraction_result = {
            "success": True,
            "filepath": filepath,
            "file_id": data.get("file_id", "unknown"),
            "original_filename": data.get("original_filename", os.path.basename(filepath)),
            "extraction_data": {
                # Raw extraction data (no scoring)
                "color_analysis": color_analysis,
                "font_analysis": font_analysis,
                "layout_analysis": layout_analysis,
                "image_analysis": image_analysis,
                "vector_analysis": vector_analysis,
                "font_insights": font_insights,
                
                # Intelligent color extractions
                "intelligent_color_analysis": intelligent_color_analysis,
                "design_color_analysis": design_color_analysis,
                "color_profile_analysis": color_profile_analysis,
                
                # GPT Vision analysis
                "vision_analysis": vision_analysis
            },
            "summary": {
                "total_colors": design_color_analysis.get("total_design_colors", 0) if "error" not in design_color_analysis else 0,
                "total_fonts": font_analysis.get("total_fonts", 0),
                "total_pages": layout_analysis.get("overall_stats", {}).get("total_pages", 0),
                "total_images": image_analysis.get("overall_stats", {}).get("total_images", 0),
                "total_vectors": vector_analysis.get("overall_stats", {}).get("total_vectors", 0),
                "total_usage": color_analysis.get("total_usage", 0) + font_analysis.get("total_usage", 0),
                "primary_color_space": intelligent_color_analysis.get("primary_color_space", "Unknown") if "error" not in intelligent_color_analysis else "Unknown",
                "total_design_colors": design_color_analysis.get("total_design_colors", 0) if "error" not in design_color_analysis else 0,
                "color_management_strategy": color_profile_analysis.get("overall_color_management", {}).get("color_management_strategy", "Unknown") if "error" not in color_profile_analysis else "Unknown",
                "vision_analysis_available": vision_analysis is not None and "error" not in vision_analysis,
                "vision_images_analyzed": vision_analysis.get("total_images", 0) if vision_analysis and "error" not in vision_analysis else 0
            },
            "processing_time": "Extraction completed",
            "status": "Extraction completed successfully"
        }
        
        # Store extraction result for status endpoint
        file_id = data.get("file_id", "unknown")
        status_file = f"/app/status/{file_id}.json"
        os.makedirs("/app/status", exist_ok=True)
        
        with open(status_file, "w") as f:
            json.dump({
                "file_id": file_id,
                "start_time": time.time(),
                "progress": 100,
                "status": "completed",
                "message": "Extraction completed successfully",
                "results": extraction_result,
                "last_update": time.time()
            }, f)
        
        return jsonify(extraction_result)
        
    except Exception as e:
        logger.error(f"Error in extract_all_path: {e}")
        return jsonify({"error": str(e)}), 500
@app.route('/extract-design-colors-with-bosch-path', methods=['POST'])
def extract_design_colors_with_bosch_by_path():
    """Extract design colors and compare with Bosch colors from database using file path"""
    
    try:
        data = request.get_json()
        if not data or 'filepath' not in data:
            return jsonify({"error": "No filepath provided in JSON body"}), 400
        
        filepath = data['filepath']
        
        # Validate filepath
        if not os.path.exists(filepath):
            return jsonify({"error": f"File not found: {filepath}"}), 404
        
        if not filepath.lower().endswith('.pdf'):
            return jsonify({"error": "File must be a PDF"}), 400
        
        filename = os.path.basename(filepath)
        logger.info(f"Processing PDF for design colors with Bosch comparison: {filename}")
        
        # Import the new function
        from color_analyzer import extract_design_colors_with_bosch_comparison
        
        # Extract design colors with Bosch comparison
        start_time = time.time()
        color_analysis = extract_design_colors_with_bosch_comparison(filepath)
        processing_time = time.time() - start_time
        
        # Save to database if available
        if DATABASE_AVAILABLE:
            try:
                save_analysis_to_database(
                    filepath=filepath,
                    filename=filename,
                    analysis_type="design_colors_with_bosch",
                    analysis_data=color_analysis,
                    processing_time=processing_time
                )
                logger.info(f"Saved design colors with Bosch analysis to database for {filename}")
            except Exception as e:
                logger.error(f"Failed to save to database: {e}")
        
        return jsonify({
            "success": True,
            "filename": filename,
            "filepath": filepath,
            "processing_time": processing_time,
            "analysis_type": "design_colors_with_bosch_comparison",
            "color_analysis": color_analysis
        })
        
    except Exception as e:
        logger.error(f"Error in extract_design_colors_with_bosch_by_path: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "analysis_type": "design_colors_with_bosch_comparison"
        }), 500

@app.route('/info', methods=['GET'])
def get_info():
    """Get information about the service"""
    return jsonify({
        "service": "Brandchecker Analysis",
        "version": "3.0",
        "database_available": DATABASE_AVAILABLE,
        "endpoints": {
            "health": "/health",
            "extract_colors": "/extract-colors",
            "extract_colors_path": "/extract-colors-path",
            "extract_design_colors": "/extract-design-colors",
            "extract_design_colors_path": "/extract-design-colors-path",
            "extract_all": "/extract-all",
            "extract_all_path": "/extract-all-path",
            "extract_fonts": "/extract-fonts",
            "extract_layout": "/extract-layout",
            "extract_images": "/extract-images",
            "analyze_images_vision": "/analyze-images-vision",
            "extract_vectors": "/extract-vectors",
            "database_stats": "/database/stats",
            "database_recent": "/database/recent",
            "database_search": "/database/search"
        }
    })

# Database endpoints
@app.route('/database/stats', methods=['GET'])
def get_database_stats():
    """Get database statistics"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available"}), 503
    
    try:
        stats = db_manager.get_database_stats()
        return jsonify({
            "success": True,
            "database_stats": stats
        })
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/database/recent', methods=['GET'])
def get_recent_analyses():
    """Get recent analyses from database"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available"}), 503
    
    try:
        limit = request.args.get('limit', 10, type=int)
        if limit > 100:
            limit = 100
        
        recent = db_manager.get_recent_analyses(limit)
        return jsonify({
            "success": True,
            "recent_analyses": recent,
            "total": len(recent)
        })
    except Exception as e:
        logger.error(f"Error getting recent analyses: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/database/search', methods=['GET'])
def search_colors():
    """Search for colors in database"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available"}), 503
    
    try:
        hex_code = request.args.get('hex_code')
        color_space = request.args.get('color_space')
        limit = request.args.get('limit', 50, type=int)
        
        if limit > 200:
            limit = 200
        
        colors = db_manager.search_colors(hex_code, color_space, limit)
        return jsonify({
            "success": True,
            "colors": colors,
            "total": len(colors)
        })
    except Exception as e:
        logger.error(f"Error searching colors: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/database/document/<pdf_id>', methods=['GET'])
def get_document(pdf_id):
    """Get a specific document by ID"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available"}), 503
    
    try:
        document = db_manager.get_pdf_document(pdf_id)
        if not document:
            return jsonify({"error": "Document not found"}), 404
        
        return jsonify({
            "success": True,
            "document": document
        })
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        return jsonify({"error": str(e)}), 500

# Helper function to save analysis to database
def save_analysis_to_database(filepath: str, filename: str, analysis_type: str, analysis_data: dict, processing_time: float = None):
    """Save analysis results to database"""
    if not DATABASE_AVAILABLE:
        logger.warning("Database not available, skipping save")
        return None
    
    try:
        # Get file size
        file_size = os.path.getsize(filepath) if os.path.exists(filepath) else None
        
        # Insert or update PDF document
        pdf_id = db_manager.insert_pdf_document(filename, filepath, file_size)
        if not pdf_id:
            logger.error("Failed to insert PDF document")
            return None
        
        # Update analysis status
        db_manager.update_analysis_status(pdf_id, 'processing')
        
        # Save analysis data based on type
        if analysis_type == 'colors':
            color_analysis_id = db_manager.insert_color_analysis(pdf_id, 'all_colors', analysis_data)
            if color_analysis_id and 'colors' in analysis_data:
                db_manager.insert_colors(color_analysis_id, analysis_data['colors'])
        
        elif analysis_type == 'design_colors':
            color_analysis_id = db_manager.insert_color_analysis(pdf_id, 'design_colors', analysis_data)
            if color_analysis_id and 'design_colors' in analysis_data:
                db_manager.insert_colors(color_analysis_id, analysis_data['design_colors'])
        
        elif analysis_type == 'complete':
            # Save complete analysis
            summary = analysis_data.get('summary', {})
            db_manager.insert_complete_analysis(pdf_id, summary, analysis_data, processing_time)
            
            # Save individual analysis components
            if 'color_analysis' in analysis_data:
                color_analysis_id = db_manager.insert_color_analysis(pdf_id, 'all_colors', analysis_data['color_analysis'])
                if color_analysis_id and 'colors' in analysis_data['color_analysis']:
                    db_manager.insert_colors(color_analysis_id, analysis_data['color_analysis']['colors'])
            
            # Save design colors if available
            if 'design_color_analysis' in analysis_data:
                design_color_analysis_id = db_manager.insert_color_analysis(pdf_id, 'design_colors', analysis_data['design_color_analysis'])
                if design_color_analysis_id and 'design_colors' in analysis_data['design_color_analysis']:
                    db_manager.insert_colors(design_color_analysis_id, analysis_data['design_color_analysis']['design_colors'])
            
            # Create knowledge chunks if knowledge database is available
            if KNOWLEDGE_DB_AVAILABLE:
                try:
                    chunks = knowledge_db_manager.extract_knowledge_from_analysis(pdf_id, analysis_data)
                    if chunks:
                        saved_chunk_ids = knowledge_db_manager.save_knowledge_chunks(chunks)
                        logger.info(f"Created {len(saved_chunk_ids)} knowledge chunks for {filename}")
                except Exception as e:
                    logger.error(f"Error creating knowledge chunks: {e}")
        
        # Update analysis status to completed
        db_manager.update_analysis_status(pdf_id, 'completed', completed=True)
        
        logger.info(f"Analysis saved to database for {filename}")
        return pdf_id
        
    except Exception as e:
        logger.error(f"Error saving analysis to database: {e}")
        # Try to update status to failed
        try:
            if pdf_id:
                db_manager.update_analysis_status(pdf_id, 'failed')
        except:
            pass
        return None

# Knowledge Database endpoints
@app.route('/knowledge/stats', methods=['GET'])
def get_knowledge_stats():
    """Get knowledge database statistics"""
    if not KNOWLEDGE_DB_AVAILABLE:
        return jsonify({"error": "Knowledge database not available"}), 503
    
    try:
        stats = knowledge_db_manager.get_knowledge_stats()
        return jsonify({
            "success": True,
            "knowledge_stats": stats
        })
    except Exception as e:
        logger.error(f"Error getting knowledge stats: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/knowledge/search', methods=['POST'])
def search_knowledge():
    """Search knowledge base using vector similarity"""
    if not KNOWLEDGE_DB_AVAILABLE:
        return jsonify({"error": "Knowledge database not available"}), 503
    
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "No query provided"}), 400
        
        query_text = data['query']
        limit = data.get('limit', 5)
        similarity_threshold = data.get('similarity_threshold', 0.7)
        
        if limit > 20:
            limit = 20
        
        results = knowledge_db_manager.search_knowledge(query_text, limit, similarity_threshold)
        
        return jsonify({
            "success": True,
            "query": query_text,
            "results": results,
            "total": len(results)
        })
        
    except Exception as e:
        logger.error(f"Error searching knowledge: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/knowledge/query', methods=['POST'])
def query_knowledge_with_gpt():
    """Query knowledge base and generate GPT response"""
    if not KNOWLEDGE_DB_AVAILABLE:
        return jsonify({"error": "Knowledge database not available"}), 503
    
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "No query provided"}), 400
        
        query_text = data['query']
        limit = data.get('limit', 5)
        
        if limit > 10:
            limit = 10
        
        result = knowledge_db_manager.query_knowledge_with_gpt(query_text, limit)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error querying knowledge with GPT: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/knowledge/chunks', methods=['GET'])
def get_knowledge_chunks():
    """Get knowledge chunks with optional filtering"""
    if not KNOWLEDGE_DB_AVAILABLE:
        return jsonify({"error": "Knowledge database not available"}), 503
    
    try:
        chunk_type = request.args.get('chunk_type')
        pdf_id = request.args.get('pdf_id')
        limit = request.args.get('limit', 50, type=int)
        
        if limit > 100:
            limit = 100
        
        query = """
        SELECT 
            kc.id,
            kc.chunk_type,
            kc.chunk_index,
            kc.content,
            kc.metadata,
            kc.embedding_created_at,
            kc.created_at,
            pd.filename,
            pd.filepath
        FROM knowledge_chunks kc
        JOIN pdf_documents pd ON kc.pdf_document_id = pd.id
        WHERE 1=1
        """
        
        params = []
        
        if chunk_type:
            query += " AND kc.chunk_type = %s"
            params.append(chunk_type)
        
        if pdf_id:
            query += " AND kc.pdf_document_id = %s"
            params.append(pdf_id)
        
        query += " ORDER BY kc.created_at DESC LIMIT %s"
        params.append(limit)
        
        result = db_manager.execute_query(query, tuple(params))
        
        if result:
            chunks = [dict(row) for row in result]
        else:
            chunks = []
        
        return jsonify({
            "success": True,
            "chunks": chunks,
            "total": len(chunks)
        })
        
    except Exception as e:
        logger.error(f"Error getting knowledge chunks: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/knowledge/embed', methods=['POST'])
def embed_analysis_to_knowledge():
    """Embed analysis data into knowledge base"""
    if not KNOWLEDGE_DB_AVAILABLE:
        return jsonify({"error": "Knowledge database not available"}), 503
    
    try:
        data = request.get_json()
        if not data or 'pdf_id' not in data or 'analysis_data' not in data:
            return jsonify({"error": "pdf_id and analysis_data required"}), 400
        
        pdf_id = data['pdf_id']
        analysis_data = data['analysis_data']
        
        # Extract knowledge chunks from analysis
        chunks = knowledge_db_manager.extract_knowledge_from_analysis(pdf_id, analysis_data)
        
        if not chunks:
            return jsonify({
                "success": True,
                "message": "No knowledge chunks extracted",
                "chunks_saved": 0
            })
        
        # Save chunks with embeddings
        saved_chunk_ids = knowledge_db_manager.save_knowledge_chunks(chunks)
        
        return jsonify({
            "success": True,
            "chunks_extracted": len(chunks),
            "chunks_saved": len(saved_chunk_ids),
            "chunk_ids": saved_chunk_ids
        })
        
    except Exception as e:
        logger.error(f"Error embedding analysis to knowledge: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/knowledge/embed-bosch-colors', methods=['POST'])
def embed_bosch_colors():
    """Embed Bosch colors JSON data into knowledge base"""
    if not KNOWLEDGE_DB_AVAILABLE:
        return jsonify({"error": "Knowledge database not available"}), 503
    
    try:
        data = request.get_json()
        if not data or 'bosch_colors' not in data:
            return jsonify({"error": "bosch_colors data required"}), 400
        
        bosch_colors_data = data['bosch_colors']
        
        # Validate that it's a dictionary
        if not isinstance(bosch_colors_data, dict):
            return jsonify({"error": "bosch_colors must be a JSON object"}), 400
        
        # Embed Bosch colors into knowledge base
        saved_chunk_ids = knowledge_db_manager.embed_bosch_colors(bosch_colors_data)
        
        return jsonify({
            "success": True,
            "message": f"Successfully embedded {len(saved_chunk_ids)} Bosch color chunks",
            "chunks_saved": len(saved_chunk_ids),
            "chunk_ids": saved_chunk_ids
        })
        
    except Exception as e:
        logger.error(f"Error embedding Bosch colors: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/knowledge/bosch-colors', methods=['GET'])
def get_bosch_colors():
    """Get Bosch colors from knowledge base"""
    if not KNOWLEDGE_DB_AVAILABLE:
        return jsonify({"error": "Knowledge database not available"}), 503
    
    try:
        # Get query parameters
        hex_code = request.args.get('hex_code')
        limit = int(request.args.get('limit', 50))
        
        if hex_code:
            # Get specific Bosch color by hex code
            color = knowledge_db_manager.get_bosch_color_by_hex(hex_code)
            if color:
                return jsonify({
                    "success": True,
                    "color": color
                })
            else:
                return jsonify({
                    "success": False,
                    "message": f"No Bosch color found with hex code {hex_code}"
                }), 404
        else:
            # Get all Bosch colors
            colors = knowledge_db_manager.search_bosch_colors("", limit=limit)
            return jsonify({
                "success": True,
                "colors": colors,
                "total": len(colors)
            })
        
    except Exception as e:
        logger.error(f"Error getting Bosch colors: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/knowledge/sql', methods=['POST'])
def execute_sql_query():
    """Execute custom SQL query on knowledge database"""
    if not KNOWLEDGE_DB_AVAILABLE:
        return jsonify({"error": "Knowledge database not available"}), 503
    
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "No SQL query provided"}), 400
        
        sql_query = data['query']
        params = data.get('params', [])
        
        # Validate query (basic security check)
        sql_lower = sql_query.lower().strip()
        if not sql_lower.startswith('select'):
            return jsonify({"error": "Only SELECT queries are allowed"}), 400
        
        # Check for potentially dangerous keywords
        dangerous_keywords = ['drop', 'delete', 'insert', 'update', 'create', 'alter', 'truncate']
        if any(keyword in sql_lower for keyword in dangerous_keywords):
            return jsonify({"error": "Query contains forbidden keywords"}), 400
        
        # Execute query
        if params:
            results = db_manager.execute_query(sql_query, params)
        else:
            results = db_manager.execute_query(sql_query)
        
        if results:
            # Convert results to list of dicts
            columns = list(results[0].keys()) if results else []
            rows = []
            for row in results:
                row_dict = {}
                for col in columns:
                    value = row[col]
                    # Handle datetime objects
                    if hasattr(value, 'isoformat'):
                        row_dict[col] = value.isoformat()
                    else:
                        row_dict[col] = value
                rows.append(row_dict)
            
            return jsonify({
                "success": True,
                "query": sql_query,
                "columns": columns,
                "results": rows,
                "total_rows": len(rows)
            })
        else:
            return jsonify({
                "success": True,
                "query": sql_query,
                "columns": [],
                "results": [],
                "total_rows": 0
            })
        
    except Exception as e:
        logger.error(f"Error executing SQL query: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/analysis-status/<file_id>", methods=["GET"])
def get_analysis_status(file_id):
    """Get analysis status for a file"""
    status_dir = "/app/status"
    os.makedirs(status_dir, exist_ok=True)
    status_file = os.path.join(status_dir, f"{file_id}.json")
    
    current_time = time.time()
    
    if not os.path.exists(status_file):
        # Initial status for a new file
        initial_status = {
            "file_id": file_id,
            "start_time": current_time,
            "progress": 0,
            "status": "processing",
            "message": "Initializing analysis...",
            "results": None,
            "last_update": current_time
        }
        with open(status_file, "w") as f:
            json.dump(initial_status, f)
        return jsonify(initial_status)
    
    with open(status_file, "r") as f:
        data = json.load(f)
        
    if data["status"] == "completed" or data["status"] == "error":
        return jsonify(data) # Return final status

    # Simulate progress over 30 seconds
    elapsed_time = current_time - data["start_time"]
    total_duration = 30 # seconds
    
    new_progress = min(int((elapsed_time / total_duration) * 100), 100)
    
    message = data["message"]
    status = "processing"
    results = None

    if new_progress < 20:
        message = "Extracting text and images..."
    elif new_progress < 50:
        message = "Analyzing brand elements..."
    elif new_progress < 80:
        message = "Generating report..."
    elif new_progress < 100:
        message = "Finalizing analysis..."
    else:
        new_progress = 100
        status = "completed"
        message = "Analysis completed successfully"
        
        # Load results from the extraction if available
        results = data.get("results", None)

    data.update({
        "progress": new_progress,
        "status": status,
        "message": message,
        "results": results,
        "last_update": current_time
    })
    
    with open(status_file, "w") as f:
        json.dump(data, f)
        
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 