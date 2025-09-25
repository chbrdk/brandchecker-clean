import React from 'react';
import './Spacer.css';

export interface SpacerProps {
  /** Spacer size */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl';
  /** Responsive spacer sizes */
  responsive?: {
    xs?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl';
    sm?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl';
    md?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl';
    lg?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl';
    xl?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl';
    '2xl'?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl';
  };
  /** Spacer direction */
  direction?: 'horizontal' | 'vertical' | 'both';
  /** Custom CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/** Responsive Spacer Component for precise spacing control */
export const Spacer = ({
  size = 'md',
  responsive,
  direction = 'vertical',
  className = '',
  ...props
}: SpacerProps) => {
  const classes = [
    'spacer',
    `spacer--${direction}`,
    `spacer--${size}`,
    className
  ].filter(Boolean).join(' ');

  // Generate CSS custom properties for responsive sizing
  const spacerStyle = React.useMemo(() => {
    if (!responsive) return {};

    return {
      '--spacer-size-xs': `var(--spacer-${responsive.xs || size})`,
      '--spacer-size-sm': `var(--spacer-${responsive.sm || responsive.xs || size})`,
      '--spacer-size-md': `var(--spacer-${responsive.md || responsive.sm || responsive.xs || size})`,
      '--spacer-size-lg': `var(--spacer-${responsive.lg || responsive.md || responsive.sm || responsive.xs || size})`,
      '--spacer-size-xl': `var(--spacer-${responsive.xl || responsive.lg || responsive.md || responsive.sm || responsive.xs || size})`,
      '--spacer-size-2xl': `var(--spacer-${responsive['2xl'] || responsive.xl || responsive.lg || responsive.md || responsive.sm || responsive.xs || size})`,
    } as React.CSSProperties;
  }, [size, responsive]);

  return (
    <div 
      className={classes} 
      style={spacerStyle}
      aria-hidden="true"
      {...props}
    />
  );
};

// Convenience components for common use cases
export const VerticalSpacer = (props: Omit<SpacerProps, 'direction'>) => (
  <Spacer {...props} direction="vertical" />
);

export const HorizontalSpacer = (props: Omit<SpacerProps, 'direction'>) => (
  <Spacer {...props} direction="horizontal" />
);

export const ResponsiveSpacer = (props: Omit<SpacerProps, 'responsive'>) => (
  <Spacer 
    {...props} 
    responsive={{
      xs: 'sm',
      sm: 'md', 
      md: 'lg',
      lg: 'xl',
      xl: 'xl',
      '2xl': 'xl'
    }}
  />
);
