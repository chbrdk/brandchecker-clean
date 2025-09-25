import type { Meta, StoryObj } from '@storybook/react';
import { useState } from 'react';
import { Modal } from '../../components/molecules';
import { Button } from '../../components/atoms/Button';

const meta: Meta<typeof Modal> = {
  title: 'Molecules/Modal',
  component: Modal,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'A versatile modal component with multiple variants, sizes, and accessibility features.',
      },
    },
  },
  argTypes: {
    isOpen: {
      control: 'boolean',
      description: 'Modal open state',
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large', 'fullscreen'],
      description: 'Modal size',
    },
    variant: {
      control: 'select',
      options: ['default', 'confirmation', 'alert'],
      description: 'Modal variant style',
    },
    showCloseButton: {
      control: 'boolean',
      description: 'Show close button',
    },
    closeOnOverlayClick: {
      control: 'boolean',
      description: 'Close when clicking overlay',
    },
    closeOnEscape: {
      control: 'boolean',
      description: 'Close when pressing escape',
    },
    title: {
      control: 'text',
      description: 'Modal title',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

// Helper component for interactive stories
const ModalWrapper = ({ children, ...props }: any) => {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div>
      <Button onClick={() => setIsOpen(true)}>
        Open Modal
      </Button>
      <Modal
        {...props}
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
      >
        {children}
      </Modal>
    </div>
  );
};

// Default story
export const Default: Story = {
  render: () => (
    <ModalWrapper title="Default Modal">
      <p>This is a default modal with some content.</p>
      <p>You can put any content here.</p>
    </ModalWrapper>
  ),
};

// With title
export const WithTitle: Story = {
  render: () => (
    <ModalWrapper title="Modal with Title">
      <p>This modal has a title and some content below it.</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
    </ModalWrapper>
  ),
};

// Sizes
export const Small: Story = {
  render: () => (
    <ModalWrapper title="Small Modal" size="small">
      <p>This is a small modal.</p>
      <p>Perfect for simple confirmations or short messages.</p>
    </ModalWrapper>
  ),
};

export const Medium: Story = {
  render: () => (
    <ModalWrapper title="Medium Modal" size="medium">
      <p>This is a medium modal.</p>
      <p>Good for forms and moderate amounts of content.</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
    </ModalWrapper>
  ),
};

export const Large: Story = {
  render: () => (
    <ModalWrapper title="Large Modal" size="large">
      <p>This is a large modal.</p>
      <p>Perfect for complex forms or detailed content.</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
      <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
    </ModalWrapper>
  ),
};

export const Fullscreen: Story = {
  render: () => (
    <ModalWrapper title="Fullscreen Modal" size="fullscreen">
      <p>This is a fullscreen modal.</p>
      <p>Perfect for complex workflows or detailed views.</p>
      <div style={{ height: '200px', background: '#f0f0f0', padding: '20px', margin: '20px 0' }}>
        <p>Content area with background</p>
      </div>
      <p>More content here...</p>
    </ModalWrapper>
  ),
};

// Variants
export const Confirmation: Story = {
  render: () => (
    <ModalWrapper title="Confirm Action" variant="confirmation">
      <p>Are you sure you want to delete this item?</p>
      <p>This action cannot be undone.</p>
    </ModalWrapper>
  ),
};

export const Alert: Story = {
  render: () => (
    <ModalWrapper title="Alert" variant="alert">
      <p>Something went wrong!</p>
      <p>Please try again or contact support if the problem persists.</p>
    </ModalWrapper>
  ),
};

// Without close button
export const WithoutCloseButton: Story = {
  render: () => (
    <ModalWrapper title="No Close Button" showCloseButton={false}>
      <p>This modal doesn't have a close button.</p>
      <p>You can only close it by clicking outside or pressing escape.</p>
    </ModalWrapper>
  ),
};

// With footer
export const WithFooter: Story = {
  render: () => (
    <ModalWrapper 
      title="Modal with Footer" 
      footer={
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button variant="secondary" onClick={() => {}}>
            Cancel
          </Button>
          <Button variant="primary" onClick={() => {}}>
            Save
          </Button>
        </div>
      }
    >
      <p>This modal has a footer with action buttons.</p>
      <p>Perfect for forms and confirmations.</p>
    </ModalWrapper>
  ),
};

// Long content
export const LongContent: Story = {
  render: () => (
    <ModalWrapper title="Long Content Modal">
      <h3>Section 1</h3>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
      
      <h3>Section 2</h3>
      <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
      
      <h3>Section 3</h3>
      <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
      
      <h3>Section 4</h3>
      <p>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
      
      <h3>Section 5</h3>
      <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.</p>
    </ModalWrapper>
  ),
};

// Form example
export const FormExample: Story = {
  render: () => (
    <ModalWrapper 
      title="Create New Item" 
      size="medium"
      footer={
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button variant="secondary" onClick={() => {}}>
            Cancel
          </Button>
          <Button variant="primary" onClick={() => {}}>
            Create
          </Button>
        </div>
      }
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
            Name
          </label>
          <input 
            type="text" 
            placeholder="Enter name"
            style={{ 
              width: '100%', 
              padding: '8px 12px', 
              border: '1px solid #ccc', 
              borderRadius: '4px' 
            }}
          />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
            Description
          </label>
          <textarea 
            placeholder="Enter description"
            rows={3}
            style={{ 
              width: '100%', 
              padding: '8px 12px', 
              border: '1px solid #ccc', 
              borderRadius: '4px',
              resize: 'vertical'
            }}
          />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
            Category
          </label>
          <select 
            style={{ 
              width: '100%', 
              padding: '8px 12px', 
              border: '1px solid #ccc', 
              borderRadius: '4px' 
            }}
          >
            <option>Select category</option>
            <option>Category 1</option>
            <option>Category 2</option>
            <option>Category 3</option>
          </select>
        </div>
      </div>
    </ModalWrapper>
  ),
};

// Interactive example
export const Interactive: Story = {
  render: () => {
    const [isOpen, setIsOpen] = useState(false);
    
    return (
      <div>
        <Button onClick={() => setIsOpen(true)}>
          Open Interactive Modal
        </Button>
        <Modal
          isOpen={isOpen}
          onClose={() => setIsOpen(false)}
          title="Interactive Modal"
          footer={
            <div style={{ display: 'flex', gap: '8px' }}>
              <Button variant="secondary" onClick={() => setIsOpen(false)}>
                Close
              </Button>
              <Button variant="primary" onClick={() => alert('Action performed!')}>
                Perform Action
              </Button>
            </div>
          }
        >
          <p>This is an interactive modal.</p>
          <p>Try clicking the buttons or pressing escape to close it.</p>
        </Modal>
      </div>
    );
  },
};

// All variants showcase
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', padding: '20px' }}>
      <h3>Modal Variants</h3>
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        <ModalWrapper title="Default Modal" size="small">
          <p>Default variant</p>
        </ModalWrapper>
        <ModalWrapper title="Confirmation Modal" variant="confirmation" size="small">
          <p>Confirmation variant</p>
        </ModalWrapper>
        <ModalWrapper title="Alert Modal" variant="alert" size="small">
          <p>Alert variant</p>
        </ModalWrapper>
      </div>
      
      <h3>Modal Sizes</h3>
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        <ModalWrapper title="Small" size="small">
          <p>Small size</p>
        </ModalWrapper>
        <ModalWrapper title="Medium" size="medium">
          <p>Medium size</p>
        </ModalWrapper>
        <ModalWrapper title="Large" size="large">
          <p>Large size</p>
        </ModalWrapper>
        <ModalWrapper title="Fullscreen" size="fullscreen">
          <p>Fullscreen size</p>
        </ModalWrapper>
      </div>
    </div>
  ),
  parameters: {
    layout: 'padded',
  },
};
