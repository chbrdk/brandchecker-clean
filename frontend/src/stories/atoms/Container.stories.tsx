import type { Meta, StoryObj } from '@storybook/react';
import { Container } from '../../components/atoms/Container';

const meta: Meta<typeof Container> = {
  title: 'Atoms/Container',
  component: Container,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'A responsive container component for layout management with configurable max-width and padding.',
      },
    },
  },
  argTypes: {
    maxWidth: {
      control: 'select',
      options: ['xs', 'sm', 'md', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl', '6xl', '7xl', 'full'],
      description: 'Maximum width of the container',
    },
    padding: {
      control: 'select',
      options: ['none', 'small', 'medium', 'large'],
      description: 'Horizontal padding size',
    },
    center: {
      control: 'boolean',
      description: 'Center the container horizontally',
    },
    fluid: {
      control: 'boolean',
      description: 'Make container fluid (no max-width)',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

// Default story
export const Default: Story = {
  args: {
    children: (
      <div style={{ 
        backgroundColor: '#f0f0f0', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #ccc'
      }}>
        Default Container Content
      </div>
    ),
  },
};

// Different max widths
export const Small: Story = {
  args: {
    maxWidth: 'sm',
    children: (
      <div style={{ 
        backgroundColor: '#e3f2fd', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #2196f3'
      }}>
        Small Container (384px max-width)
      </div>
    ),
  },
};

export const Medium: Story = {
  args: {
    maxWidth: 'md',
    children: (
      <div style={{ 
        backgroundColor: '#e8f5e8', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #4caf50'
      }}>
        Medium Container (448px max-width)
      </div>
    ),
  },
};

export const Large: Story = {
  args: {
    maxWidth: 'lg',
    children: (
      <div style={{ 
        backgroundColor: '#fff3e0', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #ff9800'
      }}>
        Large Container (512px max-width)
      </div>
    ),
  },
};

export const ExtraLarge: Story = {
  args: {
    maxWidth: 'xl',
    children: (
      <div style={{ 
        backgroundColor: '#fce4ec', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #e91e63'
      }}>
        Extra Large Container (576px max-width)
      </div>
    ),
  },
};

export const FullWidth: Story = {
  args: {
    maxWidth: '7xl',
    children: (
      <div style={{ 
        backgroundColor: '#f3e5f5', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #9c27b0'
      }}>
        Full Width Container (1280px max-width)
      </div>
    ),
  },
};

// Padding variants
export const NoPadding: Story = {
  args: {
    maxWidth: 'md',
    padding: 'none',
    children: (
      <div style={{ 
        backgroundColor: '#ffebee', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #f44336'
      }}>
        Container with No Padding
      </div>
    ),
  },
};

export const SmallPadding: Story = {
  args: {
    maxWidth: 'md',
    padding: 'small',
    children: (
      <div style={{ 
        backgroundColor: '#e0f2f1', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #009688'
      }}>
        Container with Small Padding
      </div>
    ),
  },
};

export const MediumPadding: Story = {
  args: {
    maxWidth: 'md',
    padding: 'medium',
    children: (
      <div style={{ 
        backgroundColor: '#e1f5fe', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #00bcd4'
      }}>
        Container with Medium Padding
      </div>
    ),
  },
};

export const LargePadding: Story = {
  args: {
    maxWidth: 'md',
    padding: 'large',
    children: (
      <div style={{ 
        backgroundColor: '#f1f8e9', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #8bc34a'
      }}>
        Container with Large Padding
      </div>
    ),
  },
};

// Fluid container
export const Fluid: Story = {
  args: {
    fluid: true,
    children: (
      <div style={{ 
        backgroundColor: '#fff8e1', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #ffc107'
      }}>
        Fluid Container (no max-width)
      </div>
    ),
  },
};

// Not centered
export const NotCentered: Story = {
  args: {
    maxWidth: 'md',
    center: false,
    children: (
      <div style={{ 
        backgroundColor: '#efebe9', 
        padding: '20px', 
        textAlign: 'center',
        border: '2px dashed #795548'
      }}>
        Not Centered Container
      </div>
    ),
  },
};

// Complex content
export const ComplexContent: Story = {
  args: {
    maxWidth: 'lg',
    padding: 'medium',
    children: (
      <div>
        <h2 style={{ marginTop: 0, color: '#333' }}>Container with Complex Content</h2>
        <p>This container demonstrates how content flows within different container sizes.</p>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '16px',
          marginTop: '20px'
        }}>
          <div style={{ backgroundColor: '#e3f2fd', padding: '16px', borderRadius: '8px' }}>
            <h3 style={{ marginTop: 0 }}>Card 1</h3>
            <p>This is a sample card within the container.</p>
          </div>
          <div style={{ backgroundColor: '#e8f5e8', padding: '16px', borderRadius: '8px' }}>
            <h3 style={{ marginTop: 0 }}>Card 2</h3>
            <p>Another sample card with different content.</p>
          </div>
          <div style={{ backgroundColor: '#fff3e0', padding: '16px', borderRadius: '8px' }}>
            <h3 style={{ marginTop: 0 }}>Card 3</h3>
            <p>A third card to show the grid layout.</p>
          </div>
        </div>
      </div>
    ),
  },
};

// All sizes showcase
export const AllSizes: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {['xs', 'sm', 'md', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl', '6xl', '7xl'].map((size) => (
        <Container key={size} maxWidth={size as any} padding="small">
          <div style={{ 
            backgroundColor: '#f5f5f5', 
            padding: '16px', 
            textAlign: 'center',
            borderRadius: '8px',
            border: '1px solid #ddd'
          }}>
            {size.toUpperCase()} Container
          </div>
        </Container>
      ))}
    </div>
  ),
  parameters: {
    layout: 'padded',
  },
};
