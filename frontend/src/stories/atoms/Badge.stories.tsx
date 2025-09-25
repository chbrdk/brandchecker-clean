import type { Meta, StoryObj } from '@storybook/react';
import { Badge, NotificationBadge, StatusBadge } from '../../components/atoms/Badge';

const meta: Meta<typeof Badge> = {
  title: 'Atoms/Badge',
  component: Badge,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'A versatile badge component for displaying counts, status indicators, and notifications with various variants and types.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'primary', 'secondary', 'success', 'warning', 'error', 'info', 'neutral'],
      description: 'Badge visual variant',
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
      description: 'Badge size',
    },
    type: {
      control: 'select',
      options: ['count', 'status', 'notification', 'dot'],
      description: 'Badge type',
    },
    visible: {
      control: 'boolean',
      description: 'Whether the badge is visible',
    },
    maxCount: {
      control: 'number',
      description: 'Maximum count to display',
    },
    icon: {
      control: 'select',
      options: [
        'check', 'x', 'info', 'warning', 'error', 'success',
        'eye', 'color-palette', 'type', 'logo', 'analytics',
        'user', 'settings', 'star', 'heart', 'bookmark'
      ],
      description: 'Icon to display',
    },
    clickable: {
      control: 'boolean',
      description: 'Whether the badge is clickable',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Badge>;

export const Default: Story = {
  args: {
    children: 'Badge',
  },
};

export const CountBadges: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <Badge type="count" variant="primary">5</Badge>
      <Badge type="count" variant="success">12</Badge>
      <Badge type="count" variant="warning">3</Badge>
      <Badge type="count" variant="error">99+</Badge>
      <Badge type="count" variant="neutral">0</Badge>
    </div>
  ),
};

export const StatusBadges: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <Badge type="status" variant="success">Active</Badge>
      <Badge type="status" variant="warning">Pending</Badge>
      <Badge type="status" variant="error">Failed</Badge>
      <Badge type="status" variant="info">Processing</Badge>
      <Badge type="status" variant="neutral">Draft</Badge>
    </div>
  ),
};

export const NotificationBadges: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <Badge type="notification" variant="error">5</Badge>
      <Badge type="notification" variant="warning">12</Badge>
      <Badge type="notification" variant="info">3</Badge>
      <Badge type="notification" variant="primary">99+</Badge>
    </div>
  ),
};

export const DotBadges: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <Badge type="dot" variant="success" />
      <Badge type="dot" variant="warning" />
      <Badge type="dot" variant="error" />
      <Badge type="dot" variant="info" />
      <Badge type="dot" variant="primary" />
    </div>
  ),
};

export const WithIcons: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <Badge variant="success" icon="check">Approved</Badge>
      <Badge variant="warning" icon="warning">Review</Badge>
      <Badge variant="error" icon="x">Rejected</Badge>
      <Badge variant="info" icon="info">Info</Badge>
      <Badge variant="primary" icon="star">Featured</Badge>
    </div>
  ),
};

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <Badge size="small" variant="primary">Small</Badge>
      <Badge size="medium" variant="primary">Medium</Badge>
      <Badge size="large" variant="primary">Large</Badge>
    </div>
  ),
};

export const Clickable: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <Badge clickable onClick={() => alert('Clicked!')} variant="primary">Clickable</Badge>
      <Badge clickable onClick={() => alert('Clicked!')} variant="success" icon="check">With Icon</Badge>
      <Badge clickable onClick={() => alert('Clicked!')} type="count" variant="error">5</Badge>
    </div>
  ),
};

export const BrandAnalysis: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <Badge variant="success" icon="check">Compliant</Badge>
      <Badge variant="error" icon="x">Non-Compliant</Badge>
      <Badge variant="warning" icon="warning">Review Required</Badge>
      <Badge variant="info" icon="info">Pending Analysis</Badge>
      <Badge variant="primary" icon="analytics">Analysis Complete</Badge>
    </div>
  ),
};

export const NotificationBadgeComponent: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <NotificationBadge count={5} onClick={() => alert('Notifications clicked!')} />
      <NotificationBadge count={0} />
      <NotificationBadge count={150} maxCount={99} />
      <NotificationBadge count={12} visible={false} />
    </div>
  ),
};

export const StatusBadgeComponent: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <StatusBadge status="Approved" variant="success" icon="check" />
      <StatusBadge status="Pending" variant="warning" icon="clock" />
      <StatusBadge status="Failed" variant="error" icon="x" />
      <StatusBadge status="Processing" variant="info" icon="loading" />
      <StatusBadge status="Draft" variant="neutral" />
    </div>
  ),
};

export const InteractiveExample: Story = {
  render: () => {
    const [notifications, setNotifications] = React.useState(5);
    const [status, setStatus] = React.useState('active');

    const handleNotificationClick = () => {
      setNotifications(0);
      alert('Notifications cleared!');
    };

    const handleStatusClick = () => {
      const statuses = ['active', 'pending', 'completed', 'failed'];
      const currentIndex = statuses.indexOf(status);
      const nextStatus = statuses[(currentIndex + 1) % statuses.length];
      setStatus(nextStatus);
    };

    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <div>
          <h4>Notification Badge</h4>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <NotificationBadge 
              count={notifications} 
              onClick={handleNotificationClick}
            />
            <span>Click to clear notifications</span>
          </div>
        </div>

        <div>
          <h4>Status Badge</h4>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <StatusBadge 
              status={status} 
              variant={status === 'active' ? 'success' : status === 'pending' ? 'warning' : status === 'completed' ? 'info' : 'error'}
              clickable
              onClick={handleStatusClick}
            />
            <span>Click to change status</span>
          </div>
        </div>

        <div>
          <h4>Count Badges</h4>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <Badge type="count" variant="primary">5</Badge>
            <Badge type="count" variant="success">12</Badge>
            <Badge type="count" variant="warning">3</Badge>
            <Badge type="count" variant="error">99+</Badge>
          </div>
        </div>
      </div>
    );
  },
};

export const MaxCount: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <Badge type="count" variant="primary" maxCount={9}>5</Badge>
      <Badge type="count" variant="success" maxCount={9}>12</Badge>
      <Badge type="count" variant="warning" maxCount={9}>99</Badge>
      <Badge type="count" variant="error" maxCount={9}>150</Badge>
    </div>
  ),
};

export const Visibility: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <Badge visible={true} variant="primary">Visible</Badge>
      <Badge visible={false} variant="primary">Hidden</Badge>
      <Badge visible={true} variant="success">Always Visible</Badge>
    </div>
  ),
};
