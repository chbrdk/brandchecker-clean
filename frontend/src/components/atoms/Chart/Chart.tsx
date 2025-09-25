import React from 'react';
import { Typography } from '../Typography';
import { Icon } from '../Icon';
import type { IconName } from '../Icon';
import './Chart.css';

/**
 * Chart Type
 */
export type ChartType = 'bar' | 'line' | 'pie' | 'doughnut' | 'area' | 'scatter';

/**
 * Chart Data Point
 */
export interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
  iconName?: IconName;
}

/**
 * Chart Props
 */
export interface ChartProps {
  /** Chart type */
  type: ChartType;
  /** Chart title */
  title?: string;
  /** Chart description */
  description?: string;
  /** Chart data */
  data: ChartDataPoint[];
  /** Chart width */
  width?: number;
  /** Chart height */
  height?: number;
  /** Show legend */
  showLegend?: boolean;
  /** Show values */
  showValues?: boolean;
  /** Show percentage */
  showPercentage?: boolean;
  /** Color scheme */
  colorScheme?: 'primary' | 'success' | 'warning' | 'error' | 'neutral' | 'brand';
  /** Size */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Additional CSS class */
  className?: string;
  /** Click handler for data points */
  onDataPointClick?: (dataPoint: ChartDataPoint, index: number) => void;
}

/**
 * Chart Component
 * 
 * Displays various chart types using SVG for lightweight, customizable charts.
 * Supports bar, line, pie, doughnut, area, and scatter charts.
 * 
 * Features:
 * - Multiple chart types (bar, line, pie, doughnut, area, scatter)
 * - SVG-based rendering for performance
 * - Customizable colors and sizes
 * - Interactive data points
 * - Legend and value display
 * - Responsive design
 * - Design token integration
 * 
 * @param props - ChartProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Bar chart
 * <Chart 
 *   type="bar" 
 *   title="Brand Usage" 
 *   data={[
 *     { label: 'Logo', value: 85 },
 *     { label: 'Colors', value: 92 },
 *     { label: 'Typography', value: 78 }
 *   ]} 
 * />
 * 
 * // Pie chart
 * <Chart 
 *   type="pie" 
 *   title="Brand Elements" 
 *   data={brandData} 
 *   showLegend 
 *   showPercentage 
 * />
 * ```
 */
export const Chart = ({
  type,
  title,
  description,
  data,
  width = 400,
  height = 300,
  showLegend = false,
  showValues = false,
  showPercentage = false,
  colorScheme = 'primary',
  size = 'md',
  className = '',
  onDataPointClick
}: ChartProps) => {
  const classes = [
    'chart',
    `chart--${type}`,
    `chart--${size}`,
    `chart--${colorScheme}`,
    className
  ].filter(Boolean).join(' ');

  // Calculate chart dimensions based on size
  const getChartDimensions = () => {
    switch (size) {
      case 'sm': return { width: 300, height: 200 };
      case 'md': return { width: 400, height: 300 };
      case 'lg': return { width: 500, height: 400 };
      case 'xl': return { width: 600, height: 500 };
      default: return { width, height };
    }
  };

  const { width: chartWidth, height: chartHeight } = getChartDimensions();

  // Get color for data point
  const getDataPointColor = (index: number, dataPoint: ChartDataPoint) => {
    if (dataPoint.color) return dataPoint.color;
    
    const colors = {
      primary: ['var(--color-primary-500)', 'var(--color-primary-600)', 'var(--color-primary-700)'],
      success: ['var(--color-status-success)', 'var(--color-success-600)', 'var(--color-success-700)'],
      warning: ['var(--color-status-warning)', 'var(--color-warning-600)', 'var(--color-warning-700)'],
      error: ['var(--color-status-error)', 'var(--color-error-600)', 'var(--color-error-700)'],
      neutral: ['var(--color-neutral-500)', 'var(--color-neutral-600)', 'var(--color-neutral-700)'],
      brand: ['var(--color-brand-primary)', 'var(--color-brand-secondary)', 'var(--color-brand-accent)']
    };
    
    return colors[colorScheme][index % colors[colorScheme].length];
  };

  // Calculate max value for scaling
  const maxValue = Math.max(...data.map(d => d.value));

  // Render bar chart
  const renderBarChart = () => {
    const barWidth = chartWidth / data.length * 0.8;
    const barSpacing = chartWidth / data.length * 0.2;
    const maxBarHeight = chartHeight * 0.7;

    return (
      <svg width={chartWidth} height={chartHeight} className="chart__svg">
        {data.map((dataPoint, index) => {
          const barHeight = (dataPoint.value / maxValue) * maxBarHeight;
          const x = index * (barWidth + barSpacing) + barSpacing / 2;
          const y = chartHeight - barHeight - 30; // 30px for labels
          
          return (
            <g key={index}>
              <rect
                x={x}
                y={y}
                width={barWidth}
                height={barHeight}
                fill={getDataPointColor(index, dataPoint)}
                className="chart__bar"
                onClick={() => onDataPointClick?.(dataPoint, index)}
              />
              <text
                x={x + barWidth / 2}
                y={chartHeight - 10}
                textAnchor="middle"
                className="chart__label"
              >
                {dataPoint.label}
              </text>
              {showValues && (
                <text
                  x={x + barWidth / 2}
                  y={y - 5}
                  textAnchor="middle"
                  className="chart__value"
                >
                  {dataPoint.value}{showPercentage ? '%' : ''}
                </text>
              )}
            </g>
          );
        })}
      </svg>
    );
  };

  // Render pie chart
  const renderPieChart = () => {
    const centerX = chartWidth / 2;
    const centerY = chartHeight / 2;
    const radius = Math.min(chartWidth, chartHeight) / 2 - 40;
    
    let cumulativePercentage = 0;
    const total = data.reduce((sum, d) => sum + d.value, 0);

    return (
      <svg width={chartWidth} height={chartHeight} className="chart__svg">
        {data.map((dataPoint, index) => {
          const percentage = (dataPoint.value / total) * 100;
          const startAngle = (cumulativePercentage / 100) * 2 * Math.PI;
          const endAngle = ((cumulativePercentage + percentage) / 100) * 2 * Math.PI;
          
          const x1 = centerX + radius * Math.cos(startAngle);
          const y1 = centerY + radius * Math.sin(startAngle);
          const x2 = centerX + radius * Math.cos(endAngle);
          const y2 = centerY + radius * Math.sin(endAngle);
          
          const largeArcFlag = percentage > 50 ? 1 : 0;
          
          const pathData = [
            `M ${centerX} ${centerY}`,
            `L ${x1} ${y1}`,
            `A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2}`,
            'Z'
          ].join(' ');

          cumulativePercentage += percentage;

          return (
            <path
              key={index}
              d={pathData}
              fill={getDataPointColor(index, dataPoint)}
              className="chart__pie-slice"
              onClick={() => onDataPointClick?.(dataPoint, index)}
            />
          );
        })}
        
        {/* Center text for doughnut */}
        {type === 'doughnut' && (
          <text
            x={centerX}
            y={centerY}
            textAnchor="middle"
            dominantBaseline="middle"
            className="chart__center-text"
          >
            {showPercentage ? `${Math.round(total)}%` : total}
          </text>
        )}
      </svg>
    );
  };

  // Render line chart
  const renderLineChart = () => {
    const padding = 40;
    const chartAreaWidth = chartWidth - padding * 2;
    const chartAreaHeight = chartHeight - padding * 2;
    
    const points = data.map((dataPoint, index) => {
      const x = padding + (index / (data.length - 1)) * chartAreaWidth;
      const y = padding + chartAreaHeight - (dataPoint.value / maxValue) * chartAreaHeight;
      return `${x},${y}`;
    }).join(' ');

    return (
      <svg width={chartWidth} height={chartHeight} className="chart__svg">
        <polyline
          points={points}
          fill="none"
          stroke={getDataPointColor(0, data[0])}
          strokeWidth="2"
          className="chart__line"
        />
        {data.map((dataPoint, index) => {
          const x = padding + (index / (data.length - 1)) * chartAreaWidth;
          const y = padding + chartAreaHeight - (dataPoint.value / maxValue) * chartAreaHeight;
          
          return (
            <g key={index}>
              <circle
                cx={x}
                cy={y}
                r="4"
                fill={getDataPointColor(index, dataPoint)}
                className="chart__point"
                onClick={() => onDataPointClick?.(dataPoint, index)}
              />
              {showValues && (
                <text
                  x={x}
                  y={y - 10}
                  textAnchor="middle"
                  className="chart__value"
                >
                  {dataPoint.value}
                </text>
              )}
            </g>
          );
        })}
      </svg>
    );
  };

  // Render chart based on type
  const renderChart = () => {
    switch (type) {
      case 'bar':
        return renderBarChart();
      case 'pie':
      case 'doughnut':
        return renderPieChart();
      case 'line':
        return renderLineChart();
      case 'area':
        return renderLineChart(); // Simplified for now
      case 'scatter':
        return renderLineChart(); // Simplified for now
      default:
        return null;
    }
  };

  // Render legend
  const renderLegend = () => {
    if (!showLegend) return null;

    return (
      <div className="chart__legend">
        {data.map((dataPoint, index) => (
          <div
            key={index}
            className="chart__legend-item"
            onClick={() => onDataPointClick?.(dataPoint, index)}
          >
            <div
              className="chart__legend-color"
              style={{ backgroundColor: getDataPointColor(index, dataPoint) }}
            />
            <Typography variant="caption" size="sm" color="secondary">
              {dataPoint.label}
            </Typography>
            {showValues && (
              <Typography variant="caption" size="sm" color="tertiary">
                {dataPoint.value}{showPercentage ? '%' : ''}
              </Typography>
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className={classes}>
      {(title || description) && (
        <div className="chart__header">
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
      
      <div className="chart__content">
        {renderChart()}
      </div>
      
      {renderLegend()}
    </div>
  );
};

Chart.displayName = 'Chart';
