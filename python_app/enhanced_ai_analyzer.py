import os
import json
import logging
import tempfile
import base64
import requests
from PIL import Image
import fitz  # PyMuPDF
import io
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedAIAnalyzer:
    """Comprehensive AI-powered PDF analyzer for graphics, fonts, and layout"""
    
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.openai_base_url = "https://api.openai.com/v1"
    
    def analyze_pdf_comprehensive(self, pdf_path):
        """Complete PDF analysis with graphics, fonts, and layout"""
        
        try:
            logger.info("Starting comprehensive AI PDF analysis...")
            
            # Step 1: Graphics Analysis (existing functionality)
            graphics_analysis = self._analyze_graphics(pdf_path)
            
            # Step 2: Font Analysis with AI
            font_analysis = self._analyze_fonts_with_ai(pdf_path)
            
            # Step 3: Layout Analysis with AI
            layout_analysis = self._analyze_layout_with_ai(pdf_path)
            
            # Step 4: Combine all analyses
            comprehensive_analysis = {
                "graphics_analysis": graphics_analysis,
                "font_analysis": font_analysis,
                "layout_analysis": layout_analysis,
                "summary": self._generate_comprehensive_summary(graphics_analysis, font_analysis, layout_analysis)
            }
            
            return comprehensive_analysis
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            return {"error": str(e)}
    
    def _analyze_graphics(self, pdf_path):
        """Analyze graphics using existing GlobalGraphicDetector"""
        try:
            from global_graphic_detector import GlobalGraphicDetector
            detector = GlobalGraphicDetector(self.openai_api_key)
            return detector.detect_all_graphics(pdf_path)
        except Exception as e:
            logger.error(f"Error in graphics analysis: {e}")
            return {"error": str(e)}
    
    def _analyze_fonts_with_ai(self, pdf_path):
        """Analyze fonts using AI vision and text extraction"""
        
        try:
            logger.info("Starting AI-powered font analysis...")
            
            # Extract text and font information using PyMuPDF
            doc = fitz.open(pdf_path)
            font_data = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Convert page to image for AI analysis
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                
                # Get text with font information
                text_dict = page.get_text("dict")
                page_fonts = []
                
                for block in text_dict.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line.get("spans", []):
                                if "font" in span and "size" in span:
                                    font_info = {
                                        "name": span["font"],
                                        "size": span["size"],
                                        "text": span.get("text", ""),
                                        "bbox": span.get("bbox", []),
                                        "page": page_num + 1,
                                        "color": span.get("color", 0),
                                        "flags": span.get("flags", 0)
                                    }
                                    page_fonts.append(font_info)
                
                # Analyze fonts with AI
                if page_fonts:
                    ai_font_analysis = self._analyze_fonts_ai(img_data, page_fonts, page_num + 1)
                    font_data.append({
                        "page": page_num + 1,
                        "fonts": page_fonts,
                        "ai_analysis": ai_font_analysis
                    })
            
            doc.close()
            
            # Aggregate font analysis
            return self._aggregate_font_analysis(font_data)
            
        except Exception as e:
            logger.error(f"Error in font analysis: {e}")
            return {"error": str(e)}
    
    def _analyze_fonts_ai(self, img_data, fonts, page_num):
        """Analyze fonts using AI vision"""
        
        try:
            # Encode image for OpenAI
            image_base64 = base64.b64encode(img_data).decode('utf-8')
            
            # Prepare prompt for font analysis
            font_prompt = f"""Analyze the fonts and typography in this image. Focus on:

1. Font families and styles used
2. Typography hierarchy (headings, body text, etc.)
3. Font sizes and their purposes
4. Color usage in text
5. Overall typography quality and consistency

Provide a detailed analysis in JSON format with these fields:
- font_families: (list of font families found)
- typography_hierarchy: (description of text hierarchy)
- font_sizes: (list of font sizes and their purposes)
- text_colors: (list of colors used in text)
- typography_quality: (high/medium/low assessment)
- consistency_score: (0-1 score for typography consistency)
- recommendations: (list of typography recommendations)"""
            
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": font_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 800
            }
            
            response = requests.post(
                f"{self.openai_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Try to parse JSON response
                try:
                    # Extract JSON from markdown code blocks if present
                    if "```json" in content:
                        json_start = content.find("```json") + 7
                        json_end = content.find("```", json_start)
                        json_content = content[json_start:json_end].strip()
                        ai_analysis = json.loads(json_content)
                    else:
                        ai_analysis = json.loads(content)
                    
                    return {
                        "success": True,
                        "ai_analysis": ai_analysis,
                        "raw_response": content
                    }
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": "Failed to parse AI response as JSON",
                        "raw_response": content
                    }
            else:
                return {
                    "success": False,
                    "error": f"OpenAI API error: {response.status_code}",
                    "raw_response": response.text
                }
                
        except Exception as e:
            logger.error(f"Error in AI font analysis: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _analyze_layout_with_ai(self, pdf_path):
        """Analyze layout using AI vision"""
        
        try:
            logger.info("Starting AI-powered layout analysis...")
            
            doc = fitz.open(pdf_path)
            layout_data = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Convert page to image for AI analysis
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                
                # Analyze layout with AI
                ai_layout_analysis = self._analyze_layout_ai(img_data, page_num + 1)
                
                layout_data.append({
                    "page": page_num + 1,
                    "ai_analysis": ai_layout_analysis
                })
            
            doc.close()
            
            return self._aggregate_layout_analysis(layout_data)
            
        except Exception as e:
            logger.error(f"Error in layout analysis: {e}")
            return {"error": str(e)}
    
    def _analyze_layout_ai(self, img_data, page_num):
        """Analyze layout using AI vision"""
        
        try:
            # Encode image for OpenAI
            image_base64 = base64.b64encode(img_data).decode('utf-8')
            
            # Prepare prompt for layout analysis
            layout_prompt = f"""Analyze the layout and design structure of this page. Focus on:

1. Overall layout type (grid, asymmetric, centered, etc.)
2. Content organization and hierarchy
3. Spacing and margins
4. Visual balance and composition
5. Design principles used

Provide a detailed analysis in JSON format with these fields:
- layout_type: (grid/asymmetric/centered/other)
- content_hierarchy: (description of content organization)
- spacing_analysis: (description of spacing and margins)
- visual_balance: (high/medium/low assessment)
- design_quality: (high/medium/low assessment)
- composition_score: (0-1 score for overall composition)
- recommendations: (list of layout improvements)"""
            
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": layout_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 800
            }
            
            response = requests.post(
                f"{self.openai_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Try to parse JSON response
                try:
                    # Extract JSON from markdown code blocks if present
                    if "```json" in content:
                        json_start = content.find("```json") + 7
                        json_end = content.find("```", json_start)
                        json_content = content[json_start:json_end].strip()
                        ai_analysis = json.loads(json_content)
                    else:
                        ai_analysis = json.loads(content)
                    
                    return {
                        "success": True,
                        "ai_analysis": ai_analysis,
                        "raw_response": content
                    }
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": "Failed to parse AI response as JSON",
                        "raw_response": content
                    }
            else:
                return {
                    "success": False,
                    "error": f"OpenAI API error: {response.status_code}",
                    "raw_response": response.text
                }
                
        except Exception as e:
            logger.error(f"Error in AI layout analysis: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _aggregate_font_analysis(self, font_data):
        """Aggregate font analysis results"""
        
        try:
            all_fonts = []
            font_families = Counter()
            font_sizes = Counter()
            ai_analyses = []
            
            for page_data in font_data:
                all_fonts.extend(page_data["fonts"])
                if page_data["ai_analysis"]["success"]:
                    ai_analyses.append(page_data["ai_analysis"])
                
                # Count font families and sizes
                for font in page_data["fonts"]:
                    font_families[font["name"]] += 1
                    font_sizes[font["size"]] += 1
            
            # Aggregate AI analyses
            aggregated_ai = {}
            if ai_analyses:
                # Combine AI insights
                all_font_families = []
                all_hierarchies = []
                all_qualities = []
                
                for analysis in ai_analyses:
                    ai_data = analysis["ai_analysis"]
                    if "font_families" in ai_data:
                        all_font_families.extend(ai_data["font_families"])
                    if "typography_hierarchy" in ai_data:
                        all_hierarchies.append(ai_data["typography_hierarchy"])
                    if "typography_quality" in ai_data:
                        all_qualities.append(ai_data["typography_quality"])
                
                aggregated_ai = {
                    "font_families": list(set(all_font_families)),
                    "typography_hierarchy": all_hierarchies,
                    "typography_quality": max(all_qualities) if all_qualities else "unknown"
                }
            
            return {
                "total_fonts": len(all_fonts),
                "font_families": dict(font_families),
                "font_sizes": dict(font_sizes),
                "ai_analysis": aggregated_ai,
                "page_analyses": font_data
            }
            
        except Exception as e:
            logger.error(f"Error aggregating font analysis: {e}")
            return {"error": str(e)}
    
    def _aggregate_layout_analysis(self, layout_data):
        """Aggregate layout analysis results"""
        
        try:
            ai_analyses = []
            
            for page_data in layout_data:
                if page_data["ai_analysis"]["success"]:
                    ai_analyses.append(page_data["ai_analysis"])
            
            # Aggregate AI analyses
            aggregated_ai = {}
            if ai_analyses:
                # Combine AI insights
                layout_types = []
                design_qualities = []
                composition_scores = []
                
                for analysis in ai_analyses:
                    ai_data = analysis["ai_analysis"]
                    if "layout_type" in ai_data:
                        layout_types.append(ai_data["layout_type"])
                    if "design_quality" in ai_data:
                        design_qualities.append(ai_data["design_quality"])
                    if "composition_score" in ai_data:
                        composition_scores.append(ai_data["composition_score"])
                
                aggregated_ai = {
                    "layout_types": list(set(layout_types)),
                    "design_quality": max(design_qualities) if design_qualities else "unknown",
                    "avg_composition_score": sum(composition_scores) / len(composition_scores) if composition_scores else 0
                }
            
            return {
                "total_pages": len(layout_data),
                "ai_analysis": aggregated_ai,
                "page_analyses": layout_data
            }
            
        except Exception as e:
            logger.error(f"Error aggregating layout analysis: {e}")
            return {"error": str(e)}
    
    def _generate_comprehensive_summary(self, graphics_analysis, font_analysis, layout_analysis):
        """Generate comprehensive summary of all analyses"""
        
        try:
            summary = {
                "total_pages": 0,
                "graphics_summary": {},
                "fonts_summary": {},
                "layout_summary": {},
                "overall_assessment": {}
            }
            
            # Graphics summary
            if "graphic_regions" in graphics_analysis:
                summary["graphics_summary"] = {
                    "total_graphics": len(graphics_analysis["graphic_regions"]),
                    "brands_found": graphics_analysis.get("analysis_summary", {}).get("ai_analysis_summary", {}).get("brands_companies", []),
                    "graphic_types": graphics_analysis.get("analysis_summary", {}).get("ai_analysis_summary", {}).get("graphic_types", {})
                }
            
            # Fonts summary
            if "total_fonts" in font_analysis:
                summary["fonts_summary"] = {
                    "total_fonts": font_analysis["total_fonts"],
                    "font_families": len(font_analysis.get("font_families", {})),
                    "typography_quality": font_analysis.get("ai_analysis", {}).get("typography_quality", "unknown")
                }
            
            # Layout summary
            if "total_pages" in layout_analysis:
                summary["layout_summary"] = {
                    "total_pages": layout_analysis["total_pages"],
                    "layout_types": layout_analysis.get("ai_analysis", {}).get("layout_types", []),
                    "design_quality": layout_analysis.get("ai_analysis", {}).get("design_quality", "unknown")
                }
                summary["total_pages"] = layout_analysis["total_pages"]
            
            # Overall assessment
            summary["overall_assessment"] = {
                "comprehensive_analysis": True,
                "ai_powered": True,
                "analysis_quality": "high"
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating comprehensive summary: {e}")
            return {"error": str(e)} 