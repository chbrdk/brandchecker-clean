import os
import json
import logging
import numpy as np
from collections import defaultdict
import fitz  # PyMuPDF
from PIL import Image, ImageDraw
import cv2
import io
import tempfile
import base64
import requests
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GlobalGraphicDetector:
    """Global graphic/illustration detection with OpenAI AI analysis"""
    
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.openai_base_url = "https://api.openai.com/v1"
        self.graphic_regions = []
        self.screenshot_paths = []
        
    def detect_all_graphics(self, pdf_path):
        """Main method to detect all graphics/illustrations and analyze with AI"""
        
        try:
            logger.info("Starting global graphic detection with AI analysis...")
            
            detection_results = {
                "graphic_regions": [],
                "screenshots": [],
                "ai_analysis": [],
                "analysis_summary": {},
                "recommended_graphics": []
            }
            
            # Step 1: Find all potential graphic regions
            all_regions = self.find_all_graphic_regions(pdf_path)
            
            # Step 2: Cluster similar regions to eliminate duplicates
            clustered_regions = self.cluster_similar_regions(all_regions)
            
            # Step 3: Rank regions by graphic probability
            ranked_regions = self.rank_regions_by_graphic_probability(clustered_regions)
            
            # Step 4: Generate screenshots for all regions
            screenshots = self.generate_region_screenshots(pdf_path, ranked_regions)
            
            # Step 5: Analyze each screenshot with OpenAI AI
            ai_analysis = self.analyze_screenshots_with_ai(screenshots)
            
            # Step 6: Combine results and recommend graphics
            recommended = self.recommend_graphics(ranked_regions, ai_analysis)
            
            detection_results["graphic_regions"] = ranked_regions
            detection_results["screenshots"] = screenshots
            detection_results["ai_analysis"] = ai_analysis
            detection_results["recommended_graphics"] = recommended
            detection_results["analysis_summary"] = self.analyze_graphic_regions(ranked_regions, ai_analysis)
            
            return detection_results
            
        except Exception as e:
            logger.error(f"Error in global graphic detection: {e}")
            return {"error": str(e)}
    
    def find_all_graphic_regions(self, pdf_path):
        """Find all potential graphic regions using comprehensive methods"""
        
        try:
            all_regions = []
            doc = fitz.open(pdf_path)
            
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
                
                # Method 1: Color-based regions (logos, graphics)
                color_regions = self.find_color_based_regions(cv_image, page_num)
                all_regions.extend(color_regions)
                
                # Method 2: Edge-based regions (illustrations, diagrams)
                edge_regions = self.find_edge_based_regions(cv_image, page_num)
                all_regions.extend(edge_regions)
                
                # Method 3: Contour-based regions (shapes, graphics)
                contour_regions = self.find_contour_based_regions(cv_image, page_num)
                all_regions.extend(contour_regions)
                
                # Method 4: Texture-based regions (patterns, backgrounds)
                texture_regions = self.find_texture_based_regions(cv_image, page_num)
                all_regions.extend(texture_regions)
                
                # Method 5: Position-based regions (typical graphic positions)
                position_regions = self.find_position_based_regions(cv_image, page_num)
                all_regions.extend(position_regions)
                
                # Method 6: Brightness-based regions (high contrast areas)
                brightness_regions = self.find_brightness_based_regions(cv_image, page_num)
                all_regions.extend(brightness_regions)
            
            doc.close()
            return all_regions
            
        except Exception as e:
            logger.error(f"Error finding graphic regions: {e}")
            return []
    
    def find_color_based_regions(self, cv_image, page_num):
        """Find regions based on color analysis"""
        
        try:
            regions = []
            
            # Convert to HSV for better color analysis
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            
            # Define color ranges for graphics
            color_ranges = {
                "blue": ([100, 50, 50], [130, 255, 255]),
                "red": ([0, 50, 50], [10, 255, 255]),
                "red2": ([170, 50, 50], [180, 255, 255]),
                "green": ([40, 50, 50], [80, 255, 255]),
                "yellow": ([20, 50, 50], [40, 255, 255]),
                "orange": ([10, 50, 50], [20, 255, 255]),
                "purple": ([130, 50, 50], [170, 255, 255]),
                "black": ([0, 0, 0], [180, 255, 30]),
                "white": ([0, 0, 200], [180, 30, 255]),
                "gray": ([0, 0, 50], [180, 50, 200])
            }
            
            for color_name, (lower, upper) in color_ranges.items():
                # Create mask for color
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                
                # Find contours
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if 50 < area < 50000:  # Wider range for graphics
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        region_info = {
                            "bbox": [x, y, x + w, y + h],
                            "area": area,
                            "width": w,
                            "height": h,
                            "center_x": x + w // 2,
                            "center_y": y + h // 2,
                            "page": page_num + 1,
                            "detection_method": "color_based",
                            "color": color_name,
                            "confidence": 0.0
                        }
                        regions.append(region_info)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error finding color-based regions: {e}")
            return []
    
    def find_edge_based_regions(self, cv_image, page_num):
        """Find regions based on edge detection"""
        
        try:
            regions = []
            
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Edge detection with different thresholds
            edges_low = cv2.Canny(gray, 30, 100)
            edges_high = cv2.Canny(gray, 50, 150)
            
            # Combine edge maps
            edges = cv2.bitwise_or(edges_low, edges_high)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 100 < area < 30000:  # Wider range for graphics
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate edge density
                    roi = edges[y:y+h, x:x+w]
                    edge_density = np.sum(roi > 0) / (w * h)
                    
                    if edge_density > 0.02:  # Lower threshold for graphics
                        region_info = {
                            "bbox": [x, y, x + w, y + h],
                            "area": area,
                            "width": w,
                            "height": h,
                            "center_x": x + w // 2,
                            "center_y": y + h // 2,
                            "page": page_num + 1,
                            "detection_method": "edge_based",
                            "edge_density": edge_density,
                            "confidence": 0.0
                        }
                        regions.append(region_info)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error finding edge-based regions: {e}")
            return []
    
    def find_contour_based_regions(self, cv_image, page_num):
        """Find regions based on contour analysis"""
        
        try:
            regions = []
            
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Multiple threshold levels
            thresholds = [127, 100, 150]
            
            for threshold in thresholds:
                _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
                
                # Find contours
                contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if 200 < area < 40000:  # Wider range for graphics
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        # Calculate aspect ratio
                        aspect_ratio = w / h if h > 0 else 0
                        
                        # Filter by aspect ratio (graphics can be more varied)
                        if 0.1 < aspect_ratio < 10.0:
                            region_info = {
                                "bbox": [x, y, x + w, y + h],
                                "area": area,
                                "width": w,
                                "height": h,
                                "center_x": x + w // 2,
                                "center_y": y + h // 2,
                                "page": page_num + 1,
                                "detection_method": "contour_based",
                                "aspect_ratio": aspect_ratio,
                                "threshold": threshold,
                                "confidence": 0.0
                            }
                            regions.append(region_info)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error finding contour-based regions: {e}")
            return []
    
    def find_texture_based_regions(self, cv_image, page_num):
        """Find regions based on texture analysis"""
        
        try:
            regions = []
            
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Calculate texture features using local binary patterns
            # Simple approach: variance of local regions
            kernel_size = 15
            kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
            
            # Convolve with kernel to get local mean
            local_mean = cv2.filter2D(gray.astype(np.float32), -1, kernel)
            
            # Calculate local variance
            local_variance = cv2.filter2D((gray.astype(np.float32) - local_mean) ** 2, -1, kernel)
            
            # Find regions with high texture
            texture_threshold = np.percentile(local_variance, 90)
            texture_mask = local_variance > texture_threshold
            
            # Find contours in texture mask
            contours, _ = cv2.findContours(texture_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 300 < area < 20000:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    region_info = {
                        "bbox": [x, y, x + w, y + h],
                        "area": area,
                        "width": w,
                        "height": h,
                        "center_x": x + w // 2,
                        "center_y": y + h // 2,
                        "page": page_num + 1,
                        "detection_method": "texture_based",
                        "texture_variance": float(np.mean(local_variance[y:y+h, x:x+w])),
                        "confidence": 0.0
                    }
                    regions.append(region_info)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error finding texture-based regions: {e}")
            return []
    
    def find_position_based_regions(self, cv_image, page_num):
        """Find regions based on typical graphic positions"""
        
        try:
            regions = []
            
            img_height, img_width = cv_image.shape[:2]
            
            # Define typical graphic positions
            graphic_positions = [
                # Top-right corner (logos)
                {
                    "x_range": (int(img_width * 0.7), int(img_width * 0.95)),
                    "y_range": (0, int(img_height * 0.3)),
                    "name": "top_right"
                },
                # Top-left corner (logos)
                {
                    "x_range": (0, int(img_width * 0.3)),
                    "y_range": (0, int(img_height * 0.3)),
                    "name": "top_left"
                },
                # Center-top (headers)
                {
                    "x_range": (int(img_width * 0.3), int(img_width * 0.7)),
                    "y_range": (0, int(img_height * 0.2)),
                    "name": "center_top"
                },
                # Center (main graphics)
                {
                    "x_range": (int(img_width * 0.2), int(img_width * 0.8)),
                    "y_range": (int(img_height * 0.2), int(img_height * 0.8)),
                    "name": "center"
                },
                # Bottom (footers)
                {
                    "x_range": (int(img_width * 0.2), int(img_width * 0.8)),
                    "y_range": (int(img_height * 0.8), img_height),
                    "name": "bottom"
                }
            ]
            
            for pos in graphic_positions:
                # Create a region for each typical graphic position
                x_min, x_max = pos["x_range"]
                y_min, y_max = pos["y_range"]
                
                region_info = {
                    "bbox": [x_min, y_min, x_max, y_max],
                    "area": (x_max - x_min) * (y_max - y_min),
                    "width": x_max - x_min,
                    "height": y_max - y_min,
                    "center_x": (x_min + x_max) // 2,
                    "center_y": (y_min + y_max) // 2,
                    "page": page_num + 1,
                    "detection_method": "position_based",
                    "position": pos["name"],
                    "confidence": 0.0
                }
                regions.append(region_info)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error finding position-based regions: {e}")
            return []
    
    def find_brightness_based_regions(self, cv_image, page_num):
        """Find regions based on brightness/contrast analysis"""
        
        try:
            regions = []
            
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Calculate local contrast
            kernel_size = 21
            kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
            
            # Local mean
            local_mean = cv2.filter2D(gray.astype(np.float32), -1, kernel)
            
            # Local contrast (standard deviation)
            local_contrast = cv2.filter2D((gray.astype(np.float32) - local_mean) ** 2, -1, kernel)
            local_contrast = np.sqrt(local_contrast)
            
            # Find regions with high contrast
            contrast_threshold = np.percentile(local_contrast, 85)
            contrast_mask = local_contrast > contrast_threshold
            
            # Find contours in contrast mask
            contours, _ = cv2.findContours(contrast_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 200 < area < 15000:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    region_info = {
                        "bbox": [x, y, x + w, y + h],
                        "area": area,
                        "width": w,
                        "height": h,
                        "center_x": x + w // 2,
                        "center_y": y + h // 2,
                        "page": page_num + 1,
                        "detection_method": "brightness_based",
                        "contrast_level": float(np.mean(local_contrast[y:y+h, x:x+w])),
                        "confidence": 0.0
                    }
                    regions.append(region_info)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error finding brightness-based regions: {e}")
            return []
    
    def cluster_similar_regions(self, regions):
        """Cluster similar regions to eliminate duplicates"""
        
        try:
            if not regions:
                return []
            
            # Prepare features for clustering
            features = []
            for region in regions:
                # Normalize features
                center_x_norm = region["center_x"] / 2000
                center_y_norm = region["center_y"] / 2000
                area_norm = region["area"] / 10000
                
                features.append([center_x_norm, center_y_norm, area_norm])
            
            # Use DBSCAN for clustering
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)
            
            # Cluster with DBSCAN
            clustering = DBSCAN(eps=0.4, min_samples=1).fit(features_scaled)
            
            # Group regions by cluster
            clusters = defaultdict(list)
            for i, label in enumerate(clustering.labels_):
                clusters[label].append(regions[i])
            
            # Select best region from each cluster
            clustered_regions = []
            for cluster_id, cluster_regions in clusters.items():
                if len(cluster_regions) == 1:
                    best_region = cluster_regions[0]
                else:
                    best_region = self.select_best_region_from_cluster(cluster_regions)
                
                clustered_regions.append(best_region)
            
            return clustered_regions
            
        except Exception as e:
            logger.error(f"Error clustering regions: {e}")
            return regions
    
    def select_best_region_from_cluster(self, cluster_regions):
        """Select the best region from a cluster"""
        
        try:
            # Score each region
            scored_regions = []
            for region in cluster_regions:
                score = self.calculate_region_score(region)
                scored_regions.append((score, region))
            
            # Return the region with highest score
            scored_regions.sort(key=lambda x: x[0], reverse=True)
            return scored_regions[0][1]
            
        except Exception as e:
            logger.error(f"Error selecting best region: {e}")
            return cluster_regions[0] if cluster_regions else None
    
    def calculate_region_score(self, region):
        """Calculate a score for a region based on graphic characteristics"""
        
        try:
            score = 0.0
            
            # Size scoring (prefer medium-sized regions for graphics)
            area = region["area"]
            if 200 < area < 5000:
                score += 0.3
            elif 5000 < area < 20000:
                score += 0.2
            
            # Position scoring
            if region["detection_method"] == "position_based":
                if region.get("position") == "top_right":
                    score += 0.3
                elif region.get("position") == "center":
                    score += 0.4
                elif region.get("position") == "top_left":
                    score += 0.2
            
            # Method scoring
            if region["detection_method"] == "edge_based":
                score += 0.3
            elif region["detection_method"] == "texture_based":
                score += 0.3
            elif region["detection_method"] == "brightness_based":
                score += 0.2
            elif region["detection_method"] == "color_based":
                score += 0.2
            elif region["detection_method"] == "contour_based":
                score += 0.2
            
            # Aspect ratio scoring
            if "aspect_ratio" in region:
                aspect_ratio = region["aspect_ratio"]
                if 0.3 < aspect_ratio < 5.0:
                    score += 0.2
            
            return score
            
        except Exception as e:
            logger.error(f"Error calculating region score: {e}")
            return 0.0
    
    def rank_regions_by_graphic_probability(self, regions):
        """Rank regions by their probability of being graphics"""
        
        try:
            # Calculate confidence for each region
            for region in regions:
                region["confidence"] = self.calculate_graphic_confidence(region)
            
            # Sort by confidence
            regions.sort(key=lambda x: x["confidence"], reverse=True)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error ranking regions: {e}")
            return regions
    
    def calculate_graphic_confidence(self, region):
        """Calculate confidence that a region contains graphics"""
        
        try:
            confidence = 0.0
            
            # Position-based confidence
            if region["detection_method"] == "position_based":
                if region.get("position") == "center":
                    confidence += 0.4
                elif region.get("position") == "top_right":
                    confidence += 0.3
                elif region.get("position") == "top_left":
                    confidence += 0.2
            
            # Size-based confidence
            area = region["area"]
            if 200 < area < 5000:
                confidence += 0.3
            elif 5000 < area < 20000:
                confidence += 0.2
            
            # Method-based confidence
            if region["detection_method"] == "edge_based":
                confidence += 0.3
            elif region["detection_method"] == "texture_based":
                confidence += 0.3
            elif region["detection_method"] == "brightness_based":
                confidence += 0.2
            elif region["detection_method"] == "color_based":
                confidence += 0.2
            elif region["detection_method"] == "contour_based":
                confidence += 0.2
            
            # Aspect ratio confidence
            if "aspect_ratio" in region:
                aspect_ratio = region["aspect_ratio"]
                if 0.3 < aspect_ratio < 5.0:
                    confidence += 0.2
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating graphic confidence: {e}")
            return 0.0
    
    def generate_region_screenshots(self, pdf_path, regions):
        """Generate screenshots for all regions"""
        
        try:
            screenshots = []
            doc = fitz.open(pdf_path)
            
            # Generate screenshots for all regions (not just top 3)
            for i, region in enumerate(regions):
                page_num = region["page"] - 1
                page = doc[page_num]
                
                # Convert page to image
                mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to PIL Image
                img_data = pix.tobytes("png")
                pil_image = Image.open(io.BytesIO(img_data))
                
                # Extract region
                x1, y1, x2, y2 = region["bbox"]
                region_image = pil_image.crop((x1, y1, x2, y2))
                
                # Save screenshot
                screenshot_path = f"/tmp/graphic_region_{i+1}.png"
                region_image.save(screenshot_path)
                
                screenshot_info = {
                    "region_index": i + 1,
                    "file_path": screenshot_path,
                    "region_bbox": region["bbox"],
                    "confidence": region["confidence"],
                    "detection_method": region["detection_method"],
                    "page": region["page"]
                }
                screenshots.append(screenshot_info)
            
            doc.close()
            return screenshots
            
        except Exception as e:
            logger.error(f"Error generating screenshots: {e}")
            return []
    
    def analyze_screenshots_with_ai(self, screenshots):
        """Analyze each screenshot with OpenAI AI"""
        
        try:
            ai_analysis = []
            
            for screenshot in screenshots:
                try:
                    # Read and encode image
                    with open(screenshot["file_path"], "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode('utf-8')
                    
                    # Prepare OpenAI API request
                    headers = {
                        "Authorization": f"Bearer {self.openai_api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "model": "gpt-4o",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": """Analyze this image and describe what you see. Focus on identifying:
1. Type of graphic (logo, illustration, diagram, chart, icon, etc.)
2. Content description (what the graphic shows)
3. Colors and visual elements
4. Brand or company if recognizable
5. Quality and clarity of the graphic

Provide a detailed analysis in JSON format with these fields:
- graphic_type: (logo/illustration/diagram/chart/icon/other)
- content_description: (detailed description)
- colors: (list of main colors)
- brand_company: (if recognizable, otherwise null)
- quality: (high/medium/low)
- confidence: (0-1 score for your analysis)"""
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{image_data}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "max_tokens": 500
                    }
                    
                    # Make API request
                    response = requests.post(
                        f"{self.openai_base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        ai_content = result["choices"][0]["message"]["content"]
                        
                        # Try to parse JSON from AI response
                        try:
                            # Extract JSON from response (AI might wrap it in markdown)
                            if "```json" in ai_content:
                                json_start = ai_content.find("```json") + 7
                                json_end = ai_content.find("```", json_start)
                                json_str = ai_content[json_start:json_end].strip()
                            else:
                                json_str = ai_content.strip()
                            
                            ai_result = json.loads(json_str)
                        except json.JSONDecodeError:
                            # If JSON parsing fails, create a structured response
                            ai_result = {
                                "graphic_type": "unknown",
                                "content_description": ai_content,
                                "colors": [],
                                "brand_company": None,
                                "quality": "unknown",
                                "confidence": 0.5
                            }
                        
                        analysis_info = {
                            "region_index": screenshot["region_index"],
                            "ai_analysis": ai_result,
                            "raw_response": ai_content,
                            "success": True
                        }
                        
                    else:
                        analysis_info = {
                            "region_index": screenshot["region_index"],
                            "ai_analysis": {
                                "graphic_type": "error",
                                "content_description": f"API Error: {response.status_code}",
                                "colors": [],
                                "brand_company": None,
                                "quality": "unknown",
                                "confidence": 0.0
                            },
                            "raw_response": "",
                            "success": False
                        }
                    
                    ai_analysis.append(analysis_info)
                    
                except Exception as e:
                    logger.error(f"Error analyzing screenshot {screenshot['region_index']}: {e}")
                    analysis_info = {
                        "region_index": screenshot["region_index"],
                        "ai_analysis": {
                            "graphic_type": "error",
                            "content_description": f"Analysis error: {str(e)}",
                            "colors": [],
                            "brand_company": None,
                            "quality": "unknown",
                            "confidence": 0.0
                        },
                        "raw_response": "",
                        "success": False
                    }
                    ai_analysis.append(analysis_info)
            
            return ai_analysis
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            return []
    
    def recommend_graphics(self, regions, ai_analysis):
        """Recommend graphics based on AI analysis"""
        
        try:
            recommendations = []
            
            # Match regions with AI analysis
            for region in regions:
                region_index = regions.index(region) + 1
                
                # Find corresponding AI analysis
                ai_result = None
                for analysis in ai_analysis:
                    if analysis["region_index"] == region_index:
                        ai_result = analysis
                        break
                
                if ai_result and ai_result["success"]:
                    ai_data = ai_result["ai_analysis"]
                    
                    # Calculate overall score
                    overall_score = (region["confidence"] + ai_data.get("confidence", 0.5)) / 2
                    
                    recommendation = {
                        "region": region,
                        "ai_analysis": ai_data,
                        "overall_score": overall_score,
                        "recommendation_reason": self.generate_recommendation_reason(region, ai_data)
                    }
                    
                    recommendations.append(recommendation)
            
            # Sort by overall score
            recommendations.sort(key=lambda x: x["overall_score"], reverse=True)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error recommending graphics: {e}")
            return []
    
    def generate_recommendation_reason(self, region, ai_data):
        """Generate reasoning for recommendation"""
        
        try:
            reasons = []
            
            # Region-based reasons
            if region["confidence"] > 0.6:
                reasons.append("High detection confidence")
            
            if region["detection_method"] == "edge_based":
                reasons.append("Detected through edge analysis")
            
            if region["detection_method"] == "texture_based":
                reasons.append("Detected through texture analysis")
            
            # AI-based reasons
            graphic_type = ai_data.get("graphic_type", "unknown")
            if graphic_type in ["logo", "illustration", "diagram"]:
                reasons.append(f"AI identified as {graphic_type}")
            
            brand = ai_data.get("brand_company")
            if brand:
                reasons.append(f"Recognized brand: {brand}")
            
            quality = ai_data.get("quality", "unknown")
            if quality == "high":
                reasons.append("High quality graphic")
            
            return reasons
            
        except Exception as e:
            logger.error(f"Error generating recommendation reason: {e}")
            return ["Selected based on highest overall score"]
    
    def analyze_graphic_regions(self, regions, ai_analysis):
        """Analyze and summarize graphic regions with AI insights"""
        
        try:
            summary = {
                "total_regions": len(regions),
                "high_confidence_regions": len([r for r in regions if r["confidence"] > 0.7]),
                "medium_confidence_regions": len([r for r in regions if 0.4 < r["confidence"] <= 0.7]),
                "low_confidence_regions": len([r for r in regions if r["confidence"] <= 0.4]),
                "detection_methods": {},
                "ai_analysis_summary": {
                    "graphic_types": {},
                    "brands_companies": [],
                    "quality_distribution": {}
                }
            }
            
            # Count by detection method
            for region in regions:
                method = region["detection_method"]
                summary["detection_methods"][method] = summary["detection_methods"].get(method, 0) + 1
            
            # Analyze AI results
            for analysis in ai_analysis:
                if analysis["success"]:
                    ai_data = analysis["ai_analysis"]
                    
                    # Count graphic types
                    graphic_type = ai_data.get("graphic_type", "unknown")
                    summary["ai_analysis_summary"]["graphic_types"][graphic_type] = \
                        summary["ai_analysis_summary"]["graphic_types"].get(graphic_type, 0) + 1
                    
                    # Collect brands/companies
                    brand = ai_data.get("brand_company")
                    if brand and brand not in summary["ai_analysis_summary"]["brands_companies"]:
                        summary["ai_analysis_summary"]["brands_companies"].append(brand)
                    
                    # Count quality distribution
                    quality = ai_data.get("quality", "unknown")
                    summary["ai_analysis_summary"]["quality_distribution"][quality] = \
                        summary["ai_analysis_summary"]["quality_distribution"].get(quality, 0) + 1
            
            return summary
            
        except Exception as e:
            logger.error(f"Error analyzing graphic regions: {e}")
            return {} 