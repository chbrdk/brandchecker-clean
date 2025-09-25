import type { Meta, StoryObj } from '@storybook/react';
import { ProgressBar } from '../../components/atoms/ProgressBar';

const meta: Meta<typeof ProgressBar> = {
  title: 'Atoms/ProgressBar',
  component: ProgressBar,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Progress bar component with linear and circular variants for displaying progress.'
      }
    }
  },
  argTypes: {
    value: {
      control: { type: 'range', min: 0, max: 100, step: 1 },
      description: 'Progress value (0-100)'
    },
    max: {
      control: { type: 'number', min: 1, max: 1000 },
      description: 'Maximum value'
    },
    variant: {
      control: 'select',
      options: ['linear', 'circular'],
      description: 'Progress bar variant'
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'Size variant'
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
    showLabel: {
      control: 'boolean',
      description: 'Show label'
    },
    label: {
      control: 'text',
      description: 'Custom label'
    }
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof ProgressBar>;

export const Linear: Story = {
  args: {
    value: 75,
    variant: 'linear',
    size: 'md',
    showPercentage: true
  }
};

export const Circular: Story = {
  args: {
    value: 60,
    variant: 'circular',
    size: 'md',
    showPercentage: true,
    label: 'Loading...'
  }
};

export const WithLabel: Story = {
  args: {
    value: 85,
    variant: 'linear',
    size: 'md',
    label: 'Brand Analysis Progress',
    showPercentage: true
  }
};

export const Success: Story = {
  args: {
    value: 95,
    variant: 'linear',
    size: 'md',
    color: 'success',
    showPercentage: true,
    label: 'Analysis Complete'
  }
};

export const Warning: Story = {
  args: {
    value: 45,
    variant: 'circular',
    size: 'lg',
    color: 'warning',
    showPercentage: true,
    label: 'Needs Attention'
  }
};

export const Error: Story = {
  args: {
    value: 20,
    variant: 'linear',
    size: 'md',
    color: 'error',
    showPercentage: true,
    label: 'Critical Issues Found'
  }
};

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '300px' }}>
      <ProgressBar value={75} variant="linear" size="sm" label="Small" showPercentage />
      <ProgressBar value={75} variant="linear" size="md" label="Medium" showPercentage />
      <ProgressBar value={75} variant="linear" size="lg" label="Large" showPercentage />
    </div>
  )
};

export const Variants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
      <ProgressBar value={75} variant="linear" size="md" showPercentage />
      <ProgressBar value={75} variant="circular" size="md" showPercentage />
    </div>
  )
};

export const Colors: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '300px' }}>
      <ProgressBar value={85} variant="linear" color="primary" label="Primary" showPercentage />
      <ProgressBar value={75} variant="linear" color="success" label="Success" showPercentage />
      <ProgressBar value={55} variant="linear" color="warning" label="Warning" showPercentage />
      <ProgressBar value={25} variant="linear" color="error" label="Error" showPercentage />
    </div>
  )
};

export const ProgressRange: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '300px' }}>
      <ProgressBar value={0} variant="linear" label="0%" showPercentage />
      <ProgressBar value={25} variant="linear" label="25%" showPercentage />
      <ProgressBar value={50} variant="linear" label="50%" showPercentage />
      <ProgressBar value={75} variant="linear" label="75%" showPercentage />
      <ProgressBar value={100} variant="linear" label="100%" showPercentage />
    </div>
  )
};
