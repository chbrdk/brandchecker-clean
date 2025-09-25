import type { Meta, StoryObj } from '@storybook/react';
import { Score } from '../../components/atoms/Score';

const meta: Meta<typeof Score> = {
  title: 'Atoms/Score',
  component: Score,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Score component for displaying numerical values with color coding and optional labels.'
      }
    }
  },
  argTypes: {
    value: {
      control: { type: 'range', min: 0, max: 100, step: 1 },
      description: 'Score value (0-100)'
    },
    max: {
      control: { type: 'number', min: 1, max: 1000 },
      description: 'Maximum score'
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg', 'xl'],
      description: 'Score size'
    },
    showLabel: {
      control: 'boolean',
      description: 'Show label'
    },
    showPercentage: {
      control: 'boolean',
      description: 'Show percentage instead of value'
    },
    iconName: {
      control: 'select',
      options: ['star', 'target', 'trending-up', 'check-circle', 'alert-circle', 'info'],
      description: 'Icon name'
    }
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof Score>;

export const Default: Story = {
  args: {
    value: 85,
    label: 'Brand Consistency',
    size: 'md'
  }
};

export const Excellent: Story = {
  args: {
    value: 95,
    label: 'Typography Score',
    size: 'lg',
    iconName: 'check-circle'
  }
};

export const Fair: Story = {
  args: {
    value: 72,
    label: 'Color Usage',
    size: 'md',
    iconName: 'info'
  }
};

export const Poor: Story = {
  args: {
    value: 35,
    label: 'Layout Consistency',
    size: 'md',
    iconName: 'alert-circle'
  }
};

export const WithPercentage: Story = {
  args: {
    value: 87,
    label: 'Overall Score',
    size: 'lg',
    showPercentage: true,
    iconName: 'star'
  }
};

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
      <Score value={85} label="Small" size="sm" />
      <Score value={85} label="Medium" size="md" />
      <Score value={85} label="Large" size="lg" />
      <Score value={85} label="Extra Large" size="xl" />
    </div>
  )
};

export const ScoreRange: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
      <Score value={25} label="Poor" size="md" />
      <Score value={45} label="Below Average" size="md" />
      <Score value={65} label="Fair" size="md" />
      <Score value={85} label="Good" size="md" />
      <Score value={95} label="Excellent" size="md" />
    </div>
  )
};

export const WithoutLabel: Story = {
  args: {
    value: 78,
    size: 'lg',
    showLabel: false,
    iconName: 'target'
  }
};
