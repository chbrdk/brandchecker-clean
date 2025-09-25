import type { Meta, StoryObj } from '@storybook/react';
import { Avatar } from '../../components/atoms/Avatar';

const meta: Meta<typeof Avatar> = {
  title: 'Atoms/Avatar',
  component: Avatar,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof Avatar>;

export const Default: Story = {
  args: {
    initials: 'JD',
    size: 'md',
    shape: 'circle'
  }
};

export const WithImage: Story = {
  args: {
    src: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face',
    alt: 'John Doe',
    size: 'md',
    shape: 'circle'
  }
};

export const WithIcon: Story = {
  args: {
    iconName: 'info',
    size: 'md',
    shape: 'circle',
    backgroundColor: '#3b82f6'
  }
};

export const WithStatus: Story = {
  args: {
    initials: 'JD',
    size: 'md',
    shape: 'circle',
    status: 'online',
    backgroundColor: '#10b981'
  }
};
