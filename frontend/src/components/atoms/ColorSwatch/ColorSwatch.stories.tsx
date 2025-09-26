import type { Meta, StoryObj } from '@storybook/react';
import { ColorSwatch } from './ColorSwatch';
import type { ColorData } from './ColorSwatch';

const meta: Meta<typeof ColorSwatch> = {
  title: 'Atoms/ColorSwatch',
  component: ColorSwatch,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A color swatch component for displaying extracted PDF colors with detailed information including hex values, usage statistics, and RGB values.'
      }
    }
  },
  argTypes: {
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'Size variant of the color swatch'
    },
    showName: {
      control: 'boolean',
      description: 'Show color name'
    },
    showPercentage: {
      control: 'boolean',
      description: 'Show usage percentage'
    },
    showCount: {
      control: 'boolean',
      description: 'Show usage count'
    },
    showRgb: {
      control: 'boolean',
      description: 'Show RGB values'
    },
    showDescription: {
      control: 'boolean',
      description: 'Show color description'
    },
    onClick: {
      action: 'clicked',
      description: 'Click handler for the color swatch'
    }
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof ColorSwatch>;

// Sample color data
const sampleColor: ColorData = {
  hex: '#fdfefe',
  name: 'White',
  usage_percentage: 24.52,
  usage_count: 284743,
  rgb: [253, 254, 254],
  description: 'White color used 284743 times (24.5%) across 1 sources'
};

const sampleColors: ColorData[] = [
  {
    hex: '#fdfefe',
    name: 'White',
    usage_percentage: 24.52,
    usage_count: 284743,
    rgb: [253, 254, 254],
    description: 'White color used 284743 times (24.5%) across 1 sources'
  },
  {
    hex: '#86909f',
    name: 'Gray',
    usage_percentage: 10.47,
    usage_count: 121538,
    rgb: [134, 144, 159],
    description: 'Gray color used 121538 times (10.5%) across 1 sources'
  },
  {
    hex: '#fefefe',
    name: 'White',
    usage_percentage: 9.43,
    usage_count: 109389,
    rgb: [254, 254, 254],
    description: 'White color used 109389 times (9.4%) across 1 sources'
  },
  {
    hex: '#ff6b6b',
    name: 'Red',
    usage_percentage: 8.2,
    usage_count: 95234,
    rgb: [255, 107, 107],
    description: 'Red color used 95234 times (8.2%) across 1 sources'
  },
  {
    hex: '#4ecdc4',
    name: 'Teal',
    usage_percentage: 6.8,
    usage_count: 78912,
    rgb: [78, 205, 196],
    description: 'Teal color used 78912 times (6.8%) across 1 sources'
  }
];

export const Default: Story = {
  args: {
    color: sampleColor,
    size: 'md',
    showName: true,
    showPercentage: true,
    showCount: false,
    showRgb: false,
    showDescription: false
  }
};

export const Small: Story = {
  args: {
    color: sampleColor,
    size: 'sm',
    showName: true,
    showPercentage: true
  }
};

export const Large: Story = {
  args: {
    color: sampleColor,
    size: 'lg',
    showName: true,
    showPercentage: true,
    showCount: true,
    showRgb: true,
    showDescription: true
  }
};

export const WithAllDetails: Story = {
  args: {
    color: sampleColor,
    size: 'md',
    showName: true,
    showPercentage: true,
    showCount: true,
    showRgb: true,
    showDescription: true
  }
};

export const Minimal: Story = {
  args: {
    color: sampleColor,
    size: 'sm',
    showName: false,
    showPercentage: false,
    showCount: false,
    showRgb: false,
    showDescription: false
  }
};

export const Clickable: Story = {
  args: {
    color: sampleColor,
    size: 'md',
    showName: true,
    showPercentage: true,
    onClick: (color) => console.log('Color clicked:', color)
  }
};

export const ColorPalette: Story = {
  render: () => (
    <div style={{ 
      display: 'flex', 
      gap: 'var(--space-3)', 
      flexWrap: 'wrap',
      maxWidth: '800px'
    }}>
      {sampleColors.map((color, index) => (
        <ColorSwatch
          key={index}
          color={color}
          size="md"
          showName={true}
          showPercentage={true}
          showCount={false}
          showRgb={false}
          showDescription={false}
          onClick={(color) => console.log('Color clicked:', color)}
        />
      ))}
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'A palette of color swatches showing the top 5 colors from a PDF extraction.'
      }
    }
  }
};

export const ResponsiveGrid: Story = {
  render: () => (
    <div style={{ 
      display: 'grid', 
      gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
      gap: 'var(--space-3)',
      maxWidth: '600px'
    }}>
      {sampleColors.map((color, index) => (
        <ColorSwatch
          key={index}
          color={color}
          size="sm"
          showName={true}
          showPercentage={true}
          showCount={false}
          showRgb={false}
          showDescription={false}
        />
      ))}
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Color swatches in a responsive grid layout that adapts to different screen sizes.'
      }
    }
  }
};
