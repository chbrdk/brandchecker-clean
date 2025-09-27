import React from 'react';
import { Typography } from '../../atoms/Typography';
import { Score } from '../../atoms/Score';
import { TrafficLight } from '../../atoms/TrafficLight';
import { Chip } from '../../atoms/Chip';
import './VisionResults.css';

export interface VisionAnalysis {
  content_analysis: {
    main_subject: string;
    composition: string;
    dominant_elements: string[];
  };
  contrast_analysis: {
    contrast_level: 'high' | 'medium' | 'low';
    brightness: 'bright' | 'balanced' | 'dark';
    exposure_issues: string[];
  };
  color_analysis: {
    dominant_colors: string[];
    color_temperature: 'warm' | 'cool' | 'neutral';
    accent_colors: string[];
    color_harmony: 'good' | 'moderate' | 'poor';
  };
  depth_analysis: {
    depth_of_field: 'shallow' | 'medium' | 'deep';
    sharpness: 'sharp' | 'moderate' | 'soft';
    bokeh_effects: boolean;
  };
  perspective_analysis: {
    camera_angle: string;
    viewpoint: string;
    spatial_depth: 'good' | 'moderate' | 'poor';
  };
  people_analysis: {
    people_present: boolean;
    emotions: string[];
    body_language: string;
  };
  mood_analysis: {
    overall_mood: string;
    brand_values: string[];
    professional_impression: 'high' | 'medium' | 'low';
  };
  technical_quality: {
    image_quality: 'excellent' | 'good' | 'moderate' | 'poor';
    technical_issues: string[];
    professional_suitability: 'high' | 'medium' | 'low';
  };
  recommendations: {
    strengths: string[];
    improvements: string[];
    brand_alignment: string;
  };
}

export interface VisionResultsProps {
  visionData: {
    success: boolean;
    total_images: number;
    image_analyses: Array<{
      success: boolean;
      analysis: VisionAnalysis | { raw_analysis: string };
      metadata: {
        page_number: number;
        image_index: number;
        image_size: [number, number];
        image_format: string;
      };
    }>;
    summary: {
      successful_analyses: number;
      failed_analyses: number;
    };
  };
  className?: string;
}

export const VisionResults = ({ visionData, className = '' }: VisionResultsProps) => {
  if (!visionData.success || !visionData.image_analyses.length) {
    return (
      <div className={`vision-results vision-results--error ${className}`}>
        <Typography variant="body" size="sm" color="error">
          Keine Vision-Analyse verfügbar
        </Typography>
      </div>
    );
  }

  // Parse raw analysis if needed
  const parseAnalysis = (analysis: VisionAnalysis | { raw_analysis: string }): VisionAnalysis | null => {
    if ('raw_analysis' in analysis) {
      try {
        // Extract JSON from markdown code block
        const jsonMatch = analysis.raw_analysis.match(/```json\n([\s\S]*?)\n```/);
        if (jsonMatch) {
          return JSON.parse(jsonMatch[1]);
        }
        // Try direct JSON parsing
        return JSON.parse(analysis.raw_analysis);
      } catch (error) {
        console.error('Error parsing vision analysis:', error);
        return null;
      }
    }
    return analysis;
  };

  const getQualityScore = (quality: string) => {
    switch (quality) {
      case 'excellent': return 95;
      case 'good': return 80;
      case 'moderate': return 60;
      case 'poor': return 30;
      default: return 50;
    }
  };

  const getQualityColor = (quality: string) => {
    switch (quality) {
      case 'excellent': return 'success';
      case 'good': return 'success';
      case 'moderate': return 'warning';
      case 'poor': return 'error';
      default: return 'info';
    }
  };

  const getContrastColor = (level: string) => {
    switch (level) {
      case 'high': return 'success';
      case 'medium': return 'warning';
      case 'low': return 'error';
      default: return 'info';
    }
  };

  return (
    <div className={`vision-results ${className}`}>
      <div className="vision-results__header">
        <Typography variant="h3" size="md" weight="semibold">
          🔍 GPT Vision Analyse
        </Typography>
        <Typography variant="body" size="xs" color="secondary">
          {visionData.total_images} Bilder analysiert • {visionData.summary.successful_analyses} erfolgreich
        </Typography>
      </div>

      {visionData.image_analyses.map((imageAnalysis, index) => {
        if (!imageAnalysis.success || !imageAnalysis.analysis) {
          return (
            <div key={index} className="vision-results__image vision-results__image--error">
              <Typography variant="body" size="sm" color="error">
                Bild {imageAnalysis.metadata?.image_index || index + 1} konnte nicht analysiert werden
              </Typography>
            </div>
          );
        }

        const parsedAnalysis = parseAnalysis(imageAnalysis.analysis);
        if (!parsedAnalysis) {
          return (
            <div key={index} className="vision-results__image vision-results__image--error">
              <Typography variant="body" size="sm" color="error">
                Bild {imageAnalysis.metadata?.image_index || index + 1} - Analyse konnte nicht geparst werden
              </Typography>
            </div>
          );
        }

        const analysis = parsedAnalysis;
        const metadata = imageAnalysis.metadata;

        return (
          <div key={index} className="vision-results__image">
            <div className="vision-results__image-header">
              <Typography variant="h4" size="sm" weight="semibold">
                Bild {metadata.image_index} (Seite {metadata.page_number})
              </Typography>
              <Typography variant="caption" size="xs" color="secondary">
                {metadata.image_size[0]} × {metadata.image_size[1]} • {metadata.image_format}
              </Typography>
            </div>

            <div className="vision-results__grid">
              {/* Content Analysis */}
              <div className="vision-results__section">
                <Typography variant="h5" size="xs" weight="semibold" color="primary">
                  📋 Inhalt & Komposition
                </Typography>
                <div className="vision-results__content">
                  <Typography variant="body" size="xs" weight="medium">
                    {analysis.content_analysis.main_subject}
                  </Typography>
                  <Typography variant="body" size="xs" color="secondary">
                    {analysis.content_analysis.composition}
                  </Typography>
                  <div className="vision-results__chips">
                    {analysis.content_analysis.dominant_elements.map((element, i) => (
                      <Chip key={i} variant="secondary" size="sm">
                        {element}
                      </Chip>
                    ))}
                  </div>
                </div>
              </div>

              {/* Color Analysis */}
              <div className="vision-results__section">
                <Typography variant="h5" size="xs" weight="semibold" color="primary">
                  🎨 Farbgebung
                </Typography>
                <div className="vision-results__content">
                  <div className="vision-results__color-info">
                    <Typography variant="body" size="xs" weight="medium">
                      Temperatur: {analysis.color_analysis.color_temperature}
                    </Typography>
                    <Typography variant="body" size="xs" weight="medium">
                      Harmonie: {analysis.color_analysis.color_harmony}
                    </Typography>
                  </div>
                  <div className="vision-results__color-swatches">
                    {analysis.color_analysis.dominant_colors.slice(0, 5).map((color, i) => (
                      <div
                        key={i}
                        className="vision-results__color-swatch"
                        style={{ backgroundColor: color }}
                        title={color}
                      />
                    ))}
                  </div>
                  {analysis.color_analysis.accent_colors.length > 0 && (
                    <div className="vision-results__chips">
                      {analysis.color_analysis.accent_colors.map((color, i) => (
                        <Chip key={i} variant="accent" size="sm">
                          {color}
                        </Chip>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Technical Quality */}
              <div className="vision-results__section">
                <Typography variant="h5" size="xs" weight="semibold" color="primary">
                  ⚙️ Technische Qualität
                </Typography>
                <div className="vision-results__content">
                  <div className="vision-results__quality-score">
                    <Score
                      value={getQualityScore(analysis.technical_quality.image_quality)}
                      size="sm"
                      showPercentage={true}
                    />
                    <TrafficLight
                      status={getQualityColor(analysis.technical_quality.image_quality)}
                      size="sm"
                      showLabel={true}
                    />
                  </div>
                  <Typography variant="body" size="xs" color="secondary">
                    Eignung: {analysis.technical_quality.professional_suitability}
                  </Typography>
                  {analysis.technical_quality.technical_issues.length > 0 && (
                    <div className="vision-results__issues">
                      {analysis.technical_quality.technical_issues.map((issue, i) => (
                        <Chip key={i} variant="error" size="sm">
                          {issue}
                        </Chip>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Mood & Brand */}
              <div className="vision-results__section">
                <Typography variant="h5" size="xs" weight="semibold" color="primary">
                  💭 Stimmung & Marke
                </Typography>
                <div className="vision-results__content">
                  <Typography variant="body" size="xs" weight="medium">
                    {analysis.mood_analysis.overall_mood}
                  </Typography>
                  <div className="vision-results__chips">
                    {analysis.mood_analysis.brand_values.map((value, i) => (
                      <Chip key={i} variant="primary" size="sm">
                        {value}
                      </Chip>
                    ))}
                  </div>
                  <Typography variant="body" size="xs" color="secondary">
                    Professioneller Eindruck: {analysis.mood_analysis.professional_impression}
                  </Typography>
                </div>
              </div>

              {/* Contrast & Depth */}
              <div className="vision-results__section">
                <Typography variant="h5" size="xs" weight="semibold" color="primary">
                  📐 Kontrast & Tiefe
                </Typography>
                <div className="vision-results__content">
                  <div className="vision-results__metrics">
                    <div className="vision-results__metric">
                      <Typography variant="body" size="xs" weight="medium">
                        Kontrast: {analysis.contrast_analysis.contrast_level}
                      </Typography>
                      <TrafficLight
                        status={getContrastColor(analysis.contrast_analysis.contrast_level)}
                        size="sm"
                        showLabel={false}
                      />
                    </div>
                    <div className="vision-results__metric">
                      <Typography variant="body" size="xs" weight="medium">
                        Schärfe: {analysis.depth_analysis.sharpness}
                      </Typography>
                    </div>
                    <div className="vision-results__metric">
                      <Typography variant="body" size="xs" weight="medium">
                        Tiefe: {analysis.depth_analysis.depth_of_field}
                      </Typography>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recommendations */}
              <div className="vision-results__section vision-results__section--full">
                <Typography variant="h5" size="xs" weight="semibold" color="primary">
                  💡 Empfehlungen
                </Typography>
                <div className="vision-results__content">
                  <Typography variant="body" size="xs" weight="medium" color="primary">
                    {analysis.recommendations.brand_alignment}
                  </Typography>
                  
                  {analysis.recommendations.strengths.length > 0 && (
                    <div className="vision-results__recommendations">
                      <Typography variant="body" size="xs" weight="medium" color="success">
                        Stärken:
                      </Typography>
                      <div className="vision-results__chips">
                        {analysis.recommendations.strengths.map((strength, i) => (
                          <Chip key={i} variant="success" size="sm">
                            {strength}
                          </Chip>
                        ))}
                      </div>
                    </div>
                  )}

                  {analysis.recommendations.improvements.length > 0 && (
                    <div className="vision-results__recommendations">
                      <Typography variant="body" size="xs" weight="medium" color="warning">
                        Verbesserungen:
                      </Typography>
                      <div className="vision-results__chips">
                        {analysis.recommendations.improvements.map((improvement, i) => (
                          <Chip key={i} variant="warning" size="sm">
                            {improvement}
                          </Chip>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

VisionResults.displayName = 'VisionResults';
