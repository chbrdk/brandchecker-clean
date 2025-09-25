import React from 'react';
import { Typography } from '../Typography';
import { Icon } from '../Icon';
import { Chip } from '../Chip';
import { Badge } from '../Badge';
import type { IconName } from '../Icon';
import './RecommendationList.css';

/**
 * Recommendation Priority
 */
export type RecommendationPriority = 'low' | 'medium' | 'high' | 'critical';

/**
 * Recommendation Status
 */
export type RecommendationStatus = 'pending' | 'in-progress' | 'completed' | 'dismissed';

/**
 * Recommendation Item
 */
export interface RecommendationItem {
  id: string;
  title: string;
  description: string;
  priority: RecommendationPriority;
  status?: RecommendationStatus;
  category?: string;
  tags?: string[];
  iconName?: IconName;
  estimatedTime?: string;
  impact?: 'low' | 'medium' | 'high';
  createdAt?: Date;
  completedAt?: Date;
}

/**
 * Recommendation List Props
 */
export interface RecommendationListProps {
  /** List title */
  title?: string;
  /** List description */
  description?: string;
  /** Recommendations data */
  recommendations: RecommendationItem[];
  /** Show priority indicators */
  showPriority?: boolean;
  /** Show status indicators */
  showStatus?: boolean;
  /** Show category */
  showCategory?: boolean;
  /** Show tags */
  showTags?: boolean;
  /** Show estimated time */
  showEstimatedTime?: boolean;
  /** Show impact level */
  showImpact?: boolean;
  /** Show timestamps */
  showTimestamps?: boolean;
  /** Size */
  size?: 'sm' | 'md' | 'lg';
  /** Maximum items to show */
  maxItems?: number;
  /** Show "Show more" button */
  showMoreButton?: boolean;
  /** Additional CSS class */
  className?: string;
  /** Click handler for recommendations */
  onRecommendationClick?: (recommendation: RecommendationItem) => void;
  /** Status change handler */
  onStatusChange?: (recommendationId: string, newStatus: RecommendationStatus) => void;
  /** Dismiss handler */
  onDismiss?: (recommendationId: string) => void;
}

/**
 * Recommendation List Component
 * 
 * Displays a list of recommendations with priority, status, and metadata.
 * Supports different display options and interactive features.
 * 
 * Features:
 * - Priority-based color coding
 * - Status indicators and management
 * - Category and tag display
 * - Estimated time and impact level
 * - Interactive actions (click, status change, dismiss)
 * - Responsive design
 * - Design token integration
 * 
 * @param props - RecommendationListProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Basic recommendation list
 * <RecommendationList 
 *   title="Brand Improvements" 
 *   recommendations={brandRecommendations} 
 * />
 * 
 * // With all features
 * <RecommendationList 
 *   title="Action Items" 
 *   recommendations={recommendations}
 *   showPriority 
 *   showStatus 
 *   showTags 
 *   showEstimatedTime 
 *   onRecommendationClick={handleClick}
 * />
 * ```
 */
export const RecommendationList = ({
  title,
  description,
  recommendations,
  showPriority = true,
  showStatus = true,
  showCategory = false,
  showTags = true,
  showEstimatedTime = false,
  showImpact = false,
  showTimestamps = false,
  size = 'md',
  maxItems,
  showMoreButton = false,
  className = '',
  onRecommendationClick,
  onStatusChange,
  onDismiss
}: RecommendationListProps) => {
  const classes = [
    'recommendation-list',
    `recommendation-list--${size}`,
    className
  ].filter(Boolean).join(' ');

  // Filter and limit recommendations
  const displayedRecommendations = maxItems 
    ? recommendations.slice(0, maxItems)
    : recommendations;

  // Get priority color
  const getPriorityColor = (priority: RecommendationPriority) => {
    switch (priority) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'primary';
      case 'low': return 'success';
      default: return 'neutral';
    }
  };

  // Get status color
  const getStatusColor = (status: RecommendationStatus) => {
    switch (status) {
      case 'completed': return 'success';
      case 'in-progress': return 'warning';
      case 'pending': return 'primary';
      case 'dismissed': return 'neutral';
      default: return 'neutral';
    }
  };

  // Get impact color
  const getImpactColor = (impact: 'low' | 'medium' | 'high') => {
    switch (impact) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'neutral';
    }
  };

  // Format timestamp
  const formatTimestamp = (date: Date) => {
    return date.toLocaleDateString('de-DE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  // Render recommendation item
  const renderRecommendationItem = (recommendation: RecommendationItem, index: number) => {
    const itemClasses = [
      'recommendation-item',
      `recommendation-item--${recommendation.priority}`,
      `recommendation-item--${size}`,
      onRecommendationClick && 'recommendation-item--clickable'
    ].filter(Boolean).join(' ');

    return (
      <div
        key={recommendation.id}
        className={itemClasses}
        onClick={() => onRecommendationClick?.(recommendation)}
        role={onRecommendationClick ? 'button' : undefined}
        tabIndex={onRecommendationClick ? 0 : undefined}
      >
        <div className="recommendation-item__header">
          <div className="recommendation-item__title-section">
            {recommendation.iconName && (
              <div className="recommendation-item__icon">
                <Icon name={recommendation.iconName} size={size === 'sm' ? 'xs' : 'sm'} />
              </div>
            )}
            <div className="recommendation-item__title">
              <Typography 
                variant="h4" 
                size={size === 'sm' ? 'xs' : 'sm'} 
                weight="semibold" 
                color="primary"
              >
                {recommendation.title}
              </Typography>
            </div>
          </div>
          
          <div className="recommendation-item__indicators">
            {showPriority && (
              <Badge 
                type={getPriorityColor(recommendation.priority)}
                size={size === 'sm' ? 'xs' : 'sm'}
              >
                {recommendation.priority}
              </Badge>
            )}
            
            {showStatus && recommendation.status && (
              <Badge 
                type={getStatusColor(recommendation.status)}
                size={size === 'sm' ? 'xs' : 'sm'}
              >
                {recommendation.status}
              </Badge>
            )}
            
            {showImpact && recommendation.impact && (
              <Badge 
                type={getImpactColor(recommendation.impact)}
                size={size === 'sm' ? 'xs' : 'sm'}
              >
                {recommendation.impact} impact
              </Badge>
            )}
          </div>
        </div>

        <div className="recommendation-item__content">
          <Typography 
            variant="body" 
            size={size === 'sm' ? 'xs' : 'sm'} 
            color="secondary"
          >
            {recommendation.description}
          </Typography>
        </div>

        <div className="recommendation-item__footer">
          <div className="recommendation-item__metadata">
            {showCategory && recommendation.category && (
              <Chip 
                variant="outlined" 
                size={size === 'sm' ? 'xs' : 'sm'}
                color="secondary"
              >
                {recommendation.category}
              </Chip>
            )}
            
            {showTags && recommendation.tags && recommendation.tags.length > 0 && (
              <div className="recommendation-item__tags">
                {recommendation.tags.slice(0, 3).map((tag, tagIndex) => (
                  <Chip 
                    key={tagIndex}
                    variant="filled" 
                    size={size === 'sm' ? 'xs' : 'sm'}
                    color="neutral"
                  >
                    {tag}
                  </Chip>
                ))}
                {recommendation.tags.length > 3 && (
                  <Typography variant="caption" size="xs" color="tertiary">
                    +{recommendation.tags.length - 3} more
                  </Typography>
                )}
              </div>
            )}
            
            {showEstimatedTime && recommendation.estimatedTime && (
              <Typography variant="caption" size="xs" color="tertiary">
                ⏱️ {recommendation.estimatedTime}
              </Typography>
            )}
          </div>
          
          <div className="recommendation-item__actions">
            {showTimestamps && recommendation.createdAt && (
              <Typography variant="caption" size="xs" color="tertiary">
                Created: {formatTimestamp(recommendation.createdAt)}
              </Typography>
            )}
            
            {showTimestamps && recommendation.completedAt && (
              <Typography variant="caption" size="xs" color="tertiary">
                Completed: {formatTimestamp(recommendation.completedAt)}
              </Typography>
            )}
            
            {onDismiss && (
              <button
                className="recommendation-item__dismiss"
                onClick={(e) => {
                  e.stopPropagation();
                  onDismiss(recommendation.id);
                }}
                aria-label={`Dismiss ${recommendation.title}`}
              >
                <Icon name="x" size="xs" />
              </button>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className={classes}>
      {(title || description) && (
        <div className="recommendation-list__header">
          {title && (
            <Typography variant="h3" size={size === 'sm' ? 'sm' : 'md'} weight="semibold" color="primary">
              {title}
            </Typography>
          )}
          {description && (
            <Typography variant="body" size="sm" color="secondary">
              {description}
            </Typography>
          )}
        </div>
      )}
      
      <div className="recommendation-list__content">
        {displayedRecommendations.length === 0 ? (
          <div className="recommendation-list__empty">
            <Typography variant="body" color="tertiary">
              No recommendations available
            </Typography>
          </div>
        ) : (
          displayedRecommendations.map(renderRecommendationItem)
        )}
      </div>
      
      {showMoreButton && maxItems && recommendations.length > maxItems && (
        <div className="recommendation-list__footer">
          <Typography variant="body" size="sm" color="secondary">
            Showing {maxItems} of {recommendations.length} recommendations
          </Typography>
        </div>
      )}
    </div>
  );
};

RecommendationList.displayName = 'RecommendationList';
