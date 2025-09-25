import type { Meta, StoryObj } from '@storybook/react';
import { Icon } from '../../components/atoms/Icon';
import type { IconName } from '../../components/atoms/Icon';

const meta: Meta<typeof Icon> = {
  title: 'Atoms/Icon',
  component: Icon,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A comprehensive icon library with over 60 icons for various use cases in the BrandChecker application.',
      },
    },
  },
  argTypes: {
    name: {
      control: 'select',
      options: [
        // Navigation & UI
        'chevron-down', 'chevron-up', 'chevron-left', 'chevron-right',
        'arrow-down', 'arrow-up', 'arrow-left', 'arrow-right',
        'menu', 'close', 'search', 'filter',
        
        // Actions
        'plus', 'minus', 'edit', 'delete', 'copy', 'share',
        'download', 'upload', 'refresh', 'save',
        
        // Status & Feedback
        'check', 'x', 'info', 'warning', 'error', 'success',
        'loading', 'star', 'heart', 'bookmark',
        
        // Files & Documents
        'file', 'file-text', 'folder', 'image', 'pdf',
        'document', 'page', 'attachment',
        
        // Brand & Analysis
        'eye', 'color-palette', 'type', 'layout', 'logo',
        'brand', 'analytics', 'chart', 'graph',
        
        // User & Account
        'user', 'users', 'profile', 'settings', 'gear',
        'login', 'logout', 'account',
        
        // Communication
        'mail', 'message', 'chat', 'phone', 'notification',
        
        // System
        'home', 'dashboard', 'database', 'server', 'cloud',
        'link', 'external-link', 'globe'
      ],
      description: 'Icon name from the icon library',
    },
    size: {
      control: 'select',
      options: ['xs', 'sm', 'md', 'lg', 'xl'],
      description: 'Icon size',
    },
    color: {
      control: 'color',
      description: 'Icon color',
    },
    title: {
      control: 'text',
      description: 'Icon title for accessibility',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Icon>;

export const Default: Story = {
  args: {
    name: 'search',
    size: 'md',
    color: 'currentColor',
    title: 'Search icon',
  },
};

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
      <Icon name="star" size="xs" title="Extra small" />
      <Icon name="star" size="sm" title="Small" />
      <Icon name="star" size="md" title="Medium" />
      <Icon name="star" size="lg" title="Large" />
      <Icon name="star" size="xl" title="Extra large" />
    </div>
  ),
};

export const Colors: Story = {
  render: () => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
      <Icon name="heart" color="#ef4444" title="Red heart" />
      <Icon name="heart" color="#10b981" title="Green heart" />
      <Icon name="heart" color="#3b82f6" title="Blue heart" />
      <Icon name="heart" color="#f59e0b" title="Yellow heart" />
      <Icon name="heart" color="#8b5cf6" title="Purple heart" />
    </div>
  ),
};

export const NavigationIcons: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', padding: '16px' }}>
      {(['chevron-down', 'chevron-up', 'chevron-left', 'chevron-right', 
         'arrow-down', 'arrow-up', 'arrow-left', 'arrow-right',
         'menu', 'close', 'search', 'filter'] as IconName[]).map((iconName) => (
        <div key={iconName} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          <Icon name={iconName} size="lg" />
          <span style={{ fontSize: '12px', color: '#6b7280' }}>{iconName}</span>
        </div>
      ))}
    </div>
  ),
};

export const ActionIcons: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', padding: '16px' }}>
      {(['plus', 'minus', 'edit', 'delete', 'copy', 'share',
         'download', 'upload', 'refresh', 'save'] as IconName[]).map((iconName) => (
        <div key={iconName} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          <Icon name={iconName} size="lg" />
          <span style={{ fontSize: '12px', color: '#6b7280' }}>{iconName}</span>
        </div>
      ))}
    </div>
  ),
};

export const StatusIcons: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', padding: '16px' }}>
      {(['check', 'x', 'info', 'warning', 'error', 'success',
         'loading', 'star', 'heart', 'bookmark'] as IconName[]).map((iconName) => (
        <div key={iconName} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          <Icon 
            name={iconName} 
            size="lg" 
            color={iconName === 'error' ? '#ef4444' : iconName === 'success' ? '#10b981' : iconName === 'warning' ? '#f59e0b' : 'currentColor'}
          />
          <span style={{ fontSize: '12px', color: '#6b7280' }}>{iconName}</span>
        </div>
      ))}
    </div>
  ),
};

export const FileIcons: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', padding: '16px' }}>
      {(['file', 'file-text', 'folder', 'image', 'pdf',
         'document', 'page', 'attachment'] as IconName[]).map((iconName) => (
        <div key={iconName} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          <Icon name={iconName} size="lg" />
          <span style={{ fontSize: '12px', color: '#6b7280' }}>{iconName}</span>
        </div>
      ))}
    </div>
  ),
};

export const BrandIcons: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', padding: '16px' }}>
      {(['eye', 'color-palette', 'type', 'layout', 'logo',
         'brand', 'analytics', 'chart', 'graph'] as IconName[]).map((iconName) => (
        <div key={iconName} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          <Icon name={iconName} size="lg" color="#1d4ed8" />
          <span style={{ fontSize: '12px', color: '#6b7280' }}>{iconName}</span>
        </div>
      ))}
    </div>
  ),
};

export const UserIcons: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', padding: '16px' }}>
      {(['user', 'users', 'profile', 'settings', 'gear',
         'login', 'logout', 'account'] as IconName[]).map((iconName) => (
        <div key={iconName} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          <Icon name={iconName} size="lg" />
          <span style={{ fontSize: '12px', color: '#6b7280' }}>{iconName}</span>
        </div>
      ))}
    </div>
  ),
};

export const CommunicationIcons: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', padding: '16px' }}>
      {(['mail', 'message', 'chat', 'phone', 'notification'] as IconName[]).map((iconName) => (
        <div key={iconName} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          <Icon name={iconName} size="lg" />
          <span style={{ fontSize: '12px', color: '#6b7280' }}>{iconName}</span>
        </div>
      ))}
    </div>
  ),
};

export const SystemIcons: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', padding: '16px' }}>
      {(['home', 'dashboard', 'database', 'server', 'cloud',
         'link', 'external-link', 'globe'] as IconName[]).map((iconName) => (
        <div key={iconName} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          <Icon name={iconName} size="lg" />
          <span style={{ fontSize: '12px', color: '#6b7280' }}>{iconName}</span>
        </div>
      ))}
    </div>
  ),
};

export const ClickableIcons: Story = {
  render: () => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
      <Icon 
        name="heart" 
        size="lg" 
        color="#ef4444" 
        onClick={() => alert('Heart clicked!')} 
        title="Click me!"
      />
      <Icon 
        name="star" 
        size="lg" 
        color="#f59e0b" 
        onClick={() => alert('Star clicked!')} 
        title="Click me!"
      />
      <Icon 
        name="bookmark" 
        size="lg" 
        color="#3b82f6" 
        onClick={() => alert('Bookmark clicked!')} 
        title="Click me!"
      />
    </div>
  ),
};

export const LoadingIcon: Story = {
  render: () => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
      <Icon name="loading" size="sm" className="icon--loading" />
      <Icon name="loading" size="md" className="icon--loading" />
      <Icon name="loading" size="lg" className="icon--loading" />
      <span style={{ color: '#6b7280' }}>Loading animations</span>
    </div>
  ),
};

export const AllIcons: Story = {
  render: () => {
    const allIcons: IconName[] = [
      // Navigation & UI
      'chevron-down', 'chevron-up', 'chevron-left', 'chevron-right',
      'arrow-down', 'arrow-up', 'arrow-left', 'arrow-right',
      'menu', 'close', 'search', 'filter',
      
      // Actions
      'plus', 'minus', 'edit', 'delete', 'copy', 'share',
      'download', 'upload', 'refresh', 'save',
      
      // Status & Feedback
      'check', 'x', 'info', 'warning', 'error', 'success',
      'loading', 'star', 'heart', 'bookmark',
      
      // Files & Documents
      'file', 'file-text', 'folder', 'image', 'pdf',
      'document', 'page', 'attachment',
      
      // Brand & Analysis
      'eye', 'color-palette', 'type', 'layout', 'logo',
      'brand', 'analytics', 'chart', 'graph',
      
      // User & Account
      'user', 'users', 'profile', 'settings', 'gear',
      'login', 'logout', 'account',
      
      // Communication
      'mail', 'message', 'chat', 'phone', 'notification',
      
      // System
      'home', 'dashboard', 'database', 'server', 'cloud',
      'link', 'external-link', 'globe'
    ];

    return (
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(8, 1fr)', gap: '16px', padding: '16px', maxWidth: '800px' }}>
        {allIcons.map((iconName) => (
          <div key={iconName} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px', padding: '8px' }}>
            <Icon name={iconName} size="md" />
            <span style={{ fontSize: '10px', color: '#6b7280', textAlign: 'center' }}>{iconName}</span>
          </div>
        ))}
      </div>
    );
  },
};
