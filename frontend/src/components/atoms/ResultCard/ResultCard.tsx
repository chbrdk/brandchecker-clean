import React from 'react';
import { Typography } from '../Typography';
import { Score } from '../Score';
import { TrafficLight } from '../TrafficLight';
import { ProgressBar } from '../ProgressBar';
import { Chart } from '../Chart';
import { RecommendationList } from '../RecommendationList';
import { Icon } from '../Icon';
import { Badge } from '../Badge';
import { Chip } from '../Chip';
import type { IconName } from '../Icon';
import type { ChartDataPoint } from '../Chart';
import type { RecommendationItem } from '../RecommendationList';
import './ResultCard.css';

/**
 * Result Card Type
 */
export type ResultCardType = 'score' | 'analysis' | 'comparison' | 'trend' | 'recommendations' | 'summary';

/**
 * Result Card Variant
 */
export type ResultCardVariant = 'default' | 'compact' | 'detailed' | 'interactive' | 'full-width';

/**
 * Analysis Result Data
 */
export interface AnalysisResult {
  category: string;
  score: number;
  status: 'success' | 'warning' | 'error';
  details?: string;
  recommendations?: string[];
}

/**
 * Result Card Props
 */
export interface ResultCardProps {
  /** Card type */
  type: ResultCardType;
  /** Card variant */
  variant?: ResultCardVariant;
  /** Card title */
  title: string;
  /** Card description */
  description?: string;
  /** Main score value */
  score?: number;
  /** Maximum score */
  maxScore?: number;
  /** Overall status */
  status?: 'success' | 'warning' | 'error';
  /** Analysis results */
  analysisResults?: AnalysisResult[];
  /** Chart data */
  chartData?: ChartDataPoint[];
  /** Recommendations */
  recommendations?: RecommendationItem[];
  /** Icon name */
  iconName?: IconName;
  /** Category */
  category?: string;
  /** Tags */
  tags?: string[];
  /** Timestamp */
  timestamp?: Date;
  /** Size */
  size?: 'sm' | 'md' | 'lg';
  /** Show score */
  showScore?: boolean;
  /** Show status */
  showStatus?: boolean;
  /** Show chart */
  showChart?: boolean;
  /** Show recommendations */
  showRecommendations?: boolean;
  /** Show details */
  showDetails?: boolean;
  /** Additional CSS class */
  className?: string;
  /** Click handler */
  onClick?: () => void;
  /** Expand handler */
  onExpand?: () => void;
}

/**
 * Result Card Component
 * 
 * Displays BrandChecker analysis results in various card formats.
 * Combines multiple atomic components for comprehensive result visualization.
 * 
 * Features:
 * - Multiple result types (score, analysis, comparison, trend, recommendations, summary)
 * - Different variants (default, compact, detailed, interactive)
 * - Integrated components (Score, TrafficLight, Chart, RecommendationList)
 * - Interactive features
 * - Responsive design
 * - Design token integration
 * 
 * @param props - ResultCardProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Score result card
 * <ResultCard 
 *   type="score" 
 *   title="Brand Consistency" 
 *   score={85} 
 *   status="success" 
 * />
 * 
 * // Analysis result card
 * <ResultCard 
 *   type="analysis" 
 *   title="Brand Analysis" 
 *   analysisResults={results} 
 *   showChart 
 *   showRecommendations 
 * />
 * ```
 */
export const ResultCard = ({
  type,
  variant = 'default',
  title,
  description,
  score,
  maxScore = 100,
  status,
  analysisResults = [],
  chartData = [],
  recommendations = [],
  iconName,
  category,
  tags = [],
  timestamp,
  size = 'md',
  showScore = true,
  showStatus = true,
  showChart = false,
  showRecommendations = false,
  showDetails = false,
  className = '',
  onClick,
  onExpand
}: ResultCardProps) => {
  const classes = [
    'result-card',
    `result-card--${type}`,
    `result-card--${variant}`,
    `result-card--${size}`,
    status && `result-card--${status}`,
    onClick && 'result-card--clickable',
    className
  ].filter(Boolean).join(' ');

  // Get status color
  const getStatusColor = (status: 'success' | 'warning' | 'error') => {
    switch (status) {
      case 'success': return 'success';
      case 'warning': return 'warning';
      case 'error': return 'error';
      default: return 'primary';
    }
  };

  // Format timestamp
  const formatTimestamp = (date: Date) => {
    return date.toLocaleDateString('de-DE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Render score section
  const renderScoreSection = () => {
    if (!showScore || score === undefined) return null;

    return (
      <div className="result-card__score">
        <Score
          value={score}
          max={maxScore}
          size={size === 'sm' ? 'sm' : size === 'lg' ? 'lg' : 'md'}
          showPercentage={true}
          iconName={iconName}
        />
      </div>
    );
  };

  // Render status section
  const renderStatusSection = () => {
    if (!showStatus || !status) return null;

    return (
      <div className="result-card__status">
        <TrafficLight
          status={status}
          size={size === 'sm' ? 'sm' : 'md'}
          showLabel={true}
        />
      </div>
    );
  };

  // Render analysis results
  const renderAnalysisResults = () => {
    if (analysisResults.length === 0) return null;

    return (
      <div className="result-card__analysis">
        {analysisResults.map((result, index) => (
          <div key={index} className="result-card__analysis-item">
            <div className="result-card__analysis-header">
              <Typography variant="h4" size="sm" weight="medium" color="primary">
                {result.category}
              </Typography>
              <div className="result-card__analysis-indicators">
                <Score
                  value={result.score}
                  size="sm"
                  showPercentage={true}
                />
                <TrafficLight
                  status={result.status}
                  size="sm"
                  showLabel={false}
                />
              </div>
            </div>
            {result.details && (
              <Typography variant="body" size="xs" color="secondary">
                {result.details}
              </Typography>
            )}
          </div>
        ))}
      </div>
    );
  };

  // Render chart section
  const renderChartSection = () => {
    if (!showChart || chartData.length === 0) return null;

    const chartType = type === 'trend' ? 'line' : type === 'comparison' ? 'bar' : 'pie';

    return (
      <div className="result-card__chart">
        <Chart
          type={chartType}
          data={chartData}
          size={size === 'sm' ? 'sm' : 'md'}
          showLegend={true}
          showValues={true}
        />
      </div>
    );
  };

  // Render recommendations section
  const renderRecommendationsSection = () => {
    if (!showRecommendations || recommendations.length === 0) return null;

    return (
      <div className="result-card__recommendations">
        <RecommendationList
          recommendations={recommendations}
          size={size === 'sm' ? 'sm' : 'md'}
          showPriority={true}
          showStatus={true}
          showTags={true}
          maxItems={3}
        />
      </div>
    );
  };

  // Render details section
  const renderDetailsSection = () => {
    if (!showDetails) return null;

    return (
      <div className="result-card__details">
        {category && (
          <Chip variant="outlined" size="sm" color="secondary">
            {category}
          </Chip>
        )}
        {tags.length > 0 && (
          <div className="result-card__tags">
            {tags.slice(0, 3).map((tag, index) => (
              <Chip key={index} variant="filled" size="sm" color="neutral">
                {tag}
              </Chip>
            ))}
            {tags.length > 3 && (
              <Typography variant="caption" size="xs" color="tertiary">
                +{tags.length - 3} more
              </Typography>
            )}
          </div>
        )}
        {timestamp && (
          <Typography variant="caption" size="xs" color="tertiary">
            {formatTimestamp(timestamp)}
          </Typography>
        )}
      </div>
    );
  };

  return (
    <div
      className={classes}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
    >
      <div className="result-card__header">
        <div className="result-card__title-section">
          {iconName && (
            <div className="result-card__icon">
              <Icon name={iconName} size={size === 'sm' ? 'sm' : 'md'} />
            </div>
          )}
          <div className="result-card__title">
            <Typography 
              variant="h3" 
              size={size === 'sm' ? 'sm' : size === 'lg' ? 'lg' : 'md'} 
              weight="semibold" 
              color="primary"
            >
              {title}
            </Typography>
            {description && (
              <Typography variant="body" size="sm" color="secondary">
                {description}
              </Typography>
            )}
          </div>
        </div>
        
        <div className="result-card__actions">
          {status && showStatus && (
            <Badge type={getStatusColor(status)} size={size === 'sm' ? 'sm' : 'md'}>
              {status}
            </Badge>
          )}
          {onExpand && (
            <button
              className="result-card__expand"
              onClick={(e) => {
                e.stopPropagation();
                onExpand();
              }}
              aria-label="Expand details"
            >
              <Icon name="chevron-down" size="sm" />
            </button>
          )}
        </div>
      </div>

      <div className="result-card__content">
        {variant === 'full-width' ? (
          <>
            {/* Score Column */}
            <div className="result-card__score-column">
              {renderScoreSection()}
              {renderStatusSection()}
            </div>
            
            {/* Analysis Column */}
            <div className="result-card__analysis-column">
              {renderAnalysisResults()}
            </div>
            
            {/* Recommendations Column */}
            <div className="result-card__recommendations-column">
              {renderRecommendationsSection()}
            </div>
            
            {/* Full Width Chart */}
            {renderChartSection()}
            
            {/* Details Section */}
            {renderDetailsSection()}
          </>
        ) : (
          <>
            {renderScoreSection()}
            {renderStatusSection()}
            {renderAnalysisResults()}
            {renderChartSection()}
            {renderRecommendationsSection()}
            {renderDetailsSection()}
          </>
        )}
      </div>
    </div>
  );
};

ResultCard.displayName = 'ResultCard';
