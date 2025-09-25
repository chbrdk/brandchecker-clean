import type { Meta, StoryObj } from '@storybook/react';
import { 
  ColorSwatch, 
  ColorPalette, 
  ColorPicker, 
  BrandColor
} from '../../components/atoms/Color';
import { useState } from 'react';

const meta: Meta<typeof ColorSwatch> = {
  title: 'Atoms/Color',
  component: ColorSwatch,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'A comprehensive color system with swatches, palettes, pickers, and brand colors.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'success', 'warning', 'error', 'info', 'neutral', 'brand', 'grey', 'black', 'white'],
      description: 'Color variant',
    },
    shade: {
      control: 'select',
      options: ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'],
      description: 'Color shade',
    },
    type: {
      control: 'select',
      options: ['background', 'text', 'border', 'accent'],
      description: 'Color type',
    },
    showName: {
      control: 'boolean',
      description: 'Whether to show color name',
    },
    showValue: {
      control: 'boolean',
      description: 'Whether to show color value',
    },
    showCode: {
      control: 'boolean',
      description: 'Whether to show color code',
    },
    customColor: {
      control: 'color',
      description: 'Custom color value',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof ColorSwatch>;

export const Default: Story = {
  args: {
    variant: 'primary',
    shade: '500',
    showName: true,
  },
};

export const ColorSwatches: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
      <ColorSwatch variant="primary" shade="500" showName showValue showCode />
      <ColorSwatch variant="secondary" shade="500" showName showValue showCode />
      <ColorSwatch variant="success" shade="500" showName showValue showCode />
      <ColorSwatch variant="warning" shade="500" showName showValue showCode />
      <ColorSwatch variant="error" shade="500" showName showValue showCode />
      <ColorSwatch variant="info" shade="500" showName showValue showCode />
      <ColorSwatch variant="grey" shade="500" showName showValue showCode />
      <ColorSwatch variant="black" showName showValue showCode />
      <ColorSwatch variant="white" showName showValue showCode />
    </div>
  ),
};

export const ColorShades: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
      <ColorSwatch variant="primary" shade="50" showName />
      <ColorSwatch variant="primary" shade="100" showName />
      <ColorSwatch variant="primary" shade="200" showName />
      <ColorSwatch variant="primary" shade="300" showName />
      <ColorSwatch variant="primary" shade="400" showName />
      <ColorSwatch variant="primary" shade="500" showName />
      <ColorSwatch variant="primary" shade="600" showName />
      <ColorSwatch variant="primary" shade="700" showName />
      <ColorSwatch variant="primary" shade="800" showName />
      <ColorSwatch variant="primary" shade="900" showName />
    </div>
  ),
};

export const CustomColors: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
      <ColorSwatch customColor="#ff6b6b" showName showValue showCode />
      <ColorSwatch customColor="#4ecdc4" showName showValue showCode />
      <ColorSwatch customColor="#45b7d1" showName showValue showCode />
      <ColorSwatch customColor="#96ceb4" showName showValue showCode />
      <ColorSwatch customColor="#feca57" showName showValue showCode />
      <ColorSwatch customColor="#ff9ff3" showName showValue showCode />
    </div>
  ),
};

export const ColorPalettes: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      <ColorPalette variant="primary" showNames showValues showCodes />
      <ColorPalette variant="success" showNames showValues />
      <ColorPalette variant="warning" showNames />
      <ColorPalette variant="error" showNames />
      <ColorPalette variant="grey" showNames />
    </div>
  ),
};

export const ColorPickerComponent: Story = {
  render: () => {
    const [selectedColor, setSelectedColor] = useState('#3b82f6');
    
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div>
          <h3>Selected Color: {selectedColor}</h3>
          <div 
            style={{ 
              width: '100px', 
              height: '50px', 
              backgroundColor: selectedColor, 
              border: '1px solid #ccc',
              borderRadius: '4px'
            }} 
          />
        </div>
        <ColorPicker 
          value={selectedColor} 
          onChange={setSelectedColor}
          showCustom={true}
        />
      </div>
    );
  },
};

export const BrandColors: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
      <BrandColor type="primary" showInfo />
      <BrandColor type="secondary" showInfo />
      <BrandColor type="accent" showInfo />
      <BrandColor type="neutral" showInfo />
    </div>
  ),
};

export const InteractiveColorPicker: Story = {
  render: () => {
    const [selectedColor, setSelectedColor] = useState('#3b82f6');
    const [customColors, setCustomColors] = useState([
      '#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'
    ]);

    const addCustomColor = (color: string) => {
      if (!customColors.includes(color)) {
        setCustomColors([...customColors, color]);
      }
    };

    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <div>
          <h3>Selected Color: {selectedColor}</h3>
          <div 
            style={{ 
              width: '200px', 
              height: '100px', 
              backgroundColor: selectedColor, 
              border: '1px solid #ccc',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '18px',
              fontWeight: 'bold',
              textShadow: '0 0 4px rgba(0,0,0,0.5)'
            }} 
          >
            {selectedColor}
          </div>
        </div>

        <div>
          <h4>Color Picker</h4>
          <ColorPicker 
            value={selectedColor} 
            onChange={setSelectedColor}
            colors={customColors}
            showCustom={true}
          />
        </div>

        <div>
          <h4>Color Swatch</h4>
          <ColorSwatch 
            customColor={selectedColor}
            showName
            showValue
            showCode
          />
        </div>
      </div>
    );
  },
};

export const GreyBlackWhite: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h3>Grey Shades</h3>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          <ColorSwatch variant="grey" shade="50" showName />
          <ColorSwatch variant="grey" shade="100" showName />
          <ColorSwatch variant="grey" shade="200" showName />
          <ColorSwatch variant="grey" shade="300" showName />
          <ColorSwatch variant="grey" shade="400" showName />
          <ColorSwatch variant="grey" shade="500" showName />
          <ColorSwatch variant="grey" shade="600" showName />
          <ColorSwatch variant="grey" shade="700" showName />
          <ColorSwatch variant="grey" shade="800" showName />
          <ColorSwatch variant="grey" shade="900" showName />
        </div>
      </div>
      
      <div>
        <h3>Black & White</h3>
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          <ColorSwatch variant="black" showName showValue showCode />
          <ColorSwatch variant="white" showName showValue showCode />
        </div>
      </div>
    </div>
  ),
};

export const ColorSystemOverview: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      <div>
        <h2>Primary Colors</h2>
        <ColorPalette variant="primary" showNames />
      </div>
      
      <div>
        <h2>Success Colors</h2>
        <ColorPalette variant="success" showNames />
      </div>
      
      <div>
        <h2>Warning Colors</h2>
        <ColorPalette variant="warning" showNames />
      </div>
      
      <div>
        <h2>Error Colors</h2>
        <ColorPalette variant="error" showNames />
      </div>
      
      <div>
        <h2>Brand Colors</h2>
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          <BrandColor type="primary" showInfo />
          <BrandColor type="secondary" showInfo />
          <BrandColor type="accent" showInfo />
          <BrandColor type="neutral" showInfo />
        </div>
      </div>
    </div>
  ),
};
