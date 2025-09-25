import React from 'react';
import './Card.css';

export interface CardProps {
  /** Card content */
  children: React.ReactNode;
  /** Card title */
  title?: string;
  /** Card subtitle */
  subtitle?: string;
  /** Custom header content */
  header?: React.ReactNode;
  /** Custom footer content */
  footer?: React.ReactNode;
  /** Card variant */
  variant?: 'elevated' | 'outlined' | 'filled';
  /** Padding size */
  padding?: 'none' | 'small' | 'medium' | 'large';
  /** Hoverable card */
  hoverable?: boolean;
  /** Clickable card */
  clickable?: boolean;
  /** Loading state */
  loading?: boolean;
  /** Additional CSS class */
  className?: string;
  /** Click handler */
  onClick?: () => void;
  /** Additional props */
  [key: string]: any;
}

/** Card component with multiple variants and interactive states */
export const Card = ({
  children,
  title,
  subtitle,
  header,
  footer,
  variant = 'elevated',
  padding = 'medium',
  hoverable = false,
  clickable = false,
  loading = false,
  className = '',
  onClick,
  ...props
}: CardProps) => {
  const hasHeader = !!(title || subtitle || header);
  const hasFooter = !!footer;
  const isInteractive = clickable || hoverable;
  
  const cardClasses = [
    'card',
    `card--${variant}`,
    `card--padding-${padding}`,
    hoverable && 'card--hoverable',
    clickable && 'card--clickable',
    loading && 'card--loading',
    isInteractive && 'card--interactive',
    className
  ].filter(Boolean).join(' ');

  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (clickable && onClick) {
      onClick();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (clickable && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault();
      onClick?.();
    }
  };

  const renderHeader = () => {
    if (!hasHeader) return null;
    
    return (
      <div className="card__header">
        {header || (
          <>
            {title && <h3 className="card__title">{title}</h3>}
            {subtitle && <p className="card__subtitle">{subtitle}</p>}
          </>
        )}
      </div>
    );
  };

  const renderContent = () => {
    if (loading) {
      return (
        <div className="card__content">
          <div className="card__skeleton" data-testid="card-skeleton">
            <div className="card__skeleton-line card__skeleton-line--title" data-testid="skeleton-line"></div>
            <div className="card__skeleton-line card__skeleton-line--text" data-testid="skeleton-line"></div>
            <div className="card__skeleton-line card__skeleton-line--text" data-testid="skeleton-line"></div>
            <div className="card__skeleton-line card__skeleton-line--text-short" data-testid="skeleton-line"></div>
          </div>
        </div>
      );
    }
    
    return <div className="card__content">{children}</div>;
  };

  const renderFooter = () => {
    if (!hasFooter) return null;
    
    return <div className="card__footer">{footer}</div>;
  };

  return (
    <div
      className={cardClasses}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      role={clickable ? 'button' : undefined}
      tabIndex={clickable ? 0 : undefined}
      {...props}
    >
      {renderHeader()}
      {renderContent()}
      {renderFooter()}
    </div>
  );
};
