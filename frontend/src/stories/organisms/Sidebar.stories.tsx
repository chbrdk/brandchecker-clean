import type { Meta, StoryObj } from '@storybook/react';
import { 
  Sidebar, 
  SidebarNavigation, 
  SidebarItem, 
  SidebarGroup, 
  SidebarFooter 
} from '../../components/organisms';
import { Button } from '../../components/atoms/Button';

const meta: Meta<typeof Sidebar> = {
  title: 'Organisms/Sidebar',
  component: Sidebar,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Responsive sidebar navigation component with mobile-first design, collapsible functionality, and flexible content organization.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'compact', 'floating'],
      description: 'Sidebar variant style',
    },
    width: {
      control: 'select',
      options: ['xs', 'sm', 'md', 'lg', 'xl'],
      description: 'Sidebar width',
    },
    collapsible: {
      control: 'boolean',
      description: 'Enable collapsible sidebar',
    },
    fixed: {
      control: 'boolean',
      description: 'Fixed sidebar position',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

// Helper component for demo content
const DemoContent = () => (
  <div style={{ 
    padding: '40px', 
    marginLeft: '320px', // Adjust for sidebar width
    backgroundColor: '#f9fafb',
    minHeight: '100vh'
  }}>
    <h2 style={{ margin: '0 0 20px 0', color: '#1f2937' }}>Main Content Area</h2>
    <p style={{ margin: 0, color: '#6b7280' }}>
      This is the main content area. The sidebar is positioned on the left side.
    </p>
  </div>
);

// Basic Sidebar
export const Default: Story = {
  render: () => (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar>
        <SidebarNavigation title="Navigation">
          <SidebarItem href="#" active icon="🏠">Dashboard</SidebarItem>
          <SidebarItem href="#" icon="📊">Analytics</SidebarItem>
          <SidebarItem href="#" icon="📄">Documents</SidebarItem>
          <SidebarItem href="#" icon="⚙️">Settings</SidebarItem>
        </SidebarNavigation>
      </Sidebar>
      <DemoContent />
    </div>
  ),
};

// BrandChecker Sidebar
export const BrandCheckerSidebar: Story = {
  render: () => (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar variant="default" width="lg">
        <SidebarNavigation title="BrandChecker">
          <SidebarItem href="#" active icon="📊">Dashboard</SidebarItem>
          <SidebarItem href="#" icon="🎨" badge="3">Color Analysis</SidebarItem>
          <SidebarItem href="#" icon="🔤">Font Analysis</SidebarItem>
          <SidebarItem href="#" icon="📷">Logo Detection</SidebarItem>
        </SidebarNavigation>
        
        <SidebarGroup title="Analysis Tools" collapsible>
          <SidebarItem href="#" icon="🔍">Brand Search</SidebarItem>
          <SidebarItem href="#" icon="📈">Reports</SidebarItem>
          <SidebarItem href="#" icon="⚡">Quick Scan</SidebarItem>
        </SidebarGroup>
        
        <SidebarGroup title="Documents" collapsible>
          <SidebarItem href="#" icon="📄" badge="12">PDF Files</SidebarItem>
          <SidebarItem href="#" icon="🖼️" badge="8">Images</SidebarItem>
          <SidebarItem href="#" icon="📋">Templates</SidebarItem>
        </SidebarGroup>
        
        <SidebarFooter>
          <SidebarItem href="#" icon="👤">Profile</SidebarItem>
          <SidebarItem href="#" icon="🔧">Settings</SidebarItem>
          <SidebarItem href="#" icon="🚪">Logout</SidebarItem>
        </SidebarFooter>
      </Sidebar>
      <DemoContent />
    </div>
  ),
};

// Collapsible Sidebar
export const Collapsible: Story = {
  render: () => (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar collapsible defaultCollapsed={false}>
        <SidebarNavigation title="Navigation">
          <SidebarItem href="#" active icon="🏠">Dashboard</SidebarItem>
          <SidebarItem href="#" icon="📊">Analytics</SidebarItem>
          <SidebarItem href="#" icon="📄">Documents</SidebarItem>
          <SidebarItem href="#" icon="⚙️">Settings</SidebarItem>
        </SidebarNavigation>
        
        <SidebarGroup title="Tools">
          <SidebarItem href="#" icon="🔍">Search</SidebarItem>
          <SidebarItem href="#" icon="📈">Reports</SidebarItem>
        </SidebarGroup>
        
        <SidebarFooter>
          <SidebarItem href="#" icon="👤">Profile</SidebarItem>
        </SidebarFooter>
      </Sidebar>
      <DemoContent />
    </div>
  ),
};

// Compact Sidebar
export const Compact: Story = {
  render: () => (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar variant="compact" width="sm">
        <SidebarNavigation>
          <SidebarItem href="#" active icon="🏠">Home</SidebarItem>
          <SidebarItem href="#" icon="📊">Stats</SidebarItem>
          <SidebarItem href="#" icon="📄">Files</SidebarItem>
          <SidebarItem href="#" icon="⚙️">Config</SidebarItem>
        </SidebarNavigation>
      </Sidebar>
      <DemoContent />
    </div>
  ),
};

// Floating Sidebar
export const Floating: Story = {
  render: () => (
    <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: '#f3f4f6' }}>
      <Sidebar variant="floating" width="md">
        <SidebarNavigation title="Menu">
          <SidebarItem href="#" active icon="🏠">Dashboard</SidebarItem>
          <SidebarItem href="#" icon="📊">Analytics</SidebarItem>
          <SidebarItem href="#" icon="📄">Documents</SidebarItem>
          <SidebarItem href="#" icon="⚙️">Settings</SidebarItem>
        </SidebarNavigation>
        
        <SidebarGroup title="Recent" collapsible defaultExpanded={false}>
          <SidebarItem href="#" icon="📄">Project A</SidebarItem>
          <SidebarItem href="#" icon="📄">Project B</SidebarItem>
        </SidebarGroup>
      </Sidebar>
      <DemoContent />
    </div>
  ),
};

// With Badges and Groups
export const WithBadgesAndGroups: Story = {
  render: () => (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar>
        <SidebarNavigation title="Main Menu">
          <SidebarItem href="#" active icon="🏠">Dashboard</SidebarItem>
          <SidebarItem href="#" icon="📊" badge="5">Analytics</SidebarItem>
          <SidebarItem href="#" icon="📄" badge="12">Documents</SidebarItem>
        </SidebarNavigation>
        
        <SidebarGroup title="Brand Analysis" collapsible>
          <SidebarItem href="#" icon="🎨" badge="new">Colors</SidebarItem>
          <SidebarItem href="#" icon="🔤">Typography</SidebarItem>
          <SidebarItem href="#" icon="📷">Logos</SidebarItem>
        </SidebarGroup>
        
        <SidebarGroup title="Tools" collapsible>
          <SidebarItem href="#" icon="🔍">Search</SidebarItem>
          <SidebarItem href="#" icon="📈">Reports</SidebarItem>
          <SidebarItem href="#" icon="⚡" badge="3">Quick Actions</SidebarItem>
        </SidebarGroup>
        
        <SidebarGroup title="Admin" collapsible defaultExpanded={false}>
          <SidebarItem href="#" icon="👥">Users</SidebarItem>
          <SidebarItem href="#" icon="🔐">Permissions</SidebarItem>
          <SidebarItem href="#" icon="⚙️">System</SidebarItem>
        </SidebarGroup>
        
        <SidebarFooter>
          <SidebarItem href="#" icon="💬" badge="2">Support</SidebarItem>
          <SidebarItem href="#" icon="👤">Profile</SidebarItem>
        </SidebarFooter>
      </Sidebar>
      <DemoContent />
    </div>
  ),
};

// Different Widths
export const DifferentWidths: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '20px', padding: '20px', backgroundColor: '#f3f4f6' }}>
      <div>
        <h4 style={{ marginBottom: '10px' }}>Extra Small (XS)</h4>
        <Sidebar width="xs" variant="floating" style={{ height: '300px' }}>
          <SidebarNavigation>
            <SidebarItem href="#" active icon="🏠">Home</SidebarItem>
            <SidebarItem href="#" icon="📊">Stats</SidebarItem>
          </SidebarNavigation>
        </Sidebar>
      </div>
      
      <div>
        <h4 style={{ marginBottom: '10px' }}>Small (SM)</h4>
        <Sidebar width="sm" variant="floating" style={{ height: '300px' }}>
          <SidebarNavigation>
            <SidebarItem href="#" active icon="🏠">Dashboard</SidebarItem>
            <SidebarItem href="#" icon="📊">Analytics</SidebarItem>
          </SidebarNavigation>
        </Sidebar>
      </div>
      
      <div>
        <h4 style={{ marginBottom: '10px' }}>Medium (MD) - Default</h4>
        <Sidebar width="md" variant="floating" style={{ height: '300px' }}>
          <SidebarNavigation>
            <SidebarItem href="#" active icon="🏠">Dashboard</SidebarItem>
            <SidebarItem href="#" icon="📊">Analytics</SidebarItem>
          </SidebarNavigation>
        </Sidebar>
      </div>
      
      <div>
        <h4 style={{ marginBottom: '10px' }}>Large (LG)</h4>
        <Sidebar width="lg" variant="floating" style={{ height: '300px' }}>
          <SidebarNavigation title="Navigation">
            <SidebarItem href="#" active icon="🏠">Dashboard</SidebarItem>
            <SidebarItem href="#" icon="📊">Analytics</SidebarItem>
          </SidebarNavigation>
        </Sidebar>
      </div>
    </div>
  ),
  parameters: {
    layout: 'padded',
  },
};

// Mobile Responsive
export const MobileResponsive: Story = {
  render: () => (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar>
        <SidebarNavigation title="Mobile Menu">
          <SidebarItem href="#" active icon="🏠">Dashboard</SidebarItem>
          <SidebarItem href="#" icon="📊">Analytics</SidebarItem>
          <SidebarItem href="#" icon="📄">Documents</SidebarItem>
          <SidebarItem href="#" icon="⚙️">Settings</SidebarItem>
        </SidebarNavigation>
        
        <SidebarFooter>
          <SidebarItem href="#" icon="👤">Profile</SidebarItem>
        </SidebarFooter>
      </Sidebar>
      <DemoContent />
    </div>
  ),
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};

// Complex Layout with Header
export const ComplexLayout: Story = {
  render: () => (
    <div style={{ minHeight: '100vh' }}>
      {/* Header */}
      <div style={{
        height: '64px',
        backgroundColor: '#1f2937',
        color: 'white',
        display: 'flex',
        alignItems: 'center',
        padding: '0 20px',
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 1000
      }}>
        <h1 style={{ margin: 0, fontSize: '20px' }}>BrandChecker Pro</h1>
        <div style={{ marginLeft: 'auto' }}>
          <Button variant="ghost" size="small" style={{ color: 'white' }}>Profile</Button>
        </div>
      </div>
      
      {/* Layout with Sidebar */}
      <div style={{ display: 'flex', paddingTop: '64px' }}>
        <Sidebar fixed variant="default" width="lg">
          <SidebarNavigation title="Main Navigation">
            <SidebarItem href="#" active icon="📊">Dashboard</SidebarItem>
            <SidebarItem href="#" icon="🎨" badge="5">Color Analysis</SidebarItem>
            <SidebarItem href="#" icon="🔤">Font Analysis</SidebarItem>
            <SidebarItem href="#" icon="📷">Logo Detection</SidebarItem>
            <SidebarItem href="#" icon="📄" badge="12">Documents</SidebarItem>
          </SidebarNavigation>
          
          <SidebarGroup title="Analysis Tools" collapsible>
            <SidebarItem href="#" icon="🔍">Brand Search</SidebarItem>
            <SidebarItem href="#" icon="📈">Reports</SidebarItem>
            <SidebarItem href="#" icon="⚡">Quick Scan</SidebarItem>
            <SidebarItem href="#" icon="🎯">Compliance Check</SidebarItem>
          </SidebarGroup>
          
          <SidebarGroup title="Recent Projects" collapsible defaultExpanded={false}>
            <SidebarItem href="#" icon="📁">Nike Brand Guide</SidebarItem>
            <SidebarItem href="#" icon="📁">Coca Cola Analysis</SidebarItem>
            <SidebarItem href="#" icon="📁">Apple Design System</SidebarItem>
          </SidebarGroup>
          
          <SidebarFooter>
            <SidebarItem href="#" icon="💬" badge="3">Support</SidebarItem>
            <SidebarItem href="#" icon="⚙️">Settings</SidebarItem>
            <SidebarItem href="#" icon="🚪">Logout</SidebarItem>
          </SidebarFooter>
        </Sidebar>
        
        {/* Main Content */}
        <div style={{ 
          flex: 1, 
          padding: '40px', 
          backgroundColor: '#f9fafb'
        }}>
          <h2 style={{ margin: '0 0 20px 0', color: '#1f2937' }}>Brand Analysis Dashboard</h2>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
            gap: '20px' 
          }}>
            <div style={{ 
              backgroundColor: 'white', 
              padding: '20px', 
              borderRadius: '8px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ margin: '0 0 10px 0' }}>Recent Analysis</h3>
              <p style={{ margin: 0, color: '#6b7280' }}>View your latest brand analysis results</p>
            </div>
            <div style={{ 
              backgroundColor: 'white', 
              padding: '20px', 
              borderRadius: '8px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ margin: '0 0 10px 0' }}>Quick Actions</h3>
              <p style={{ margin: 0, color: '#6b7280' }}>Start a new analysis or upload documents</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  ),
};

// Playground
export const Playground: Story = {
  args: {
    variant: 'default',
    width: 'md',
    collapsible: false,
    fixed: false,
  },
  render: (args) => (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar {...args}>
        <SidebarNavigation title="Navigation">
          <SidebarItem href="#" active icon="🏠">Dashboard</SidebarItem>
          <SidebarItem href="#" icon="📊">Analytics</SidebarItem>
          <SidebarItem href="#" icon="📄">Documents</SidebarItem>
          <SidebarItem href="#" icon="⚙️">Settings</SidebarItem>
        </SidebarNavigation>
      </Sidebar>
      <DemoContent />
    </div>
  ),
};
