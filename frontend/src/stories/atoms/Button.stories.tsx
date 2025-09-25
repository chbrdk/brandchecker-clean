import type { Meta, StoryObj } from '@storybook/react';
import { Button } from '../../components/atoms/Button';

const meta: Meta<typeof Button> = {
  title: 'Atoms/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Enhanced Button component with Icon library integration, multiple variants, sizes, and states.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger', 'success', 'ghost', 'link'],
      description: 'Button variant style',
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
      description: 'Button size',
    },
    iconName: {
      control: 'select',
      options: [
        'plus', 'minus', 'edit', 'delete', 'save', 'download', 'upload',
        'search', 'filter', 'refresh', 'check', 'x', 'arrow-left', 'arrow-right',
        'heart', 'star', 'bookmark', 'share', 'copy', 'eye', 'settings'
      ],
      description: 'Icon name from icon library',
    },
    iconPosition: {
      control: 'select',
      options: ['left', 'right'],
      description: 'Icon position',
    },
    loading: {
      control: 'boolean',
      description: 'Loading state',
    },
    disabled: {
      control: 'boolean',
      description: 'Disabled state',
    },
    fullWidth: {
      control: 'boolean',
      description: 'Full width button',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Default: Story = {
  args: {
    children: 'Button',
    variant: 'primary',
    size: 'medium',
  },
};

export const WithIcon: Story = {
  args: {
    children: 'Save',
    iconName: 'save',
    iconPosition: 'left',
    variant: 'primary',
  },
};

export const IconOnly: Story = {
  args: {
    children: '',
    iconName: 'plus',
    variant: 'primary',
    size: 'medium',
  },
};

export const IconRight: Story = {
  args: {
    children: 'Download',
    iconName: 'download',
    iconPosition: 'right',
    variant: 'secondary',
  },
};

export const Loading: Story = {
  args: {
    children: 'Loading...',
    loading: true,
    variant: 'primary',
  },
};

export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        <Button variant="primary" iconName="save">Save</Button>
        <Button variant="secondary" iconName="edit">Edit</Button>
        <Button variant="danger" iconName="delete">Delete</Button>
        <Button variant="success" iconName="check">Success</Button>
        <Button variant="ghost" iconName="eye">View</Button>
        <Button variant="link" iconName="external-link">Link</Button>
      </div>
    </div>
  ),
};

export const AllSizes: Story = {
  render: () => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
      <Button size="small" iconName="plus">Small</Button>
      <Button size="medium" iconName="plus">Medium</Button>
      <Button size="large" iconName="plus">Large</Button>
    </div>
  ),
};

export const ActionButtons: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
      <Button variant="primary" iconName="plus">Add Item</Button>
      <Button variant="secondary" iconName="edit">Edit</Button>
      <Button variant="secondary" iconName="copy">Copy</Button>
      <Button variant="secondary" iconName="share">Share</Button>
      <Button variant="danger" iconName="delete">Delete</Button>
    </div>
  ),
};

export const NavigationButtons: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
      <Button variant="ghost" iconName="arrow-left">Back</Button>
      <Button variant="ghost" iconName="arrow-right">Next</Button>
      <Button variant="ghost" iconName="home">Home</Button>
      <Button variant="ghost" iconName="settings">Settings</Button>
    </div>
  ),
};

export const StatusButtons: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
      <Button variant="success" iconName="check">Approved</Button>
      <Button variant="danger" iconName="x">Rejected</Button>
      <Button variant="secondary" iconName="warning">Warning</Button>
      <Button variant="secondary" iconName="info">Info</Button>
    </div>
  ),
};

export const FileActions: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
      <Button variant="primary" iconName="upload">Upload</Button>
      <Button variant="secondary" iconName="download">Download</Button>
      <Button variant="secondary" iconName="file">View File</Button>
      <Button variant="secondary" iconName="folder">Open Folder</Button>
    </div>
  ),
};

export const BrandActions: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
      <Button variant="primary" iconName="eye">Analyze</Button>
      <Button variant="secondary" iconName="color-palette">Colors</Button>
      <Button variant="secondary" iconName="type">Typography</Button>
      <Button variant="secondary" iconName="logo">Logo</Button>
      <Button variant="secondary" iconName="analytics">Analytics</Button>
    </div>
  ),
};

export const DisabledStates: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
      <Button disabled iconName="save">Disabled</Button>
      <Button disabled iconName="edit">Disabled Edit</Button>
      <Button loading iconName="refresh">Loading</Button>
    </div>
  ),
};

export const FullWidth: Story = {
  render: () => (
    <div style={{ width: '300px' }}>
      <Button fullWidth iconName="save">Full Width Button</Button>
    </div>
  ),
};