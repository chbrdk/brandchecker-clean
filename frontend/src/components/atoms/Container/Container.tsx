import React from 'react';
import './Container.css';

export interface ContainerProps {
  /** Container content */
  children: React.ReactNode;
  /** Maximum width */
  maxWidth?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl' | '6xl' | '7xl' | 'full';
  /** Padding size */
  padding?: 'none' | 'small' | 'medium' | 'large';
  /** Center the container */
  center?: boolean;
  /** Fluid container (no max-width) */
  fluid?: boolean;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/** Container component for responsive layouts */
export const Container = ({
  children,
  maxWidth = '7xl',
  padding = 'medium',
  center = true,
  fluid = false,
  className = '',
  ...props
}: ContainerProps) => {
  const containerClasses = [
    'container',
    !fluid && `container--max-width-${maxWidth}`,
    `container--padding-${padding}`,
    center && 'container--center',
    fluid && 'container--fluid',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={containerClasses} {...props}>
      {children}
    </div>
  );
};
