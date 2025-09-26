import React from 'react';
import { Score } from '../../atoms/Score';
import { ProgressBar } from '../../atoms/ProgressBar';
import { Chip } from '../../atoms/Chip';
import { Typography } from '../../atoms/Typography';
import './AnalysisResults.css';

export interface AnalysisResultsProps {
  results: {
    brand_analysis: {
      overall_score: number;
      color_analysis: {
        primary_colors: string[];
        color_harmony: string;
        accessibility_score: number;
      };
      typography_analysis: {
        font_families: string[];
        readability_score: number;
        consistency_score: number;
      };
      layout_analysis: {
        structure_score: number;
        spacing_score: number;
        balance_score: number;
      };
      logo_analysis: {
        logo_detected: boolean;
        logo_quality: string;
        placement_score: number;
      };
    };
    recommendations: Array<{
      category: string;
      priority: string;
      title: string;
      description: string;
      impact: string;
    }>;
    extracted_elements: {
      text_blocks: number;
      images: number;
      logos: number;
      tables: number;
      charts: number;
    };
    processing_time: string;
    file_info: {
      filename: string;
      pages: number;
      file_size: string;
    };
  };
  className?: string;
}

export const AnalysisResults = ({ results, className = '' }: AnalysisResultsProps) => {
  const { brand_analysis, recommendations, extracted_elements, processing_time, file_info } = results;

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'error';
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'secondary';
    }
  };

  return (
    <div className={`analysis-results ${className}`}>
      {/* Header */}
      <div className="analysis-results__header">
        <Typography variant="h3" size="lg" weight="semibold">
          Analyseergebnisse
        </Typography>
        <div className="analysis-results__meta">
          <Typography variant="caption" size="xs" color="muted">
            {file_info.filename} • {file_info.pages} Seiten • {file_info.file_size}
          </Typography>
          <Typography variant="caption" size="xs" color="muted">
            Verarbeitungszeit: {processing_time}
          </Typography>
        </div>
      </div>

      {/* Overall Score */}
      <div className="analysis-results__overall">
        <Typography variant="h4" size="md" weight="semibold">
          Gesamtbewertung
        </Typography>
        <Score 
          score={brand_analysis.overall_score} 
          label="Brand Score"
          size="lg"
        />
      </div>

      {/* Detailed Analysis */}
      <div className="analysis-results__sections">
        {/* Color Analysis */}
        <div className="analysis-results__section">
          <Typography variant="h5" size="sm" weight="semibold">
            Farbanalyse
          </Typography>
          <div className="analysis-results__metrics">
            <div className="analysis-results__metric">
              <Typography variant="body" size="xs" color="secondary">
                Barrierefreiheit
              </Typography>
              <ProgressBar 
                value={brand_analysis.color_analysis.accessibility_score}
                size="sm"
                showPercentage={true}
                color={getScoreColor(brand_analysis.color_analysis.accessibility_score)}
              />
            </div>
            <div className="analysis-results__metric">
              <Typography variant="body" size="xs" color="secondary">
                Harmonie
              </Typography>
              <Chip variant="outlined" size="sm">
                {brand_analysis.color_analysis.color_harmony}
              </Chip>
            </div>
            <div className="analysis-results__colors">
              <Typography variant="body" size="xs" color="secondary">
                Primärfarben:
              </Typography>
              <div className="analysis-results__color-palette">
                {brand_analysis.color_analysis.primary_colors.map((color, index) => (
                  <div 
                    key={index}
                    className="analysis-results__color-swatch"
                    style={{ backgroundColor: color }}
                    title={color}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Typography Analysis */}
        <div className="analysis-results__section">
          <Typography variant="h5" size="sm" weight="semibold">
            Typografie
          </Typography>
          <div className="analysis-results__metrics">
            <div className="analysis-results__metric">
              <Typography variant="body" size="xs" color="secondary">
                Lesbarkeit
              </Typography>
              <ProgressBar 
                value={brand_analysis.typography_analysis.readability_score}
                size="sm"
                showPercentage={true}
                color={getScoreColor(brand_analysis.typography_analysis.readability_score)}
              />
            </div>
            <div className="analysis-results__metric">
              <Typography variant="body" size="xs" color="secondary">
                Konsistenz
              </Typography>
              <ProgressBar 
                value={brand_analysis.typography_analysis.consistency_score}
                size="sm"
                showPercentage={true}
                color={getScoreColor(brand_analysis.typography_analysis.consistency_score)}
              />
            </div>
            <div className="analysis-results__fonts">
              <Typography variant="body" size="xs" color="secondary">
                Schriftarten:
              </Typography>
              <div className="analysis-results__font-list">
                {brand_analysis.typography_analysis.font_families.map((font, index) => (
                  <Chip key={index} variant="outlined" size="sm">
                    {font}
                  </Chip>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Layout Analysis */}
        <div className="analysis-results__section">
          <Typography variant="h5" size="sm" weight="semibold">
            Layout
          </Typography>
          <div className="analysis-results__metrics">
            <div className="analysis-results__metric">
              <Typography variant="body" size="xs" color="secondary">
                Struktur
              </Typography>
              <ProgressBar 
                value={brand_analysis.layout_analysis.structure_score}
                size="sm"
                showPercentage={true}
                color={getScoreColor(brand_analysis.layout_analysis.structure_score)}
              />
            </div>
            <div className="analysis-results__metric">
              <Typography variant="body" size="xs" color="secondary">
                Abstände
              </Typography>
              <ProgressBar 
                value={brand_analysis.layout_analysis.spacing_score}
                size="sm"
                showPercentage={true}
                color={getScoreColor(brand_analysis.layout_analysis.spacing_score)}
              />
            </div>
            <div className="analysis-results__metric">
              <Typography variant="body" size="xs" color="secondary">
                Balance
              </Typography>
              <ProgressBar 
                value={brand_analysis.layout_analysis.balance_score}
                size="sm"
                showPercentage={true}
                color={getScoreColor(brand_analysis.layout_analysis.balance_score)}
              />
            </div>
          </div>
        </div>

        {/* Logo Analysis */}
        <div className="analysis-results__section">
          <Typography variant="h5" size="sm" weight="semibold">
            Logo-Analyse
          </Typography>
          <div className="analysis-results__metrics">
            <div className="analysis-results__metric">
              <Typography variant="body" size="xs" color="secondary">
                Logo erkannt
              </Typography>
              <Chip 
                variant={brand_analysis.logo_analysis.logo_detected ? "success" : "error"} 
                size="sm"
              >
                {brand_analysis.logo_analysis.logo_detected ? "Ja" : "Nein"}
              </Chip>
            </div>
            <div className="analysis-results__metric">
              <Typography variant="body" size="xs" color="secondary">
                Qualität
              </Typography>
              <Chip variant="outlined" size="sm">
                {brand_analysis.logo_analysis.logo_quality}
              </Chip>
            </div>
            <div className="analysis-results__metric">
              <Typography variant="body" size="xs" color="secondary">
                Platzierung
              </Typography>
              <ProgressBar 
                value={brand_analysis.logo_analysis.placement_score}
                size="sm"
                showPercentage={true}
                color={getScoreColor(brand_analysis.logo_analysis.placement_score)}
              />
            </div>
          </div>
        </div>

        {/* Extracted Elements */}
        <div className="analysis-results__section">
          <Typography variant="h5" size="sm" weight="semibold">
            Extrahierte Elemente
          </Typography>
          <div className="analysis-results__elements">
            <div className="analysis-results__element">
              <Typography variant="body" size="xs" color="secondary">
                Textblöcke
              </Typography>
              <Chip variant="outlined" size="sm">
                {extracted_elements.text_blocks}
              </Chip>
            </div>
            <div className="analysis-results__element">
              <Typography variant="body" size="xs" color="secondary">
                Bilder
              </Typography>
              <Chip variant="outlined" size="sm">
                {extracted_elements.images}
              </Chip>
            </div>
            <div className="analysis-results__element">
              <Typography variant="body" size="xs" color="secondary">
                Logos
              </Typography>
              <Chip variant="outlined" size="sm">
                {extracted_elements.logos}
              </Chip>
            </div>
            <div className="analysis-results__element">
              <Typography variant="body" size="xs" color="secondary">
                Tabellen
              </Typography>
              <Chip variant="outlined" size="sm">
                {extracted_elements.tables}
              </Chip>
            </div>
            <div className="analysis-results__element">
              <Typography variant="body" size="xs" color="secondary">
                Diagramme
              </Typography>
              <Chip variant="outlined" size="sm">
                {extracted_elements.charts}
              </Chip>
            </div>
          </div>
        </div>

        {/* Recommendations */}
        <div className="analysis-results__section">
          <Typography variant="h5" size="sm" weight="semibold">
            Empfehlungen
          </Typography>
          <div className="analysis-results__recommendations">
            {recommendations.map((rec, index) => (
              <div key={index} className="analysis-results__recommendation">
                <div className="analysis-results__recommendation-header">
                  <Typography variant="body" size="sm" weight="semibold">
                    {rec.title}
                  </Typography>
                  <Chip 
                    variant={getPriorityColor(rec.priority)} 
                    size="sm"
                  >
                    {rec.priority}
                  </Chip>
                </div>
                <Typography variant="body" size="xs" color="secondary">
                  {rec.description}
                </Typography>
                <div className="analysis-results__recommendation-meta">
                  <Chip variant="outlined" size="sm">
                    {rec.category}
                  </Chip>
                  <Chip variant="outlined" size="sm">
                    {rec.impact} Impact
                  </Chip>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
