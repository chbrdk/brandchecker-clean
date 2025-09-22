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
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntelligentLogoDetector:
    """Intelligent logo detection that identifies logo regions and generates screenshots"""
    
    def __init__(self):
        self.logo_regions = []
        self.screenshot_paths = []
        
    def detect_logo_regions(self, pdf_path):
        """Main method to detect logo regions and generate screenshots"""
        
        try:
            logger.info("Starting intelligent logo region detection...")
            
            detection_results = {
                "logo_regions": [],
                "screenshots": [],
                "analysis_summary": {},
                "recommended_regions": []
            }
            
            # Step 1: Find all potential logo regions
            all_regions = self.find_all_potential_regions(pdf_path)
            
            # Step 2: Cluster similar regions to eliminate duplicates
            clustered_regions = self.cluster_similar_regions(all_regions)
            
            # Step 3: Rank regions by logo probability
            ranked_regions = self.rank_regions_by_logo_probability(clustered_regions)
            
            # Step 4: Generate screenshots for top regions
            screenshots = self.generate_region_screenshots(pdf_path, ranked_regions)
            
            # Step 5: Analyze and recommend best logo region
            recommended = self.recommend_best_logo_region(ranked_regions, screenshots)
            
            detection_results["logo_regions"] = ranked_regions
            detection_results["screenshots"] = screenshots
            detection_results["recommended_regions"] = recommended
            detection_results["analysis_summary"] = self.analyze_logo_regions(ranked_regions)
            
            return detection_results
            
        except Exception as e:
            logger.error(f"Error in intelligent logo detection: {e}")
            return {"error": str(e)}
    
    def find_all_potential_regions(self, pdf_path):
        """Find all potential logo regions using multiple methods"""
        
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
                
                # Method 1: Color-based regions
                color_regions = self.find_color_based_regions(cv_image, page_num)
                all_regions.extend(color_regions)
                
                # Method 2: Edge-based regions
                edge_regions = self.find_edge_based_regions(cv_image, page_num)
                all_regions.extend(edge_regions)
                
                # Method 3: Contour-based regions
                contour_regions = self.find_contour_based_regions(cv_image, page_num)
                all_regions.extend(contour_regions)
                
                # Method 4: Position-based regions (top-right corner)
                position_regions = self.find_position_based_regions(cv_image, page_num)
                all_regions.extend(position_regions)
            
            doc.close()
            return all_regions
            
        except Exception as e:
            logger.error(f"Error finding potential regions: {e}")
            return []
    
    def find_color_based_regions(self, cv_image, page_num):
        """Find regions based on logo colors"""
        
        try:
            regions = []
            
            # Convert to HSV for better color analysis
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            
            # Define logo color ranges
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
                    if 100 < area < 10000:  # Filter by size
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
                            "confidence": 0.0  # Will be calculated later
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
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 200 < area < 15000:  # Filter by size
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate edge density
                    roi = edges[y:y+h, x:x+w]
                    edge_density = np.sum(roi > 0) / (w * h)
                    
                    if edge_density > 0.05:  # Minimum edge density
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
            
            # Binary threshold
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 300 < area < 20000:  # Filter by size
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate aspect ratio
                    aspect_ratio = w / h if h > 0 else 0
                    
                    # Filter by aspect ratio (logos are usually not too extreme)
                    if 0.3 < aspect_ratio < 5.0:
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
                            "confidence": 0.0
                        }
                        regions.append(region_info)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error finding contour-based regions: {e}")
            return []
    
    def find_position_based_regions(self, cv_image, page_num):
        """Find regions based on typical logo positions"""
        
        try:
            regions = []
            
            img_height, img_width = cv_image.shape[:2]
            
            # Define typical logo positions
            logo_positions = [
                # Top-right corner
                {
                    "x_range": (int(img_width * 0.7), int(img_width * 0.95)),
                    "y_range": (0, int(img_height * 0.3)),
                    "name": "top_right"
                },
                # Top-left corner
                {
                    "x_range": (0, int(img_width * 0.3)),
                    "y_range": (0, int(img_height * 0.3)),
                    "name": "top_left"
                },
                # Center-top
                {
                    "x_range": (int(img_width * 0.3), int(img_width * 0.7)),
                    "y_range": (0, int(img_height * 0.2)),
                    "name": "center_top"
                }
            ]
            
            for pos in logo_positions:
                # Create a region for each typical logo position
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
    
    def cluster_similar_regions(self, regions):
        """Cluster similar regions to eliminate duplicates"""
        
        try:
            if not regions:
                return []
            
            # Prepare features for clustering
            features = []
            for region in regions:
                # Normalize features
                center_x_norm = region["center_x"] / 2000  # Normalize by typical image width
                center_y_norm = region["center_y"] / 2000  # Normalize by typical image height
                area_norm = region["area"] / 10000  # Normalize by typical area
                
                features.append([center_x_norm, center_y_norm, area_norm])
            
            # Use DBSCAN for clustering
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)
            
            # Cluster with DBSCAN
            clustering = DBSCAN(eps=0.3, min_samples=1).fit(features_scaled)
            
            # Group regions by cluster
            clusters = defaultdict(list)
            for i, label in enumerate(clustering.labels_):
                clusters[label].append(regions[i])
            
            # Select best region from each cluster
            clustered_regions = []
            for cluster_id, cluster_regions in clusters.items():
                if len(cluster_regions) == 1:
                    # Single region, keep as is
                    best_region = cluster_regions[0]
                else:
                    # Multiple regions, select the best one
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
        """Calculate a score for a region based on logo characteristics"""
        
        try:
            score = 0.0
            
            # Size scoring (prefer medium-sized regions)
            area = region["area"]
            if 500 < area < 5000:
                score += 0.3
            elif 1000 < area < 10000:
                score += 0.2
            
            # Position scoring (prefer top-right)
            if region["detection_method"] == "position_based":
                if region.get("position") == "top_right":
                    score += 0.4
                elif region.get("position") == "top_left":
                    score += 0.2
            
            # Method scoring
            if region["detection_method"] == "color_based":
                score += 0.2
            elif region["detection_method"] == "edge_based":
                score += 0.3
            elif region["detection_method"] == "contour_based":
                score += 0.2
            
            # Aspect ratio scoring
            if "aspect_ratio" in region:
                aspect_ratio = region["aspect_ratio"]
                if 0.5 < aspect_ratio < 3.0:
                    score += 0.2
            
            return score
            
        except Exception as e:
            logger.error(f"Error calculating region score: {e}")
            return 0.0
    
    def rank_regions_by_logo_probability(self, regions):
        """Rank regions by their probability of being a logo"""
        
        try:
            # Calculate confidence for each region
            for region in regions:
                region["confidence"] = self.calculate_logo_confidence(region)
            
            # Sort by confidence
            regions.sort(key=lambda x: x["confidence"], reverse=True)
            
            return regions
            
        except Exception as e:
            logger.error(f"Error ranking regions: {e}")
            return regions
    
    def calculate_logo_confidence(self, region):
        """Calculate confidence that a region contains a logo"""
        
        try:
            confidence = 0.0
            
            # Position-based confidence
            if region["detection_method"] == "position_based":
                if region.get("position") == "top_right":
                    confidence += 0.4
                elif region.get("position") == "top_left":
                    confidence += 0.3
                elif region.get("position") == "center_top":
                    confidence += 0.2
            
            # Size-based confidence
            area = region["area"]
            if 500 < area < 3000:
                confidence += 0.3
            elif 3000 < area < 10000:
                confidence += 0.2
            
            # Method-based confidence
            if region["detection_method"] == "color_based":
                confidence += 0.2
            elif region["detection_method"] == "edge_based":
                confidence += 0.3
            elif region["detection_method"] == "contour_based":
                confidence += 0.2
            
            # Aspect ratio confidence
            if "aspect_ratio" in region:
                aspect_ratio = region["aspect_ratio"]
                if 0.5 < aspect_ratio < 3.0:
                    confidence += 0.2
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating logo confidence: {e}")
            return 0.0
    
    def generate_region_screenshots(self, pdf_path, regions):
        """Generate screenshots for the top regions"""
        
        try:
            screenshots = []
            doc = fitz.open(pdf_path)
            
            # Take top 3 regions for screenshot generation
            top_regions = regions[:3]
            
            for i, region in enumerate(top_regions):
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
                screenshot_path = f"/tmp/logo_region_{i+1}.png"
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
    
    def recommend_best_logo_region(self, regions, screenshots):
        """Recommend the best logo region based on analysis"""
        
        try:
            if not regions:
                return None
            
            # Select the region with highest confidence
            best_region = regions[0]
            
            # Find corresponding screenshot
            best_screenshot = None
            for screenshot in screenshots:
                if screenshot["region_index"] == 1:  # Top region
                    best_screenshot = screenshot
                    break
            
            recommendation = {
                "best_region": best_region,
                "screenshot_path": best_screenshot["file_path"] if best_screenshot else None,
                "confidence": best_region["confidence"],
                "reasoning": self.generate_recommendation_reasoning(best_region),
                "ai_ready": True
            }
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error recommending best region: {e}")
            return None
    
    def generate_recommendation_reasoning(self, region):
        """Generate reasoning for why this region was selected"""
        
        try:
            reasons = []
            
            if region["confidence"] > 0.7:
                reasons.append("High confidence score")
            
            if region["detection_method"] == "position_based" and region.get("position") == "top_right":
                reasons.append("Located in typical logo position (top-right)")
            
            if 500 < region["area"] < 5000:
                reasons.append("Appropriate size for a logo")
            
            if region["detection_method"] == "edge_based":
                reasons.append("Detected through edge analysis")
            
            if "aspect_ratio" in region and 0.5 < region["aspect_ratio"] < 3.0:
                reasons.append("Good aspect ratio for logo")
            
            return reasons
            
        except Exception as e:
            logger.error(f"Error generating reasoning: {e}")
            return ["Selected based on highest confidence score"]
    
    def analyze_logo_regions(self, regions):
        """Analyze and summarize logo regions"""
        
        try:
            summary = {
                "total_regions": len(regions),
                "high_confidence_regions": len([r for r in regions if r["confidence"] > 0.7]),
                "medium_confidence_regions": len([r for r in regions if 0.4 < r["confidence"] <= 0.7]),
                "low_confidence_regions": len([r for r in regions if r["confidence"] <= 0.4]),
                "detection_methods": {},
                "position_distribution": {},
                "size_distribution": {}
            }
            
            # Count by detection method
            for region in regions:
                method = region["detection_method"]
                summary["detection_methods"][method] = summary["detection_methods"].get(method, 0) + 1
            
            # Count by position
            for region in regions:
                if region["detection_method"] == "position_based":
                    position = region.get("position", "unknown")
                    summary["position_distribution"][position] = summary["position_distribution"].get(position, 0) + 1
            
            # Count by size
            for region in regions:
                area = region["area"]
                if area < 1000:
                    size_cat = "small"
                elif area < 5000:
                    size_cat = "medium"
                else:
                    size_cat = "large"
                summary["size_distribution"][size_cat] = summary["size_distribution"].get(size_cat, 0) + 1
            
            return summary
            
        except Exception as e:
            logger.error(f"Error analyzing logo regions: {e}")
            return {} 