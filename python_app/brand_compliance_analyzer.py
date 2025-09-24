#!/usr/bin/env python3
"""
Brand Compliance Analyzer mit Farb-Ähnlichkeits-Bewertung
Analysiert PDF-Extraktionsergebnisse gegen offizielle Brand Guidelines
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import colorsys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrandComplianceAnalyzer:
    def __init__(self):
        self.bosch_official_colors = {
            "#007bc0": {"name": "Bosch Blau 50", "rgb": "RGB(0, 123, 192)", "cmyk": "CMYK(100, 36, 0, 25)"},
            "#ed0007": {"name": "Bosch Rot", "rgb": "RGB(237, 0, 7)", "cmyk": "CMYK(0, 100, 97, 7)"},
            "#71767c": {"name": "Bosch Grau 50", "rgb": "RGB(113, 118, 124)", "cmyk": "CMYK(9, 5, 0, 51)"},
            "#000000": {"name": "Schwarz", "rgb": "RGB(0, 0, 0)", "cmyk": "CMYK(0, 0, 0, 100)"},
            "#ffffff": {"name": "Weiß", "rgb": "RGB(255, 255, 255)", "cmyk": "CMYK(0, 0, 0, 0)"}
        }
        
        self.bosch_official_fonts = [
            "BoschSans-Regular", "BoschSans-Bold", "BoschSans-Light", 
            "BoschSans-Medium", "BoschSans-Heavy", "BoschSans-Thin"
        ]
    
    def hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert HEX color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hsv(self, r: int, g: int, b: int) -> tuple:
        """Convert RGB to HSV"""
        r, g, b = r/255.0, g/255.0, b/255.0
        return colorsys.rgb_to_hsv(r, g, b)
    
    def color_similarity(self, color1: str, color2: str) -> float:
        """Calculate color similarity between two HEX colors (0-1, higher = more similar)"""
        try:
            rgb1 = self.hex_to_rgb(color1)
            rgb2 = self.hex_to_rgb(color2)
            
            # Convert to HSV for better perceptual similarity
            hsv1 = self.rgb_to_hsv(*rgb1)
            hsv2 = self.rgb_to_hsv(*rgb2)
            
            # Calculate weighted distance
            h_diff = min(abs(hsv1[0] - hsv2[0]), 1 - abs(hsv1[0] - hsv2[0]))  # Hue is circular
            s_diff = abs(hsv1[1] - hsv2[1])
            v_diff = abs(hsv1[2] - hsv2[2])
            
            # Weighted similarity (hue is most important, then saturation, then value)
            similarity = 1 - (0.6 * h_diff + 0.3 * s_diff + 0.1 * v_diff)
            return max(0, min(1, similarity))
            
        except Exception as e:
            logger.error(f"Error calculating color similarity: {e}")
            return 0.0
    
    def find_best_color_match(self, target_color: str, threshold: float = 0.7) -> Optional[Dict[str, Any]]:
        """Find the best matching Bosch color for a target color"""
        best_match = None
        best_similarity = 0
        
        for hex_value, color_info in self.bosch_official_colors.items():
            similarity = self.color_similarity(target_color, hex_value)
            if similarity >= threshold and similarity > best_similarity:
                best_match = {
                    'hex': hex_value,
                    'name': color_info['name'],
                    'similarity': similarity,
                    'rgb': color_info['rgb'],
                    'cmyk': color_info['cmyk']
                }
                best_similarity = similarity
        
        return best_match
    
    def analyze_font_compliance(self, fonts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze font compliance against Bosch guidelines"""
        approved_fonts = []
        non_compliant_fonts = []
        
        for font in fonts:
            font_name = font.get('name', '')
            usage_percentage = font.get('usage_percentage', 0)
            
            # Check if font is Bosch-approved
            is_bosch_font = any(bosch_font in font_name for bosch_font in self.bosch_official_fonts)
            
            if is_bosch_font:
                approved_fonts.append({
                    'name': font_name,
                    'usage_percentage': usage_percentage,
                    'compliance': 'approved'
                })
            else:
                # Find closest Bosch font
                closest_bosch = None
                for bosch_font in self.bosch_official_fonts:
                    if bosch_font.lower() in font_name.lower() or font_name.lower() in bosch_font.lower():
                        closest_bosch = bosch_font
                        break
                
                non_compliant_fonts.append({
                    'name': font_name,
                    'usage_percentage': usage_percentage,
                    'compliance': 'not_approved',
                    'recommendation': f"Replace with {closest_bosch or 'BoschSans-Regular'}"
                })
        
        # Calculate score
        total_usage = sum(f.get('usage_percentage', 0) for f in fonts)
        approved_usage = sum(f.get('usage_percentage', 0) for f in approved_fonts)
        
        score = int((approved_usage / total_usage * 100)) if total_usage > 0 else 100
        
        return {
            'score': score,
            'status': 'compliant' if score >= 90 else 'mostly_compliant' if score >= 70 else 'needs_improvement',
            'approved_fonts': approved_fonts,
            'non_compliant_fonts': non_compliant_fonts,
            'recommendations': [
                f"Use official Bosch font family" if non_compliant_fonts else "Excellent font usage",
                "Maintain consistent typography"
            ]
        }
    
    def analyze_color_compliance(self, colors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze color compliance against Bosch guidelines with similarity matching"""
        approved_colors = []
        non_compliant_colors = []
        similar_colors = []
        
        for color in colors:
            hex_value = color.get('hex', '')
            usage_percentage = color.get('usage_percentage', 0)
            color_name = color.get('name', 'Unknown')
            
            # Check for exact match first
            if hex_value in self.bosch_official_colors:
                approved_colors.append({
                    'hex': hex_value,
                    'name': self.bosch_official_colors[hex_value]['name'],
                    'usage_percentage': usage_percentage,
                    'compliance': 'approved'
                })
            else:
                # Check for similar color
                best_match = self.find_best_color_match(hex_value, threshold=0.75)
                
                if best_match:
                    similar_colors.append({
                        'original_hex': hex_value,
                        'original_name': color_name,
                        'matched_hex': best_match['hex'],
                        'matched_name': best_match['name'],
                        'similarity': best_match['similarity'],
                        'usage_percentage': usage_percentage,
                        'compliance': 'similar',
                        'recommendation': f"Consider using {best_match['name']} ({best_match['hex']}) instead"
                    })
                else:
                    non_compliant_colors.append({
                        'hex': hex_value,
                        'name': color_name,
                        'usage_percentage': usage_percentage,
                        'compliance': 'not_approved',
                        'recommendation': "Replace with official Bosch color palette"
                    })
        
        # Calculate score (exact matches + similar matches with penalty)
        total_usage = sum(c.get('usage_percentage', 0) for c in colors)
        approved_usage = sum(c.get('usage_percentage', 0) for c in approved_colors)
        similar_usage = sum(c.get('usage_percentage', 0) * 0.7 for c in similar_colors)  # 70% credit for similar
        non_compliant_usage = sum(c.get('usage_percentage', 0) for c in non_compliant_colors)
        
        score = int(((approved_usage + similar_usage) / total_usage * 100)) if total_usage > 0 else 100
        
        # Add similar colors to approved for display
        approved_colors.extend(similar_colors)
        
        return {
            'score': score,
            'status': 'compliant' if score >= 90 else 'mostly_compliant' if score >= 70 else 'needs_improvement',
            'approved_colors': approved_colors,
            'non_compliant_colors': non_compliant_colors,
            'recommendations': [
                "Use official Bosch color palette",
                f"Reduce non-brand colors to <5%" if non_compliant_usage > 5 else "Excellent color usage"
            ]
        }
    
    def analyze_compliance(self, analysis_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Main compliance analysis function"""
        if not analysis_data or len(analysis_data) == 0:
            return {"error": "No analysis data provided"}
        
        data = analysis_data[0]  # Assuming single document analysis
        
        # Extract data
        colors = data.get('colors', [])
        fonts = data.get('fonts', [])
        filename = data.get('filename', 'unknown')
        total_pages = data.get('total_pages', 1)
        
        # Analyze compliance
        color_compliance = self.analyze_color_compliance(colors)
        font_compliance = self.analyze_font_compliance(fonts)
        
        # Calculate overall score
        overall_score = int((color_compliance['score'] + font_compliance['score']) / 2)
        
        # Determine overall status
        if overall_score >= 90:
            compliance_status = "compliant"
        elif overall_score >= 70:
            compliance_status = "mostly_compliant"
        elif overall_score >= 50:
            compliance_status = "partially_compliant"
        else:
            compliance_status = "non_compliant"
        
        # Generate recommendations
        overall_recommendations = []
        if color_compliance['non_compliant_colors']:
            overall_recommendations.append("Replace non-brand colors with official palette")
        if font_compliance['non_compliant_fonts']:
            overall_recommendations.append("Use official Bosch font family")
        
        if not overall_recommendations:
            overall_recommendations.append("Document meets brand guidelines")
        
        # Identify strengths and weaknesses
        strengths = []
        weaknesses = []
        
        if color_compliance['score'] >= 90:
            strengths.append("Excellent color usage")
        elif color_compliance['score'] < 70:
            weaknesses.append("Non-compliant colors detected")
            
        if font_compliance['score'] >= 90:
            strengths.append("Perfect font usage")
        elif font_compliance['score'] < 70:
            weaknesses.append("Non-compliant fonts detected")
        
        return {
            "brand_compliance_assessment": {
                "overall_score": overall_score,
                "compliance_status": compliance_status,
                "assessment_date": datetime.utcnow().isoformat() + "Z",
                "document_info": {
                    "filename": filename,
                    "total_pages": total_pages,
                    "analysis_confidence": "high"
                },
                "color_compliance": color_compliance,
                "font_compliance": font_compliance,
                "overall_recommendations": overall_recommendations,
                "compliance_summary": {
                    "strengths": strengths,
                    "weaknesses": weaknesses,
                    "priority_fixes": [
                        f"Replace {c['hex']} with official Bosch color" 
                        for c in color_compliance['non_compliant_colors'][:3]
                    ] + [
                        f"Replace {f['name']} with Bosch font" 
                        for f in font_compliance['non_compliant_fonts'][:2]
                    ]
                }
            }
        }

# Test function
def test_compliance_analyzer():
    """Test the compliance analyzer with sample data"""
    analyzer = BrandComplianceAnalyzer()
    
    # Test color similarity
    similarity = analyzer.color_similarity("#007bc0", "#0088cc")  # Similar blue
    print(f"Color similarity between Bosch Blue and similar blue: {similarity:.3f}")
    
    # Test color matching
    match = analyzer.find_best_color_match("#0088cc")
    print(f"Best match for #0088cc: {match}")
    
    # Test with sample analysis data
    sample_data = [{
        "filename": "test_document.pdf",
        "total_pages": 1,
        "colors": [
            {"hex": "#007bc0", "name": "Blue", "usage_percentage": 45.2},
            {"hex": "#ff0000", "name": "Red", "usage_percentage": 12.5},
            {"hex": "#0088cc", "name": "Light Blue", "usage_percentage": 8.3}
        ],
        "fonts": [
            {"name": "BoschSans-Regular", "usage_percentage": 60.5},
            {"name": "Arial", "usage_percentage": 39.5}
        ]
    }]
    
    result = analyzer.analyze_compliance(sample_data)
    print("\nCompliance Analysis Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_compliance_analyzer()
