import type { Meta, StoryObj } from '@storybook/react';
import { BrandCheckerChat } from '../../components/templates/BrandCheckerChat';
import type { ChatMessage } from '../../components/templates/BrandCheckerChat';
import type { AnalysisResult } from '../../components/atoms/ResultCard';
import type { ChartDataPoint } from '../../components/atoms/Chart';
import type { RecommendationItem } from '../../components/atoms/RecommendationList';

const meta: Meta<typeof BrandCheckerChat> = {
  title: 'Templates/BrandCheckerChat',
  component: BrandCheckerChat,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'BrandChecker chat interface template with support for rich content messages and various BrandChecker workflows.'
      }
    }
  },
  argTypes: {
    initialMessages: {
      control: 'object',
      description: 'Initial messages to display in the chat.'
    },
    placeholder: {
      control: 'text',
      description: 'Placeholder text for the chat input.'
    },
    onSendMessage: {
      action: 'message sent',
      description: 'Callback function when a message is sent.'
    },
    onFilesUpload: {
      action: 'files uploaded',
      description: 'Callback function when files are uploaded.'
    }
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof BrandCheckerChat>;

// Sample Data
const sampleAnalysisResults: AnalysisResult[] = [
  {
    category: 'Logo Usage',
    score: 85,
    status: 'success',
    details: 'Logo placement and sizing follow brand guidelines correctly.'
  },
  {
    category: 'Color Compliance',
    score: 92,
    status: 'success',
    details: 'All colors match the approved brand palette.'
  },
  {
    category: 'Typography',
    score: 78,
    status: 'warning',
    details: 'Some text uses non-brand fonts. Consider updating to brand fonts.'
  },
  {
    category: 'Spacing & Layout',
    score: 88,
    status: 'success',
    details: 'Layout spacing follows brand guidelines consistently.'
  }
];

const sampleChartData: ChartDataPoint[] = [
  { label: 'Logo', value: 85 },
  { label: 'Colors', value: 92 },
  { label: 'Typography', value: 78 },
  { label: 'Spacing', value: 88 }
];

const sampleRecommendations: RecommendationItem[] = [
  {
    id: '1',
    title: 'Update Typography Guidelines',
    description: 'Review and update typography usage across all materials to ensure consistency.',
    priority: 'high',
    status: 'pending',
    category: 'Typography',
    tags: ['typography', 'guidelines', 'consistency'],
    estimatedTime: '2-3 hours',
    impact: 'high',
    createdAt: new Date('2024-01-15')
  },
  {
    id: '2',
    title: 'Standardize Color Usage',
    description: 'Ensure all materials use the approved brand color palette.',
    priority: 'critical',
    status: 'in-progress',
    category: 'Brand Colors',
    tags: ['colors', 'palette', 'standards'],
    estimatedTime: '1-2 hours',
    impact: 'high',
    createdAt: new Date('2024-01-17')
  }
];

// Empty Chat - Initial State
export const EmptyChat: Story = {
  args: {
    initialMessages: [],
    placeholder: 'Ask about your brand...'
  }
};

// Welcome Message
const welcomeMessages: ChatMessage[] = [
  {
    id: 'welcome-1',
    message: 'Hello! I\'m your BrandChecker AI assistant. I can help you analyze your brand consistency and provide actionable recommendations.',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(Date.now() - 60000)
  },
  {
    id: 'welcome-2',
    message: 'You can upload brand files, ask questions about brand guidelines, or request a comprehensive brand analysis. How can I help you today?',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(Date.now() - 50000)
  }
];

export const WelcomeChat: Story = {
  args: {
    initialMessages: welcomeMessages,
    placeholder: 'Ask about your brand...'
  }
};

// File Upload Conversation
const fileUploadMessages: ChatMessage[] = [
  {
    id: 'user-1',
    message: 'Hi! I need help analyzing my brand materials.',
    sender: 'user',
    senderName: 'You',
    avatarInitials: 'U',
    timestamp: new Date(Date.now() - 300000)
  },
  {
    id: 'agent-1',
    message: 'Hello! I\'d be happy to help you analyze your brand materials. Please upload your brand files and I\'ll provide a comprehensive analysis.',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(Date.now() - 280000)
  },
  {
    id: 'user-2',
    message: 'Great! I\'ll upload my brand guidelines, logo files, and marketing materials.',
    sender: 'user',
    senderName: 'You',
    avatarInitials: 'U',
    timestamp: new Date(Date.now() - 260000)
  },
  {
    id: 'agent-2',
    message: 'Perfect! I\'ve received your files: brand-guidelines.pdf, logo-pack.zip, marketing-materials.zip. Let me analyze them now.',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(Date.now() - 240000)
  }
];

export const FileUploadChat: Story = {
  args: {
    initialMessages: fileUploadMessages,
    placeholder: 'Ask about your brand...'
  }
};

// Score Results Chat
const scoreResultsMessages: ChatMessage[] = [
  ...fileUploadMessages,
  {
    id: 'agent-3',
    message: 'Analysis complete! Here\'s your overall brand consistency score:',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(Date.now() - 180000),
    messageType: 'score',
    messageData: {
      type: 'score',
      content: {
        value: 82,
        label: 'Brand Consistency Score',
        showPercentage: true,
        iconName: 'star'
      }
    }
  },
  {
    id: 'agent-4',
    message: 'Your brand shows strong consistency overall! There are a few areas where we can make improvements. Would you like to see the detailed breakdown?',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(Date.now() - 160000)
  }
];

export const ScoreResultsChat: Story = {
  args: {
    initialMessages: scoreResultsMessages,
    placeholder: 'Ask about your brand...'
  }
};

// Detailed Analysis Chat
const detailedAnalysisMessages: ChatMessage[] = [
  ...scoreResultsMessages,
  {
    id: 'user-3',
    message: 'Yes, please show me the detailed breakdown!',
    sender: 'user',
    senderName: 'You',
    avatarInitials: 'U',
    timestamp: new Date(Date.now() - 140000)
  },
  {
    id: 'agent-5',
    message: 'Here\'s a detailed analysis of each brand element:',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(Date.now() - 120000),
    messageType: 'analysis',
    messageData: {
      type: 'analysis',
      content: {
        title: 'Brand Element Analysis',
        status: 'success',
        results: sampleAnalysisResults
      }
    }
  }
];

export const DetailedAnalysisChat: Story = {
  args: {
    initialMessages: detailedAnalysisMessages,
    placeholder: 'Ask about your brand...'
  }
};

// Chart Visualization Chat
const chartVisualizationMessages: ChatMessage[] = [
  ...detailedAnalysisMessages,
  {
    id: 'user-4',
    message: 'Can you show me this data in a chart format?',
    sender: 'user',
    senderName: 'You',
    avatarInitials: 'U',
    timestamp: new Date(Date.now() - 100000)
  },
  {
    id: 'agent-6',
    message: 'Absolutely! Here\'s a visual comparison of your brand element scores:',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(Date.now() - 80000),
    messageType: 'chart',
    messageData: {
      type: 'chart',
      content: {
        type: 'bar',
        title: 'Brand Element Scores',
        data: sampleChartData,
        showLegend: true,
        showValues: true
      }
    }
  }
];

export const ChartVisualizationChat: Story = {
  args: {
    initialMessages: chartVisualizationMessages,
    placeholder: 'Ask about your brand...'
  }
};

// Recommendations Chat
const recommendationsMessages: ChatMessage[] = [
  ...chartVisualizationMessages,
  {
    id: 'user-5',
    message: 'What specific actions should I take to improve my brand consistency?',
    sender: 'user',
    senderName: 'You',
    avatarInitials: 'U',
    timestamp: new Date(Date.now() - 40000)
  },
  {
    id: 'agent-8',
    message: 'Based on my analysis, here are my prioritized recommendations:',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(Date.now() - 20000),
    messageType: 'recommendations',
    messageData: {
      type: 'recommendations',
      content: {
        title: 'Improvement Recommendations',
        recommendations: sampleRecommendations,
        showPriority: true,
        showStatus: true,
        showTags: true,
        showEstimatedTime: true,
        maxItems: 2
      }
    }
  }
];

export const RecommendationsChat: Story = {
  args: {
    initialMessages: recommendationsMessages,
    placeholder: 'Ask about your brand...'
  }
};

// Complete Analysis Chat with Result Card
const completeAnalysisMessages: ChatMessage[] = [
  ...recommendationsMessages,
  {
    id: 'user-6',
    message: 'Can you provide a complete summary of my brand analysis?',
    sender: 'user',
    senderName: 'You',
    avatarInitials: 'U',
    timestamp: new Date(Date.now() - 10000)
  },
  {
    id: 'agent-9',
    message: 'Here\'s your comprehensive brand analysis summary:',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(),
        messageType: 'result-card',
        messageData: {
          type: 'result-card',
          content: {
            type: 'summary',
            variant: 'full-width',
            title: 'Brand Analysis Summary',
            description: 'Complete overview of your brand consistency analysis',
            score: 82,
            status: 'success',
            analysisResults: sampleAnalysisResults,
            chartData: sampleChartData,
            recommendations: sampleRecommendations,
            iconName: 'target',
            showScore: true,
            showStatus: true,
            showChart: true,
            showRecommendations: true,
            showDetails: true
          }
        }
  }
];

export const CompleteAnalysisChat: Story = {
  args: {
    initialMessages: completeAnalysisMessages,
    placeholder: 'Ask about your brand...'
  }
};

// Quick Questions Chat
const quickQuestionsMessages: ChatMessage[] = [
  {
    id: 'user-q1',
    message: 'What are the key elements of brand consistency?',
    sender: 'user',
    senderName: 'You',
    avatarInitials: 'U',
    timestamp: new Date(Date.now() - 200000)
  },
  {
    id: 'agent-q1',
    message: 'Great question! The key elements of brand consistency include:\n\n1. **Logo Usage** - Consistent placement, sizing, and clear space\n2. **Color Palette** - Using approved brand colors consistently\n3. **Typography** - Consistent font choices and hierarchy\n4. **Tone of Voice** - Consistent messaging and communication style\n5. **Visual Style** - Consistent imagery, graphics, and layout principles',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(Date.now() - 180000)
  },
  {
    id: 'user-q2',
    message: 'How often should I review my brand consistency?',
    sender: 'user',
    senderName: 'You',
    avatarInitials: 'U',
    timestamp: new Date(Date.now() - 160000)
  },
  {
    id: 'agent-q2',
    message: 'I recommend reviewing your brand consistency:\n\n• **Monthly** - Quick checks on new materials\n• **Quarterly** - Comprehensive brand audit\n• **Annually** - Full brand guideline review and updates\n• **When launching new campaigns** - Ensure alignment with brand standards\n\nRegular monitoring helps maintain consistency and catch issues early!',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(Date.now() - 140000)
  }
];

export const QuickQuestionsChat: Story = {
  args: {
    initialMessages: quickQuestionsMessages,
    placeholder: 'Ask about your brand...'
  }
};

// Interactive Demo
export const InteractiveDemo: Story = {
  args: {
    initialMessages: welcomeMessages,
    placeholder: 'Try asking: "Analyze my brand" or "Show me recommendations"',
    onSendMessage: (message: string) => {
      console.log('Demo message sent:', message);
    },
    onFilesUpload: (files: File[]) => {
      console.log('Demo files uploaded:', files.map(f => f.name));
    }
  }
};
