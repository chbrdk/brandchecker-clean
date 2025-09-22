import os
import json
import logging
import numpy as np
from collections import defaultdict, Counter
import fitz  # PyMuPDF
from PIL import Image
import cv2
import io
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomLogoDetector:
    """Custom logo detection system using multiple approaches"""
    
    def __init__(self):
        self.logo_patterns = {
            "bosch": {
                "colors": ["#1b0afe", "#e2000e", "#000000"],  # Blue, Red, Black
                "position": "top_right",
                "size_range": (50, 200),
                "aspect_ratio": (0.8, 2.0)
            },
            "generic_logo": {
                "colors": ["#1b0afe", "#e2000e", "#000000", "#ffffff"],  # Common logo colors
                "position": "any",
                "size_range": (30, 500),
                "aspect_ratio": (0.5, 3.0)
            }
        }
    
    def detect_logos_in_pdf(self, pdf_path):
        """Main method to detect logos in PDF using custom approaches"""
        
        try:
            logger.info("Starting custom logo detection...")
            
            detection_results = {
                "logos": [],
                "logo_candidates": [],
                "color_regions": [],
                "pattern_matches": [],
                "analysis_summary": {}
            }
            
            # Method 1: Color-based logo detection
            color_logos = self.detect_logos_by_color(pdf_path)
            detection_results["logos"].extend(color_logos)
            
            # Method 2: Region-based logo detection
            region_logos = self.detect_logos_by_region(pdf_path)
            detection_results["logos"].extend(region_logos)
            
            # Method 3: Pattern-based logo detection
            pattern_logos = self.detect_logos_by_pattern(pdf_path)
            detection_results["logos"].extend(pattern_logos)
            
            # Method 4: Content-stream logo detection
            content_logos = self.detect_logos_in_content_stream(pdf_path)
            detection_results["logos"].extend(content_logos)
            
            # Method 5: Pixel-based logo detection
            pixel_logos = self.detect_logos_by_pixel_analysis(pdf_path)
            detection_results["logos"].extend(pixel_logos)
            
            # Combine and rank results
            detection_results["analysis_summary"] = self.analyze_detection_results(detection_results)
            
            return detection_results
            
        except Exception as e:
            logger.error(f"Error in custom logo detection: {e}")
            return {"error": str(e)}
    
    def detect_logos_by_color(self, pdf_path):
        """Detect logos based on color analysis"""
        
        try:
            logos = []
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
                
                # Analyze colors
                color_regions = self.analyze_color_regions(cv_image)
                
                for region in color_regions:
                    if self.is_logo_color_region(region):
                        logo_info = {
                            "type": "color_based_logo",
                            "page": page_num + 1,
                            "rect": region["bbox"],
                            "colors": region["colors"],
                            "confidence": region["confidence"],
                            "detection_method": "color_analysis",
                            "area": region["area"],
                            "center_x": region["center_x"],
                            "center_y": region["center_y"]
                        }
                        logos.append(logo_info)
            
            doc.close()
            return logos
            
        except Exception as e:
            logger.error(f"Error in color-based logo detection: {e}")
            return []
    
    def analyze_color_regions(self, cv_image):
        """Analyze image for color regions that might be logos"""
        
        try:
            regions = []
            
            # Convert to HSV for better color analysis
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            
            # Define color ranges for logo colors
            color_ranges = {
                "blue": ([100, 50, 50], [130, 255, 255]),
                "red": ([0, 50, 50], [10, 255, 255]),
                "red2": ([170, 50, 50], [180, 255, 255]),
                "black": ([0, 0, 0], [180, 255, 30]),
                "white": ([0, 0, 200], [180, 30, 255])
            }
            
            for color_name, (lower, upper) in color_ranges.items():
                # Create mask for color
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                
                # Find contours
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > 100:  # Filter small regions
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        # Calculate confidence based on area and position
                        confidence = self.calculate_color_confidence(area, x, y, w, h, cv_image.shape)
                        
                        if confidence > 0.3:  # Minimum confidence threshold
                            region_info = {
                                "color": color_name,
                                "bbox": [x, y, x + w, y + h],
                                "area": area,
                                "width": w,
                                "height": h,
                                "center_x": x + w // 2,
                                "center_y": y + h // 2,
                                "confidence": confidence,
                                "colors": [color_name]
                            }
                            regions.append(region_info)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error analyzing color regions: {e}")
            return []
    
    def calculate_color_confidence(self, area, x, y, w, h, image_shape):
        """Calculate confidence score for a color region being a logo"""
        
        try:
            confidence = 0.0
            
            # Size-based scoring
            if 100 < area < 1000:
                confidence += 0.2
            elif 1000 < area < 5000:
                confidence += 0.3
            elif 5000 < area < 20000:
                confidence += 0.2
            
            # Position-based scoring (top-right for logos)
            img_height, img_width = image_shape[:2]
            if x > img_width * 0.7 and y < img_height * 0.3:
                confidence += 0.3
            elif x > img_width * 0.5 and y < img_height * 0.5:
                confidence += 0.2
            
            # Aspect ratio scoring
            aspect_ratio = w / h if h > 0 else 0
            if 0.5 < aspect_ratio < 3.0:
                confidence += 0.2
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating color confidence: {e}")
            return 0.0
    
    def is_logo_color_region(self, region):
        """Check if a color region matches logo characteristics"""
        
        try:
            # Check if colors match known logo colors
            logo_colors = ["blue", "red", "black", "white"]
            if region["color"] in logo_colors:
                return True
            
            # Check size and position
            if region["confidence"] > 0.5:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking logo color region: {e}")
            return False
    
    def detect_logos_by_region(self, pdf_path):
        """Detect logos based on region analysis"""
        
        try:
            logos = []
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Convert page to image
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                pil_image = Image.open(io.BytesIO(img_data))
                cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                
                # Find regions of interest
                regions = self.find_regions_of_interest(cv_image)
                
                for region in regions:
                    if self.is_logo_region(region):
                        logo_info = {
                            "type": "region_based_logo",
                            "page": page_num + 1,
                            "rect": region["bbox"],
                            "confidence": region["confidence"],
                            "detection_method": "region_analysis",
                            "area": region["area"],
                            "center_x": region["center_x"],
                            "center_y": region["center_y"],
                            "region_type": region["type"]
                        }
                        logos.append(logo_info)
            
            doc.close()
            return logos
            
        except Exception as e:
            logger.error(f"Error in region-based logo detection: {e}")
            return []
    
    def find_regions_of_interest(self, cv_image):
        """Find regions that might contain logos"""
        
        try:
            regions = []
            
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 200:  # Filter small contours
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Analyze region characteristics
                    region_type = self.classify_region(cv_image, x, y, w, h)
                    confidence = self.calculate_region_confidence(area, x, y, w, h, cv_image.shape, region_type)
                    
                    if confidence > 0.4:
                        region_info = {
                            "bbox": [x, y, x + w, y + h],
                            "area": area,
                            "width": w,
                            "height": h,
                            "center_x": x + w // 2,
                            "center_y": y + h // 2,
                            "confidence": confidence,
                            "type": region_type
                        }
                        regions.append(region_info)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error finding regions of interest: {e}")
            return []
    
    def classify_region(self, cv_image, x, y, w, h):
        """Classify a region based on its characteristics"""
        
        try:
            # Extract region
            region = cv_image[y:y+h, x:x+w]
            
            # Calculate features
            gray_region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            
            # Edge density
            edges = cv2.Canny(gray_region, 50, 150)
            edge_density = np.sum(edges > 0) / (w * h)
            
            # Color variance
            color_variance = np.var(region)
            
            # Classify based on features
            if edge_density > 0.1 and color_variance > 1000:
                return "complex_logo"
            elif edge_density > 0.05:
                return "simple_logo"
            elif color_variance > 500:
                return "colorful_logo"
            else:
                return "text_logo"
                
        except Exception as e:
            logger.error(f"Error classifying region: {e}")
            return "unknown"
    
    def calculate_region_confidence(self, area, x, y, w, h, image_shape, region_type):
        """Calculate confidence for a region being a logo"""
        
        try:
            confidence = 0.0
            
            # Size-based scoring
            if 200 < area < 2000:
                confidence += 0.2
            elif 2000 < area < 10000:
                confidence += 0.3
            elif 10000 < area < 50000:
                confidence += 0.2
            
            # Position-based scoring
            img_height, img_width = image_shape[:2]
            if x > img_width * 0.6 and y < img_height * 0.4:
                confidence += 0.3
            elif x > img_width * 0.4 and y < img_height * 0.6:
                confidence += 0.2
            
            # Type-based scoring
            if region_type == "complex_logo":
                confidence += 0.3
            elif region_type == "simple_logo":
                confidence += 0.2
            elif region_type == "colorful_logo":
                confidence += 0.2
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating region confidence: {e}")
            return 0.0
    
    def is_logo_region(self, region):
        """Check if a region matches logo characteristics"""
        
        try:
            # Check confidence threshold
            if region["confidence"] > 0.5:
                return True
            
            # Check region type
            if region["type"] in ["complex_logo", "simple_logo", "colorful_logo"]:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking logo region: {e}")
            return False
    
    def detect_logos_by_pattern(self, pdf_path):
        """Detect logos based on pattern matching"""
        
        try:
            logos = []
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Convert page to image
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                pil_image = Image.open(io.BytesIO(img_data))
                cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                
                # Pattern matching for known logos
                for pattern_name, pattern in self.logo_patterns.items():
                    matches = self.match_logo_pattern(cv_image, pattern)
                    
                    for match in matches:
                        logo_info = {
                            "type": f"pattern_based_{pattern_name}",
                            "page": page_num + 1,
                            "rect": match["bbox"],
                            "confidence": match["confidence"],
                            "detection_method": "pattern_matching",
                            "pattern": pattern_name,
                            "area": match["area"],
                            "center_x": match["center_x"],
                            "center_y": match["center_y"]
                        }
                        logos.append(logo_info)
            
            doc.close()
            return logos
            
        except Exception as e:
            logger.error(f"Error in pattern-based logo detection: {e}")
            return []
    
    def match_logo_pattern(self, cv_image, pattern):
        """Match a logo pattern in the image"""
        
        try:
            matches = []
            
            # Extract dominant colors from image
            dominant_colors = self.extract_dominant_colors(cv_image)
            
            # Check if pattern colors are present
            color_matches = 0
            for pattern_color in pattern["colors"]:
                for dom_color in dominant_colors:
                    if self.colors_are_similar(pattern_color, dom_color):
                        color_matches += 1
            
            # If colors match, look for regions
            if color_matches > 0:
                regions = self.find_regions_of_interest(cv_image)
                
                for region in regions:
                    # Check if region matches pattern criteria
                    if self.region_matches_pattern(region, pattern):
                        match_info = {
                            "bbox": region["bbox"],
                            "confidence": region["confidence"] * (color_matches / len(pattern["colors"])),
                            "area": region["area"],
                            "center_x": region["center_x"],
                            "center_y": region["center_y"]
                        }
                        matches.append(match_info)
            
            return matches
            
        except Exception as e:
            logger.error(f"Error matching logo pattern: {e}")
            return []
    
    def extract_dominant_colors(self, cv_image):
        """Extract dominant colors from image"""
        
        try:
            # Reshape image for clustering
            pixels = cv_image.reshape(-1, 3)
            
            # Use K-means to find dominant colors
            kmeans = KMeans(n_clusters=5, random_state=42)
            kmeans.fit(pixels)
            
            # Get dominant colors
            colors = kmeans.cluster_centers_.astype(int)
            
            # Convert to hex format
            hex_colors = []
            for color in colors:
                hex_color = "#{:02x}{:02x}{:02x}".format(color[2], color[1], color[0])
                hex_colors.append(hex_color)
            
            return hex_colors
            
        except Exception as e:
            logger.error(f"Error extracting dominant colors: {e}")
            return []
    
    def colors_are_similar(self, color1, color2, threshold=50):
        """Check if two colors are similar"""
        
        try:
            # Convert hex to RGB
            def hex_to_rgb(hex_color):
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            rgb1 = hex_to_rgb(color1)
            rgb2 = hex_to_rgb(color2)
            
            # Calculate Euclidean distance
            distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))
            
            return distance < threshold
            
        except Exception as e:
            logger.error(f"Error comparing colors: {e}")
            return False
    
    def region_matches_pattern(self, region, pattern):
        """Check if a region matches a logo pattern"""
        
        try:
            # Check size range
            min_size, max_size = pattern["size_range"]
            if not (min_size <= region["area"] <= max_size):
                return False
            
            # Check aspect ratio
            aspect_ratio = region["width"] / region["height"] if region["height"] > 0 else 0
            min_ratio, max_ratio = pattern["aspect_ratio"]
            if not (min_ratio <= aspect_ratio <= max_ratio):
                return False
            
            # Check position
            if pattern["position"] == "top_right":
                # This would need image dimensions to check properly
                pass
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking pattern match: {e}")
            return False
    
    def detect_logos_in_content_stream(self, pdf_path):
        """Detect logos by analyzing PDF content streams"""
        
        try:
            logos = []
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Get content stream
                try:
                    content_stream = page.get_contents()
                    if content_stream:
                        # Analyze content stream for logo patterns
                        logo_patterns = self.analyze_content_stream_for_logos(content_stream)
                        
                        for pattern in logo_patterns:
                            logo_info = {
                                "type": "content_stream_logo",
                                "page": page_num + 1,
                                "rect": pattern["bbox"],
                                "confidence": pattern["confidence"],
                                "detection_method": "content_stream_analysis",
                                "pattern_type": pattern["type"],
                                "area": pattern["area"],
                                "center_x": pattern["center_x"],
                                "center_y": pattern["center_y"]
                            }
                            logos.append(logo_info)
                except:
                    pass
            
            doc.close()
            return logos
            
        except Exception as e:
            logger.error(f"Error in content stream logo detection: {e}")
            return []
    
    def analyze_content_stream_for_logos(self, content_stream):
        """Analyze content stream for logo patterns"""
        
        try:
            patterns = []
            
            # Convert content stream to string
            if hasattr(content_stream, 'read'):
                content_str = content_stream.read().decode('utf-8', errors='ignore')
            else:
                content_str = str(content_stream)
            
            # Look for image operators
            if "Do" in content_str or "BI" in content_str:
                # Found image content
                pattern_info = {
                    "bbox": [0, 0, 100, 100],  # Default bbox
                    "confidence": 0.6,
                    "type": "image_operator",
                    "area": 10000,
                    "center_x": 50,
                    "center_y": 50
                }
                patterns.append(pattern_info)
            
            # Look for drawing operators
            if "m" in content_str or "l" in content_str or "c" in content_str:
                # Found drawing content
                pattern_info = {
                    "bbox": [0, 0, 100, 100],  # Default bbox
                    "confidence": 0.5,
                    "type": "drawing_operator",
                    "area": 10000,
                    "center_x": 50,
                    "center_y": 50
                }
                patterns.append(pattern_info)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing content stream: {e}")
            return []
    
    def detect_logos_by_pixel_analysis(self, pdf_path):
        """Detect logos by pixel-level analysis"""
        
        try:
            logos = []
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Convert page to image
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                pil_image = Image.open(io.BytesIO(img_data))
                cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                
                # Pixel-level analysis
                pixel_regions = self.analyze_pixel_patterns(cv_image)
                
                for region in pixel_regions:
                    if self.is_logo_pixel_region(region):
                        logo_info = {
                            "type": "pixel_based_logo",
                            "page": page_num + 1,
                            "rect": region["bbox"],
                            "confidence": region["confidence"],
                            "detection_method": "pixel_analysis",
                            "pixel_density": region["pixel_density"],
                            "area": region["area"],
                            "center_x": region["center_x"],
                            "center_y": region["center_y"]
                        }
                        logos.append(logo_info)
            
            doc.close()
            return logos
            
        except Exception as e:
            logger.error(f"Error in pixel-based logo detection: {e}")
            return []
    
    def analyze_pixel_patterns(self, cv_image):
        """Analyze pixel patterns for logo detection"""
        
        try:
            regions = []
            
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Calculate pixel density
            kernel = np.ones((5, 5), np.uint8)
            dilated = cv2.dilate(gray, kernel, iterations=1)
            
            # Find regions with high pixel density
            _, binary = cv2.threshold(dilated, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate pixel density
                    roi = gray[y:y+h, x:x+w]
                    pixel_density = np.sum(roi > 127) / (w * h)
                    
                    if pixel_density > 0.3:  # High pixel density threshold
                        confidence = self.calculate_pixel_confidence(area, pixel_density, x, y, w, h, cv_image.shape)
                        
                        if confidence > 0.4:
                            region_info = {
                                "bbox": [x, y, x + w, y + h],
                                "area": area,
                                "width": w,
                                "height": h,
                                "center_x": x + w // 2,
                                "center_y": y + h // 2,
                                "confidence": confidence,
                                "pixel_density": pixel_density
                            }
                            regions.append(region_info)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error analyzing pixel patterns: {e}")
            return []
    
    def calculate_pixel_confidence(self, area, pixel_density, x, y, w, h, image_shape):
        """Calculate confidence for pixel-based logo detection"""
        
        try:
            confidence = 0.0
            
            # Size-based scoring
            if 100 < area < 2000:
                confidence += 0.2
            elif 2000 < area < 10000:
                confidence += 0.3
            
            # Pixel density scoring
            if pixel_density > 0.5:
                confidence += 0.3
            elif pixel_density > 0.3:
                confidence += 0.2
            
            # Position-based scoring
            img_height, img_width = image_shape[:2]
            if x > img_width * 0.6 and y < img_height * 0.4:
                confidence += 0.3
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating pixel confidence: {e}")
            return 0.0
    
    def is_logo_pixel_region(self, region):
        """Check if a pixel region matches logo characteristics"""
        
        try:
            # Check confidence threshold
            if region["confidence"] > 0.5:
                return True
            
            # Check pixel density
            if region["pixel_density"] > 0.4:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking logo pixel region: {e}")
            return False
    
    def analyze_detection_results(self, detection_results):
        """Analyze and summarize detection results"""
        
        try:
            summary = {
                "total_logos": len(detection_results["logos"]),
                "detection_methods": {},
                "confidence_distribution": {},
                "page_distribution": {},
                "logo_types": {}
            }
            
            # Count by detection method
            for logo in detection_results["logos"]:
                method = logo["detection_method"]
                summary["detection_methods"][method] = summary["detection_methods"].get(method, 0) + 1
            
            # Count by confidence level
            for logo in detection_results["logos"]:
                conf = logo["confidence"]
                if conf > 0.8:
                    level = "high"
                elif conf > 0.5:
                    level = "medium"
                else:
                    level = "low"
                summary["confidence_distribution"][level] = summary["confidence_distribution"].get(level, 0) + 1
            
            # Count by page
            for logo in detection_results["logos"]:
                page = logo["page"]
                summary["page_distribution"][page] = summary["page_distribution"].get(page, 0) + 1
            
            # Count by logo type
            for logo in detection_results["logos"]:
                logo_type = logo["type"]
                summary["logo_types"][logo_type] = summary["logo_types"].get(logo_type, 0) + 1
            
            return summary
            
        except Exception as e:
            logger.error(f"Error analyzing detection results: {e}")
            return {} 