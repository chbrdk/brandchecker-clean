import type { Meta, StoryObj } from '@storybook/react';
import { 
  Header, 
  HeaderBrand, 
  HeaderNavigation, 
  HeaderActions, 
  NavItem, 
  Breadcrumb 
} from '../../components/organisms';
import { Button } from '../../components/atoms/Button';
import { Input } from '../../components/atoms/Input';
import { Badge } from '../../components/atoms/Badge';

const meta: Meta<typeof Header> = {
  title: 'Organisms/Header',
  component: Header,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Responsive header component with mobile-first navigation, brand integration, and flexible actions.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'transparent', 'elevated'],
      description: 'Header variant style',
    },
    fixed: {
      control: 'boolean',
      description: 'Fixed header position',
    },
    height: {
      control: 'select',
      options: ['xs', 'sm', 'md', 'lg', 'xl'],
      description: 'Header height',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

// Helper component for demo content
const DemoContent = () => (
  <div style={{ 
    padding: '40px 20px', 
    textAlign: 'center',
    backgroundColor: '#f9fafb',
    minHeight: '400px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'column',
    gap: '20px'
  }}>
    <h2 style={{ margin: 0, color: '#1f2937' }}>Page Content</h2>
    <p style={{ margin: 0, color: '#6b7280' }}>
      This is the main content area. Resize your browser to see responsive behavior.
    </p>
  </div>
);

// Basic Header
export const Default: Story = {
  render: () => (
    <div>
      <Header>
        <HeaderBrand 
          title="BrandChecker" 
          subtitle="Brand Analysis Platform"
        />
        <HeaderNavigation>
          <NavItem href="#" active>Dashboard</NavItem>
          <NavItem href="#">Analysis</NavItem>
          <NavItem href="#">Documents</NavItem>
          <NavItem href="#">Settings</NavItem>
        </HeaderNavigation>
        <HeaderActions>
          <Button variant="secondary" size="small">Login</Button>
        </HeaderActions>
      </Header>
      <DemoContent />
    </div>
  ),
};

export const WithBadges: Story = {
  render: () => (
    <div>
      <Header>
        <HeaderBrand>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ width: '32px', height: '32px', backgroundColor: '#0ea5e9', borderRadius: '4px' }} />
            <span style={{ fontWeight: '600', fontSize: '18px' }}>BrandChecker</span>
          </div>
        </HeaderBrand>
        <HeaderNavigation>
          <NavItem href="#" active>Dashboard</NavItem>
          <NavItem href="#" badge={5} badgeVariant="primary" badgeType="count">Analysis</NavItem>
          <NavItem href="#" badge="New" badgeVariant="success" badgeType="status">Documents</NavItem>
          <NavItem href="#" badge={12} badgeVariant="error" badgeType="notification">Notifications</NavItem>
          <NavItem href="#">Settings</NavItem>
        </HeaderNavigation>
        <HeaderActions>
          <Button variant="secondary" size="small" iconName="user">Profile</Button>
          <Button variant="ghost" size="small" iconName="settings" />
        </HeaderActions>
      </Header>
      <DemoContent />
    </div>
  ),
};

