import type { Meta, StoryObj } from '@storybook/react';
import { Spacer, VerticalSpacer, HorizontalSpacer, ResponsiveSpacer } from '../../components/atoms/Spacer';

const meta: Meta<typeof Spacer> = {
  title: 'Atoms/Spacer',
  component: Spacer,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'Responsive spacer utilities for precise spacing control. Mobile-first approach with responsive sizing.',
      },
    },
  },
  argTypes: {
    size: {
      control: 'select',
      options: ['xs', 'sm', 'md', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl'],
      description: 'Spacer size',
    },
    direction: {
      control: 'select',
      options: ['horizontal', 'vertical', 'both'],
      description: 'Spacer direction',
    },
    responsive: {
      control: 'object',
      description: 'Responsive spacer sizes',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

// Helper component for demo
const DemoBox = ({ children, color = '#e2e8f0' }: { children: React.ReactNode; color?: string }) => (
  <div style={{
    backgroundColor: color,
    padding: '16px',
    borderRadius: '8px',
    textAlign: 'center',
    minHeight: '60px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '14px',
    fontWeight: '500',
  }}>
    {children}
  </div>
);

// Basic Vertical Spacers
export const VerticalSpacers: Story = {
  render: () => (
    <div>
      <h3 style={{ marginBottom: '16px' }}>Vertical Spacers</h3>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <DemoBox color="#dbeafe">Content Above</DemoBox>
        <VerticalSpacer size="xs" />
        <DemoBox color="#fef3c7">XS Spacer (4px)</DemoBox>
        <VerticalSpacer size="sm" />
        <DemoBox color="#dcfce7">SM Spacer (8px)</DemoBox>
        <VerticalSpacer size="md" />
        <DemoBox color="#fce7f3">MD Spacer (16px)</DemoBox>
        <VerticalSpacer size="lg" />
        <DemoBox color="#e0e7ff">LG Spacer (24px)</DemoBox>
        <VerticalSpacer size="xl" />
        <DemoBox color="#fed7d7">XL Spacer (32px)</DemoBox>
        <VerticalSpacer size="2xl" />
        <DemoBox color="#d1fae5">2XL Spacer (48px)</DemoBox>
      </div>
    </div>
  ),
};

// Horizontal Spacers
export const HorizontalSpacers: Story = {
  render: () => (
    <div>
      <h3 style={{ marginBottom: '16px' }}>Horizontal Spacers</h3>
      <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}>
        <DemoBox color="#dbeafe">Left</DemoBox>
        <HorizontalSpacer size="xs" />
        <DemoBox color="#fef3c7">XS</DemoBox>
        <HorizontalSpacer size="sm" />
        <DemoBox color="#dcfce7">SM</DemoBox>
        <HorizontalSpacer size="md" />
        <DemoBox color="#fce7f3">MD</DemoBox>
        <HorizontalSpacer size="lg" />
        <DemoBox color="#e0e7ff">LG</DemoBox>
        <HorizontalSpacer size="xl" />
        <DemoBox color="#fed7d7">XL</DemoBox>
        <HorizontalSpacer size="2xl" />
        <DemoBox color="#d1fae5">Right</DemoBox>
      </div>
    </div>
  ),
};

// Responsive Spacers
export const ResponsiveSpacers: Story = {
  render: () => (
    <div>
      <h3 style={{ marginBottom: '16px' }}>Responsive Spacers</h3>
      <p style={{ marginBottom: '16px', color: '#666', fontSize: '14px' }}>
        Resize your browser to see responsive behavior: Mobile (xs) → Desktop (xl)
      </p>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <DemoBox color="#dbeafe">Content Above</DemoBox>
        <ResponsiveSpacer />
        <DemoBox color="#fef3c7">
          Responsive Spacer<br/>
          <small>Mobile: 8px → Desktop: 32px</small>
        </DemoBox>
        <VerticalSpacer 
          responsive={{
            xs: 'xs',
            sm: 'sm',
            md: 'md',
            lg: 'lg',
            xl: 'xl',
            '2xl': '2xl'
          }}
        />
        <DemoBox color="#dcfce7">
          Custom Responsive<br/>
          <small>XS: 4px → 2XL: 48px</small>
        </DemoBox>
      </div>
    </div>
  ),
};

// BrandChecker Layout Example
export const BrandCheckerLayout: Story = {
  render: () => (
    <div>
      <h3 style={{ marginBottom: '16px' }}>BrandChecker Layout Example</h3>
      <div style={{ 
        border: '1px solid #e5e7eb', 
        borderRadius: '12px', 
        padding: '20px',
        backgroundColor: 'white'
      }}>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h4 style={{ margin: 0, color: '#1f2937' }}>Brand Analysis Results</h4>
          <div style={{ fontSize: '12px', color: '#6b7280' }}>87% Compliance</div>
        </div>
        
        <VerticalSpacer size="lg" />
        
        {/* Stats Row */}
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          <div style={{ flex: '1', minWidth: '120px' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#3b82f6' }}>142</div>
            <div style={{ fontSize: '12px', color: '#6b7280' }}>Documents</div>
          </div>
          <div style={{ flex: '1', minWidth: '120px' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#10b981' }}>89%</div>
            <div style={{ fontSize: '12px', color: '#6b7280' }}>Compliance</div>
          </div>
          <div style={{ flex: '1', minWidth: '120px' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f59e0b' }}>23</div>
            <div style={{ fontSize: '12px', color: '#6b7280' }}>Issues</div>
          </div>
        </div>
        
        <VerticalSpacer size="xl" />
        
        {/* Analysis Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
          <div style={{ 
            backgroundColor: '#f0f9ff', 
            border: '1px solid #bae6fd', 
            borderRadius: '8px', 
            padding: '16px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '20px', marginBottom: '8px' }}>🎨</div>
            <div style={{ fontWeight: '500', marginBottom: '4px' }}>Color Analysis</div>
            <div style={{ fontSize: '12px', color: '#0369a1' }}>Brand compliance check</div>
          </div>
          <div style={{ 
            backgroundColor: '#f0fdf4', 
            border: '1px solid #bbf7d0', 
            borderRadius: '8px', 
            padding: '16px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '20px', marginBottom: '8px' }}>🔤</div>
            <div style={{ fontWeight: '500', marginBottom: '4px' }}>Font Analysis</div>
            <div style={{ fontSize: '12px', color: '#15803d' }}>Typography compliance</div>
          </div>
          <div style={{ 
            backgroundColor: '#fef3c7', 
            border: '1px solid #fde68a', 
            borderRadius: '8px', 
            padding: '16px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '20px', marginBottom: '8px' }}>📷</div>
            <div style={{ fontWeight: '500', marginBottom: '4px' }}>Logo Detection</div>
            <div style={{ fontSize: '12px', color: '#d97706' }}>Brand logo identification</div>
          </div>
        </div>
        
        <VerticalSpacer size="lg" />
        
        {/* Action Buttons */}
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
          <button style={{
            padding: '8px 16px',
            border: '1px solid #d1d5db',
            borderRadius: '6px',
            backgroundColor: 'white',
            fontSize: '14px',
            cursor: 'pointer'
          }}>
            Export Report
          </button>
          <button style={{
            padding: '8px 16px',
            border: 'none',
            borderRadius: '6px',
            backgroundColor: '#3b82f6',
            color: 'white',
            fontSize: '14px',
            cursor: 'pointer'
          }}>
            View Details
          </button>
        </div>
      </div>
    </div>
  ),
};

// Form Layout Example
export const FormLayout: Story = {
  render: () => (
    <div>
      <h3 style={{ marginBottom: '16px' }}>Form Layout with Spacers</h3>
      <div style={{ 
        border: '1px solid #e5e7eb', 
        borderRadius: '12px', 
        padding: '24px',
        backgroundColor: 'white',
        maxWidth: '400px'
      }}>
        <h4 style={{ margin: '0 0 16px 0', color: '#1f2937' }}>Upload Brand Guidelines</h4>
        
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500', fontSize: '14px' }}>
            Company Name
          </label>
          <input 
            type="text" 
            placeholder="Enter company name"
            style={{ 
              width: '100%', 
              padding: '8px 12px', 
              border: '1px solid #d1d5db', 
              borderRadius: '6px',
              fontSize: '14px'
            }}
          />
        </div>
        
        <VerticalSpacer size="md" />
        
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500', fontSize: '14px' }}>
            Brand Guidelines PDF
          </label>
          <div style={{
            border: '2px dashed #d1d5db',
            borderRadius: '8px',
            padding: '20px',
            textAlign: 'center',
            color: '#6b7280',
            fontSize: '14px'
          }}>
            📄 Drop PDF files here
          </div>
        </div>
        
        <VerticalSpacer size="lg" />
        
        <div style={{ display: 'flex', gap: '12px' }}>
          <button style={{
            flex: 1,
            padding: '10px 16px',
            border: '1px solid #d1d5db',
            borderRadius: '6px',
            backgroundColor: 'white',
            fontSize: '14px',
            cursor: 'pointer'
          }}>
            Cancel
          </button>
          <button style={{
            flex: 1,
            padding: '10px 16px',
            border: 'none',
            borderRadius: '6px',
            backgroundColor: '#3b82f6',
            color: 'white',
            fontSize: '14px',
            cursor: 'pointer'
          }}>
            Upload & Analyze
          </button>
        </div>
      </div>
    </div>
  ),
};

// Mobile Optimized
export const MobileOptimized: Story = {
  render: () => (
    <div>
      <h3 style={{ marginBottom: '16px' }}>Mobile-Optimized Spacing</h3>
      <p style={{ marginBottom: '16px', color: '#666', fontSize: '14px' }}>
        Spacers automatically adjust for mobile devices
      </p>
      <div style={{ 
        border: '1px solid #e5e7eb', 
        borderRadius: '12px', 
        padding: '16px',
        backgroundColor: 'white'
      }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <div style={{ 
            backgroundColor: '#f3f4f6', 
            padding: '12px', 
            borderRadius: '6px',
            fontSize: '14px',
            textAlign: 'center'
          }}>
            Mobile Card 1
          </div>
          <VerticalSpacer size="sm" />
          <div style={{ 
            backgroundColor: '#f3f4f6', 
            padding: '12px', 
            borderRadius: '6px',
            fontSize: '14px',
            textAlign: 'center'
          }}>
            Mobile Card 2
          </div>
          <VerticalSpacer size="md" />
          <div style={{ 
            backgroundColor: '#f3f4f6', 
            padding: '12px', 
            borderRadius: '6px',
            fontSize: '14px',
            textAlign: 'center'
          }}>
            Mobile Card 3
          </div>
        </div>
      </div>
    </div>
  ),
};

// All Sizes Showcase
export const AllSizes: Story = {
  render: () => (
    <div>
      <h3 style={{ marginBottom: '16px' }}>All Spacer Sizes</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {['xs', 'sm', 'md', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl'].map((size) => (
          <div key={size} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ width: '60px', fontSize: '12px', fontWeight: '500' }}>
              {size.toUpperCase()}
            </div>
            <div style={{ 
              backgroundColor: '#e5e7eb', 
              height: '2px', 
              width: '200px',
              position: 'relative'
            }}>
              <div style={{
                position: 'absolute',
                top: '-8px',
                left: '0',
                width: '100%',
                height: '18px',
                backgroundColor: '#3b82f6',
                borderRadius: '2px',
                opacity: 0.3
              }} />
            </div>
            <VerticalSpacer size={size as any} />
            <div style={{ 
              backgroundColor: '#3b82f6', 
              color: 'white',
              padding: '4px 8px',
              borderRadius: '4px',
              fontSize: '12px',
              fontWeight: '500'
            }}>
              {size}
            </div>
          </div>
        ))}
      </div>
    </div>
  ),
};

// Playground
export const Playground: Story = {
  args: {
    size: 'md',
    direction: 'vertical',
  },
  render: (args) => (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <DemoBox color="#dbeafe">Content Above</DemoBox>
      <Spacer {...args} />
      <DemoBox color="#fef3c7">Content Below</DemoBox>
    </div>
  ),
};
