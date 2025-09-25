import type { Meta, StoryObj } from '@storybook/react';
import { Accordion, AccordionItem } from '../../components/molecules';

const meta: Meta<typeof Accordion> = {
  title: 'Molecules/Accordion',
  component: Accordion,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'A flexible accordion component with collapsible sections, customizable icons, and multiple variants.',
      },
    },
  },
  argTypes: {
    allowMultiple: {
      control: 'boolean',
      description: 'Allow multiple items to be open simultaneously',
    },
    bordered: {
      control: 'boolean',
      description: 'Show borders between accordion items',
    },
    variant: {
      control: 'select',
      options: ['default', 'flush', 'outlined'],
      description: 'Accordion visual variant',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Accordion>;

export const Default: Story = {
  args: {
    children: (
      <>
        <AccordionItem title="What is BrandChecker?">
          <p>BrandChecker is a comprehensive brand analysis tool that helps you maintain consistency across all your brand materials. It analyzes PDFs, images, and documents to ensure they comply with your brand guidelines.</p>
        </AccordionItem>
        <AccordionItem title="How does the analysis work?">
          <p>Our AI-powered system uses advanced computer vision and natural language processing to:</p>
          <ul>
            <li>Extract colors and fonts from your documents</li>
            <li>Analyze layout and spacing</li>
            <li>Detect logos and brand elements</li>
            <li>Compare against your brand guidelines</li>
          </ul>
        </AccordionItem>
        <AccordionItem title="What file types are supported?">
          <p>BrandChecker supports a wide range of file formats:</p>
          <ul>
            <li>PDF documents</li>
            <li>Images (PNG, JPG, SVG)</li>
            <li>Microsoft Office documents</li>
            <li>Design files (AI, PSD)</li>
          </ul>
        </AccordionItem>
      </>
    ),
  },
};

export const AllowMultiple: Story = {
  args: {
    allowMultiple: true,
    children: (
      <>
        <AccordionItem title="Brand Guidelines" defaultExpanded>
          <p>Our comprehensive brand guidelines ensure consistency across all touchpoints.</p>
        </AccordionItem>
        <AccordionItem title="Color Palette" defaultExpanded>
          <p>Primary colors, secondary colors, and accent colors that define our brand.</p>
        </AccordionItem>
        <AccordionItem title="Typography">
          <p>Font families, sizes, and usage guidelines for all brand materials.</p>
        </AccordionItem>
      </>
    ),
  },
};

export const FlushVariant: Story = {
  args: {
    variant: 'flush',
    bordered: false,
    children: (
      <>
        <AccordionItem title="Dashboard Overview">
          <p>Get a quick overview of your brand compliance metrics and recent analyses.</p>
        </AccordionItem>
        <AccordionItem title="Recent Analyses">
          <p>View your most recent brand analysis results and compliance scores.</p>
        </AccordionItem>
        <AccordionItem title="Settings">
          <p>Configure your brand guidelines and analysis preferences.</p>
        </AccordionItem>
      </>
    ),
  },
};

export const OutlinedVariant: Story = {
  args: {
    variant: 'outlined',
    children: (
      <>
        <AccordionItem title="Analysis Results">
          <p>Detailed breakdown of your brand analysis results including compliance scores and recommendations.</p>
        </AccordionItem>
        <AccordionItem title="Recommendations">
          <p>Actionable recommendations to improve your brand compliance and consistency.</p>
        </AccordionItem>
        <AccordionItem title="Export Options">
          <p>Export your analysis results in various formats for sharing and documentation.</p>
        </AccordionItem>
      </>
    ),
  },
};

export const WithCustomIcons: Story = {
  args: {
    children: (
      <>
        <AccordionItem title="Brand Analysis" icon="eye" iconPosition="left">
          <p>Comprehensive analysis of your brand materials including colors, fonts, and layout.</p>
        </AccordionItem>
        <AccordionItem title="Color Analysis" icon="color-palette" iconPosition="left">
          <p>Detailed color extraction and compliance checking against your brand palette.</p>
        </AccordionItem>
        <AccordionItem title="Typography Analysis" icon="type" iconPosition="left">
          <p>Font detection and analysis to ensure typography compliance.</p>
        </AccordionItem>
        <AccordionItem title="Logo Detection" icon="logo" iconPosition="left">
          <p>Automatic logo detection and brand element recognition.</p>
        </AccordionItem>
      </>
    ),
  },
};

export const DisabledItems: Story = {
  args: {
    children: (
      <>
        <AccordionItem title="Available Feature" defaultExpanded>
          <p>This feature is available and working properly.</p>
        </AccordionItem>
        <AccordionItem title="Coming Soon" disabled>
          <p>This feature is currently under development and will be available soon.</p>
        </AccordionItem>
        <AccordionItem title="Premium Feature" disabled>
          <p>This feature is available for premium users only.</p>
        </AccordionItem>
      </>
    ),
  },
};

export const LongContent: Story = {
  args: {
    children: (
      <>
        <AccordionItem title="Detailed Brand Guidelines">
          <div>
            <h4>Brand Identity</h4>
            <p>Our brand identity is built on the principles of trust, innovation, and accessibility. Every element of our visual identity should reflect these core values.</p>
            
            <h4>Logo Usage</h4>
            <p>The BrandChecker logo should always be used according to these guidelines:</p>
            <ul>
              <li>Maintain clear space around the logo</li>
              <li>Use approved color variations only</li>
              <li>Never distort or modify the logo</li>
              <li>Ensure adequate contrast on backgrounds</li>
            </ul>
            
            <h4>Color System</h4>
            <p>Our color system consists of primary, secondary, and accent colors that work together to create a cohesive visual experience.</p>
            
            <h4>Typography</h4>
            <p>We use a carefully selected typeface that ensures readability and maintains our brand personality across all applications.</p>
          </div>
        </AccordionItem>
        <AccordionItem title="Technical Specifications">
          <div>
            <h4>API Endpoints</h4>
            <p>Our REST API provides comprehensive access to all BrandChecker functionality.</p>
            
            <h4>Rate Limits</h4>
            <p>API requests are limited to ensure fair usage and system stability.</p>
            
            <h4>Authentication</h4>
            <p>Secure authentication using industry-standard protocols.</p>
          </div>
        </AccordionItem>
      </>
    ),
  },
};

export const InteractiveExample: Story = {
  args: {
    allowMultiple: true,
    variant: 'outlined',
    children: (
      <>
        <AccordionItem title="Getting Started" defaultExpanded>
          <div>
            <p>Welcome to BrandChecker! Here's how to get started:</p>
            <ol>
              <li>Upload your brand guidelines</li>
              <li>Configure your analysis preferences</li>
              <li>Upload documents for analysis</li>
              <li>Review your compliance reports</li>
            </ol>
          </div>
        </AccordionItem>
        <AccordionItem title="Best Practices">
          <div>
            <p>Follow these best practices for optimal results:</p>
            <ul>
              <li>Use high-quality source documents</li>
              <li>Ensure proper file formats</li>
              <li>Regularly update brand guidelines</li>
              <li>Review analysis results regularly</li>
            </ul>
          </div>
        </AccordionItem>
        <AccordionItem title="Troubleshooting">
          <div>
            <p>Common issues and solutions:</p>
            <ul>
              <li>File upload problems</li>
              <li>Analysis accuracy issues</li>
              <li>Integration challenges</li>
              <li>Performance optimization</li>
            </ul>
          </div>
        </AccordionItem>
      </>
    ),
  },
};
