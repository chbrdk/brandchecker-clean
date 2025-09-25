import React from 'react';
import './Typography.css';

/**
 * Typography Component Props
 * 
 * Provides comprehensive typography control with consistent font sizes, weights, colors, and text modifiers.
 * Supports all standard HTML heading elements (h1-h6) and text variants (body, caption, small, lead, subtitle).
 * 
 * @interface TypographyProps
 */
export interface TypographyProps {
  /** Typography variant */
  variant?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'body' | 'caption' | 'small' | 'lead' | 'subtitle';
  /** Typography size */
  size?: 'xs' | 'sm' | 'base' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl' | '6xl';
  /** Typography weight */
  weight?: 'light' | 'normal' | 'medium' | 'semibold' | 'bold' | 'extrabold';
  /** Typography color */
  color?: 'primary' | 'secondary' | 'tertiary' | 'success' | 'warning' | 'error' | 'info' | 'muted';
  /** Typography alignment */
  align?: 'left' | 'center' | 'right' | 'justify';
  /** Whether text should be truncated */
  truncate?: boolean;
  /** Whether text should be uppercase */
  uppercase?: boolean;
  /** Whether text should be lowercase */
  lowercase?: boolean;
  /** Whether text should be capitalized */
  capitalize?: boolean;
  /** Whether text should be italic */
  italic?: boolean;
  /** Whether text should be underlined */
  underline?: boolean;
  /** Whether text should be strikethrough */
  strikethrough?: boolean;
  /** Additional CSS class */
  className?: string;
  /** Children content */
  children: React.ReactNode;
  /** Additional props */
  [key: string]: any;
}

/**
 * Typography Component
 * 
 * A comprehensive typography system component that provides consistent text styling across the application.
 * Supports semantic HTML elements (h1-h6, p) with customizable variants, sizes, weights, colors, and text modifiers.
 * 
 * Features:
 * - Semantic HTML elements (h1-h6 for headings, p for body text)
 * - Responsive font sizes with mobile-first approach
 * - Consistent color system integration
 * - Text transformation and styling options
 * - Accessibility-friendly with proper ARIA attributes
 * 
 * @param props - TypographyProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Basic usage
 * <Typography variant="h1">Main Title</Typography>
 * <Typography variant="body" color="primary">Body text</Typography>
 * 
 * // With modifiers
 * <Typography variant="caption" uppercase italic>Caption Text</Typography>
 * 
 * // Responsive sizing
 * <Typography variant="h2" size="lg">Responsive Heading</Typography>
 * ```
 */
export const Typography = ({
  variant = 'body',
  size,
  weight,
  color = 'primary',
  align,
  truncate = false,
  uppercase = false,
  lowercase = false,
  capitalize = false,
  italic = false,
  underline = false,
  strikethrough = false,
  className = '',
  children,
  ...props
}: TypographyProps) => {
  // Build CSS classes based on props
  const classes = [
    'typography',
    `typography--${variant}`,
    size && `typography--size-${size}`,
    weight && `typography--weight-${weight}`,
    `typography--color-${color}`,
    align && `typography--align-${align}`,
    truncate && 'typography--truncate',
    uppercase && 'typography--uppercase',
    lowercase && 'typography--lowercase',
    capitalize && 'typography--capitalize',
    italic && 'typography--italic',
    underline && 'typography--underline',
    strikethrough && 'typography--strikethrough',
    className
  ].filter(Boolean).join(' ');

  // Determine HTML element based on variant
  // h1-h6 variants use semantic heading elements, others use paragraph
  const Component = variant.startsWith('h') ? variant as keyof JSX.IntrinsicElements : 'p';

  return (
    <Component className={classes} {...props}>
      {children}
    </Component>
  );
};

/** Heading Components - Convenience components for semantic headings */

/**
 * Heading1 Component
 * 
 * Convenience component for h1 headings with consistent styling.
 * 
 * @param props - Omit<TypographyProps, 'variant'>
 * @returns JSX.Element
 */
export const Heading1 = ({ children, ...props }: Omit<TypographyProps, 'variant'>) => (
  <Typography variant="h1" {...props}>{children}</Typography>
);

/**
 * Heading2 Component
 * 
 * Convenience component for h2 headings with consistent styling.
 * 
 * @param props - Omit<TypographyProps, 'variant'>
 * @returns JSX.Element
 */
export const Heading2 = ({ children, ...props }: Omit<TypographyProps, 'variant'>) => (
  <Typography variant="h2" {...props}>{children}</Typography>
);

/**
 * Heading3 Component
 * 
 * Convenience component for h3 headings with consistent styling.
 * 
 * @param props - Omit<TypographyProps, 'variant'>
 * @returns JSX.Element
 */
export const Heading3 = ({ children, ...props }: Omit<TypographyProps, 'variant'>) => (
  <Typography variant="h3" {...props}>{children}</Typography>
);

/**
 * Heading4 Component
 * 
 * Convenience component for h4 headings with consistent styling.
 * 
 * @param props - Omit<TypographyProps, 'variant'>
 * @returns JSX.Element
 */
export const Heading4 = ({ children, ...props }: Omit<TypographyProps, 'variant'>) => (
  <Typography variant="h4" {...props}>{children}</Typography>
);

/**
 * Heading5 Component
 * 
 * Convenience component for h5 headings with consistent styling.
 * 
 * @param props - Omit<TypographyProps, 'variant'>
 * @returns JSX.Element
 */
export const Heading5 = ({ children, ...props }: Omit<TypographyProps, 'variant'>) => (
  <Typography variant="h5" {...props}>{children}</Typography>
);

/**
 * Heading6 Component
 * 
 * Convenience component for h6 headings with consistent styling.
 * 
 * @param props - Omit<TypographyProps, 'variant'>
 * @returns JSX.Element
 */
export const Heading6 = ({ children, ...props }: Omit<TypographyProps, 'variant'>) => (
  <Typography variant="h6" {...props}>{children}</Typography>
);

/** Text Components - Convenience components for different text types */

/**
 * Body Component
 * 
 * Convenience component for body text with consistent styling.
 * 
 * @param props - Omit<TypographyProps, 'variant'>
 * @returns JSX.Element
 */
export const Body = ({ children, ...props }: Omit<TypographyProps, 'variant'>) => (
  <Typography variant="body" {...props}>{children}</Typography>
);

/**
 * Caption Component
 * 
 * Convenience component for caption text with consistent styling.
 * 
 * @param props - Omit<TypographyProps, 'variant'>
 * @returns JSX.Element
 */
export const Caption = ({ children, ...props }: Omit<TypographyProps, 'variant'>) => (
  <Typography variant="caption" {...props}>{children}</Typography>
);

/**
 * Small Component
 * 
 * Convenience component for small text with consistent styling.
 * 
 * @param props - Omit<TypographyProps, 'variant'>
 * @returns JSX.Element
 */
export const Small = ({ children, ...props }: Omit<TypographyProps, 'variant'>) => (
  <Typography variant="small" {...props}>{children}</Typography>
);

/**
 * Lead Component
 * 
 * Convenience component for lead text with consistent styling.
 * 
 * @param props - Omit<TypographyProps, 'variant'>
 * @returns JSX.Element
 */
export const Lead = ({ children, ...props }: Omit<TypographyProps, 'variant'>) => (
  <Typography variant="lead" {...props}>{children}</Typography>
);

/**
 * Subtitle Component
 * 
 * Convenience component for subtitle text with consistent styling.
 * 
 * @param props - Omit<TypographyProps, 'variant'>
 * @returns JSX.Element
 */
export const Subtitle = ({ children, ...props }: Omit<TypographyProps, 'variant'>) => (
  <Typography variant="subtitle" {...props}>{children}</Typography>
);

/** Brand-specific Typography */

/**
 * Brand Typography Props
 * 
 * Props for brand-specific typography components that use custom brand fonts and styling.
 * 
 * @interface BrandTypographyProps
 */
export interface BrandTypographyProps {
  /** Brand typography type */
  type?: 'brand-name' | 'brand-tagline' | 'brand-description' | 'brand-heading';
  /** Additional CSS class */
  className?: string;
  /** Children content */
  children: React.ReactNode;
  /** Additional props */
  [key: string]: any;
}

/**
 * BrandTypography Component
 * 
 * Specialized typography component for brand-specific text elements.
 * Uses custom brand fonts and styling to maintain brand consistency.
 * 
 * Features:
 * - Brand-specific font families
 * - Custom brand colors
 * - Consistent brand styling
 * - Semantic brand text types
 * 
 * @param props - BrandTypographyProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * <BrandTypography type="brand-name">BrandChecker</BrandTypography>
 * <BrandTypography type="brand-tagline">Your Brand Analysis Platform</BrandTypography>
 * ```
 */
export const BrandTypography = ({
  type = 'brand-name',
  className = '',
  children,
  ...props
}: BrandTypographyProps) => {
  // Build CSS classes for brand typography
  const classes = [
    'brand-typography',
    `brand-typography--${type}`,
    className
  ].filter(Boolean).join(' ');

  return (
    <span className={classes} {...props}>
      {children}
    </span>
  );
};
