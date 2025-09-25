import type { Meta, StoryObj } from '@storybook/react';
import { Chart } from '../../components/atoms/Chart';

const meta: Meta<typeof Chart> = {
  title: 'Atoms/Chart',
  component: Chart,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Chart component with multiple chart types for data visualization.'
      }
    }
  },
  argTypes: {
    type: {
      control: 'select',
      options: ['bar', 'line', 'pie', 'doughnut', 'area', 'scatter'],
      description: 'Chart type'
    },
    title: {
      control: 'text',
      description: 'Chart title'
    },
    description: {
      control: 'text',
      description: 'Chart description'
    },
    data: {
      control: 'object',
      description: 'Chart data points'
    },
    width: {
      control: { type: 'range', min: 200, max: 800, step: 50 },
      description: 'Chart width'
    },
    height: {
      control: { type: 'range', min: 150, max: 600, step: 50 },
      description: 'Chart height'
    },
    showLegend: {
      control: 'boolean',
      description: 'Show legend'
    },
    showValues: {
      control: 'boolean',
      description: 'Show values'
    },
    showPercentage: {
      control: 'boolean',
      description: 'Show percentage'
    },
    colorScheme: {
      control: 'select',
      options: ['primary', 'success', 'warning', 'error', 'neutral', 'brand'],
      description: 'Color scheme'
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg', 'xl'],
      description: 'Chart size'
    },
    onDataPointClick: {
      action: 'data point clicked',
      description: 'Data point click handler'
    }
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof Chart>;

const brandData = [
  { label: 'Logo Usage', value: 85 },
  { label: 'Color Compliance', value: 92 },
  { label: 'Typography', value: 78 },
  { label: 'Spacing', value: 88 },
  { label: 'Imagery', value: 75 }
];

const brandElementsData = [
  { label: 'Primary Colors', value: 40 },
  { label: 'Secondary Colors', value: 25 },
  { label: 'Accent Colors', value: 20 },
  { label: 'Neutral Colors', value: 15 }
];

const trendData = [
  { label: 'Q1', value: 65 },
  { label: 'Q2', value: 72 },
  { label: 'Q3', value: 78 },
  { label: 'Q4', value: 85 }
];

export const BarChart: Story = {
  args: {
    type: 'bar',
    title: 'Brand Compliance Score',
    description: 'Overall brand adherence across different elements',
    data: brandData,
    showValues: true,
    showPercentage: true,
    colorScheme: 'primary',
    size: 'md'
  }
};

export const PieChart: Story = {
  args: {
    type: 'pie',
    title: 'Brand Color Distribution',
    description: 'Usage of different color categories',
    data: brandElementsData,
    showLegend: true,
    showPercentage: true,
    colorScheme: 'brand',
    size: 'md'
  }
};

export const DoughnutChart: Story = {
  args: {
    type: 'doughnut',
    title: 'Brand Elements',
    description: 'Distribution of brand elements',
    data: brandElementsData,
    showLegend: true,
    showPercentage: true,
    colorScheme: 'success',
    size: 'md'
  }
};

export const LineChart: Story = {
  args: {
    type: 'line',
    title: 'Brand Consistency Trend',
    description: 'Quarterly brand consistency improvement',
    data: trendData,
    showValues: true,
    colorScheme: 'success',
    size: 'md'
  }
};

export const WithLegend: Story = {
  args: {
    type: 'pie',
    title: 'Brand Analysis Results',
    data: brandElementsData,
    showLegend: true,
    showValues: true,
    colorScheme: 'primary',
    size: 'lg'
  }
};

export const InteractiveChart: Story = {
  args: {
    type: 'bar',
    title: 'Interactive Brand Metrics',
    description: 'Click on bars to see details',
    data: brandData,
    showValues: true,
    showPercentage: true,
    colorScheme: 'warning',
    size: 'md',
    onDataPointClick: (dataPoint, index) => {
      console.log(`Clicked on ${dataPoint.label}: ${dataPoint.value}`);
    }
  }
};

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <Chart 
        type="bar" 
        title="Small Chart" 
        data={brandData.slice(0, 3)} 
        size="sm" 
        showValues 
      />
      <Chart 
        type="bar" 
        title="Medium Chart" 
        data={brandData} 
        size="md" 
        showValues 
      />
      <Chart 
        type="bar" 
        title="Large Chart" 
        data={brandData} 
        size="lg" 
        showValues 
      />
    </div>
  )
};

export const ChartTypes: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '2rem', width: '800px' }}>
      <Chart 
        type="bar" 
        title="Bar Chart" 
        data={brandData.slice(0, 4)} 
        showValues 
        size="sm"
      />
      <Chart 
        type="pie" 
        title="Pie Chart" 
        data={brandElementsData} 
        showLegend 
        size="sm"
      />
      <Chart 
        type="line" 
        title="Line Chart" 
        data={trendData} 
        showValues 
        size="sm"
      />
      <Chart 
        type="doughnut" 
        title="Doughnut Chart" 
        data={brandElementsData} 
        showLegend 
        size="sm"
      />
    </div>
  )
};

export const ColorSchemes: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', width: '900px' }}>
      <Chart 
        type="pie" 
        title="Primary" 
        data={brandElementsData} 
        colorScheme="primary" 
        size="sm"
      />
      <Chart 
        type="pie" 
        title="Success" 
        data={brandElementsData} 
        colorScheme="success" 
        size="sm"
      />
      <Chart 
        type="pie" 
        title="Warning" 
        data={brandElementsData} 
        colorScheme="warning" 
        size="sm"
      />
      <Chart 
        type="pie" 
        title="Error" 
        data={brandElementsData} 
        colorScheme="error" 
        size="sm"
      />
      <Chart 
        type="pie" 
        title="Neutral" 
        data={brandElementsData} 
        colorScheme="neutral" 
        size="sm"
      />
      <Chart 
        type="pie" 
        title="Brand" 
        data={brandElementsData} 
        colorScheme="brand" 
        size="sm"
      />
    </div>
  )
};

export const BrandCheckerDashboard: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '2rem', width: '800px' }}>
      <Chart 
        type="bar" 
        title="Brand Compliance Overview" 
        description="Current compliance scores across all brand elements"
        data={brandData} 
        showValues 
        showPercentage 
        colorScheme="success"
        size="md"
      />
      <Chart 
        type="pie" 
        title="Brand Element Distribution" 
        description="How brand elements are distributed"
        data={brandElementsData} 
        showLegend 
        showPercentage 
        colorScheme="brand"
        size="md"
      />
      <Chart 
        type="line" 
        title="Consistency Trend" 
        description="Brand consistency improvement over time"
        data={trendData} 
        showValues 
        colorScheme="primary"
        size="md"
      />
      <Chart 
        type="doughnut" 
        title="Analysis Progress" 
        description="Current analysis completion status"
        data={[
          { label: 'Completed', value: 75 },
          { label: 'In Progress', value: 20 },
          { label: 'Pending', value: 5 }
        ]} 
        showLegend 
        showPercentage 
        colorScheme="warning"
        size="md"
      />
    </div>
  )
};
