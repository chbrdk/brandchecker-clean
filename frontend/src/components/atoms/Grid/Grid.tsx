import React from 'react';
import './Grid.css';

export interface GridProps {
  children: React.ReactNode;
  columns?: 1 | 2 | 3 | 4 | 6 | 12;
  gap?: 'none' | 'sm' | 'md' | 'lg';
  className?: string;
}

export interface GridItemProps {
  children: React.ReactNode;
  span?: 1 | 2 | 3 | 4 | 6 | 12;
  className?: string;
}

export const Grid = ({
  children,
  columns = 12,
  gap = 'md',
  className = '',
  ...props
}: GridProps) => {
  const classes = [
    'grid',
    `grid--cols-${columns}`,
    `grid--gap-${gap}`,
    className,
  ].filter(Boolean).join(' ');

  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};

export const GridItem = ({
  children,
  span = 12,
  className = '',
  ...props
}: GridItemProps) => {
  const classes = [
    'grid-item',
    `grid-item--span-${span}`,
    className,
  ].filter(Boolean).join(' ');

  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};
