import type { Meta, StoryObj } from '@storybook/react';
import { MetricCard } from '../../components/atoms/MetricCard';
import { Typography } from '../../components/atoms/Typography';

const meta: Meta<typeof MetricCard> = {
  title: 'Atoms/MetricCard',
  component: MetricCard,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Metric card component that displays different types of metrics in a unified card format.'
      }
    }
  },
  argTypes: {
    type: {
      control: 'select',
      options: ['score', 'traffic-light', 'progress', 'custom'],
      description: 'Type of metric to display'
    },
    title: {
      control: 'text',
      description: 'Metric title'
    },
    description: {
      control: 'text',
      description: 'Metric description'
    },
    value: {
      control: { type: 'range', min: 0, max: 100, step: 1 },
      description: 'Metric value'
    },
    max: {
      control: { type: 'number', min: 1, max: 1000 },
      description: 'Maximum value'
    },
    status: {
      control: 'select',
      options: ['success', 'warning', 'error'],
      description: 'Traffic light status'
    },
    progressVariant: {
      control: 'select',
      options: ['linear', 'circular'],
      description: 'Progress bar variant'
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'Card size'
    },
    color: {
      control: 'select',
      options: ['primary', 'success', 'warning', 'error'],
      description: 'Color variant'
    },
    showPercentage: {
      control: 'boolean',
      description: 'Show percentage'
    },
    iconName: {
      control: 'select',
      options: ['star', 'target', 'trending-up', 'check', 'x', 'info', 'alert-circle', undefined],
      description: 'Icon name'
    },
    onClick: {
      action: 'clicked',
      description: 'Click handler'
    }
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof MetricCard>;

export const ScoreMetric: Story = {
  args: {
    type: 'score',
    title: 'Brand Consistency',
    description: 'Overall brand adherence score across all materials',
    value: 85,
    showPercentage: true,
    iconName: 'star',
    size: 'md'
  }
};

export const TrafficLightMetric: Story = {
  args: {
    type: 'traffic-light',
    title: 'Color Usage',
    description: 'Brand color compliance status',
    status: 'warning',
    iconName: 'alert-circle',
    size: 'md'
  }
};

export const ProgressMetric: Story = {
  args: {
    type: 'progress',
    title: 'Analysis Progress',
    description: 'Current analysis completion status',
    value: 60,
    progressVariant: 'circular',
    showPercentage: true,
    iconName: 'trending-up',
    size: 'md'
  }
};

export const LinearProgress: Story = {
  args: {
    type: 'progress',
    title: 'Brand Analysis',
    description: 'Linear progress indicator',
    value: 75,
    progressVariant: 'linear',
    showPercentage: true,
    color: 'success',
    size: 'md'
  }
};

export const CustomMetric: Story = {
  args: {
    type: 'custom',
    title: 'Custom Metric',
    description: 'Custom metric with custom content',
    value: 0,
    iconName: 'info',
    size: 'md',
    children: (
      <div style={{ textAlign: 'center' }}>
        <Typography variant="h2" size="lg" weight="bold" color="primary">
          42
        </Typography>
        <Typography variant="caption" color="secondary">
          Custom Value
        </Typography>
      </div>
    )
  }
};

export const ClickableMetric: Story = {
  args: {
    type: 'score',
    title: 'Clickable Score',
    description: 'Click to view details',
    value: 92,
    showPercentage: true,
    iconName: 'target',
    color: 'success',
    size: 'lg',
    onClick: () => console.log('Metric clicked!')
  }
};

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
      <MetricCard 
        type="score" 
        title="Small" 
        value={75} 
        size="sm" 
        showPercentage 
      />
      <MetricCard 
        type="score" 
        title="Medium" 
        value={75} 
        size="md" 
        showPercentage 
      />
      <MetricCard 
        type="score" 
        title="Large" 
        value={75} 
        size="lg" 
        showPercentage 
      />
    </div>
  )
};

export const Types: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', width: '600px' }}>
      <MetricCard 
        type="score" 
        title="Score" 
        value={85} 
        showPercentage 
        iconName="star"
      />
      <MetricCard 
        type="traffic-light" 
        title="Status" 
        status="success" 
        iconName="check"
      />
      <MetricCard 
        type="progress" 
        title="Progress" 
        value={60} 
        progressVariant="linear" 
        showPercentage 
        iconName="trending-up"
      />
      <MetricCard 
        type="progress" 
        title="Circular" 
        value={75} 
        progressVariant="circular" 
        showPercentage 
        iconName="target"
      />
    </div>
  )
};

export const Colors: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', width: '600px' }}>
      <MetricCard 
        type="score" 
        title="Primary" 
        value={80} 
        color="primary" 
        showPercentage 
      />
      <MetricCard 
        type="score" 
        title="Success" 
        value={95} 
        color="success" 
        showPercentage 
      />
      <MetricCard 
        type="score" 
        title="Warning" 
        value={65} 
        color="warning" 
        showPercentage 
      />
      <MetricCard 
        type="score" 
        title="Error" 
        value={30} 
        color="error" 
        showPercentage 
      />
    </div>
  )
};

export const BrandCheckerMetrics: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', width: '900px' }}>
      <MetricCard 
        type="score" 
        title="Brand Consistency" 
        description="Overall adherence to brand guidelines"
        value={88} 
        color="success" 
        showPercentage 
        iconName="star"
      />
      <MetricCard 
        type="traffic-light" 
        title="Color Usage" 
        description="Brand color compliance"
        status="warning" 
        iconName="alert-circle"
      />
      <MetricCard 
        type="progress" 
        title="Analysis Progress" 
        description="Current analysis status"
        value={75} 
        progressVariant="circular" 
        showPercentage 
        color="primary"
        iconName="trending-up"
      />
    </div>
  )
};
