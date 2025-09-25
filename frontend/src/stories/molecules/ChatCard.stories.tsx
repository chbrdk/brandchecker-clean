import type { Meta, StoryObj } from '@storybook/react';
import { ChatCard } from '../../components/molecules/ChatCard';
import type { AnalysisResult } from '../../components/atoms/ResultCard';
import type { ChartDataPoint } from '../../components/atoms/Chart';
import type { RecommendationItem } from '../../components/atoms/RecommendationList';

const meta: Meta<typeof ChatCard> = {
  title: 'Molecules/ChatCard',
  component: ChatCard,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A chat message card for displaying messages from a user or an agent, with support for rich content types including scores, analysis, charts, and recommendations.'
      }
    }
  },
  argTypes: {
    message: {
      control: 'text',
      description: 'The content of the chat message.'
    },
    sender: {
      control: 'select',
      options: ['user', 'agent'],
      description: 'The sender of the message (user or agent).'
    },
    senderName: {
      control: 'text',
      description: 'The name of the sender to display.'
    },
    avatarInitials: {
      control: 'text',
      description: 'Initials to display in the avatar if no image is provided.'
    },
    timestamp: {
      control: 'date',
      description: 'The timestamp of when the message was sent.'
    },
    messageType: {
      control: 'select',
      options: ['text', 'score', 'analysis', 'chart', 'recommendations', 'result-card'],
      description: 'The type of message content.'
    },
    messageData: {
      control: 'object',
      description: 'Rich content data for the message.'
    }
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof ChatCard>;

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
    description: 'Review and update typography usage across all materials.',
    priority: 'medium',
    status: 'pending',
    category: 'Typography',
    tags: ['typography', 'guidelines'],
    estimatedTime: '2-3 hours',
    impact: 'medium',
    createdAt: new Date('2024-01-15')
  },
  {
    id: '2',
    title: 'Improve Image Quality',
    description: 'Update low-resolution images with high-quality alternatives.',
    priority: 'low',
    status: 'pending',
    category: 'Visual Assets',
    tags: ['images', 'quality'],
    estimatedTime: '1-2 hours',
    impact: 'low',
    createdAt: new Date('2024-01-16')
  }
];

export const UserMessage: Story = {
  args: {
    message: 'Hello! Can you help me analyze my brand?',
    sender: 'user',
    senderName: 'John Doe',
    avatarInitials: 'JD',
    timestamp: new Date()
  }
};

export const AgentMessage: Story = {
  args: {
    message: 'Hello! I\'d be happy to help you analyze your brand.',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date()
  }
};

export const ScoreMessage: Story = {
  args: {
    message: 'Here\'s your brand consistency score:',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(),
    messageType: 'score',
    messageData: {
      type: 'score',
      content: {
        value: 85,
        label: 'Brand Consistency',
        showPercentage: true,
        iconName: 'star'
      }
    }
  }
};

export const AnalysisMessage: Story = {
  args: {
    message: 'Here\'s a detailed analysis of your brand elements:',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(),
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
};

export const ChartMessage: Story = {
  args: {
    message: 'Here\'s a comparison of your brand elements:',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(),
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
};

export const RecommendationsMessage: Story = {
  args: {
    message: 'Here are my recommendations for improving your brand:',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(),
    messageType: 'recommendations',
    messageData: {
      type: 'recommendations',
      content: {
        title: 'Improvement Recommendations',
        recommendations: sampleRecommendations,
        showPriority: true,
        showStatus: true,
        showTags: true,
        maxItems: 3
      }
    }
  }
};

export const ResultCardMessage: Story = {
  args: {
    message: 'Here\'s a comprehensive summary of your brand analysis:',
    sender: 'agent',
    senderName: 'BrandChecker AI',
    avatarInitials: 'AI',
    timestamp: new Date(),
    messageType: 'result-card',
    messageData: {
      type: 'result-card',
      content: {
        type: 'summary',
        title: 'Brand Analysis Summary',
        description: 'Complete overview of your brand consistency',
        score: 85,
        status: 'success',
        analysisResults: sampleAnalysisResults.slice(0, 2),
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
};

export const RichContentConversation: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '100%', maxWidth: '600px' }}>
      <ChatCard
        message="Hello! Can you help me analyze my brand?"
        sender="user"
        senderName="John Doe"
        avatarInitials="JD"
        timestamp={new Date(Date.now() - 300000)}
      />
      <ChatCard
        message="Hello! I'd be happy to help you analyze your brand. Please upload your brand files and I'll provide a comprehensive analysis."
        sender="agent"
        senderName="BrandChecker AI"
        avatarInitials="AI"
        timestamp={new Date(Date.now() - 240000)}
      />
      <ChatCard
        message="Great! I'll upload my brand guidelines now."
        sender="user"
        senderName="John Doe"
        avatarInitials="JD"
        timestamp={new Date(Date.now() - 180000)}
      />
      <ChatCard
        message="Here's your brand consistency score:"
        sender="agent"
        senderName="BrandChecker AI"
        avatarInitials="AI"
        timestamp={new Date(Date.now() - 120000)}
        messageType="score"
        messageData={{
          type: 'score',
          content: {
            value: 85,
            label: 'Brand Consistency',
            showPercentage: true,
            iconName: 'star'
          }
        }}
      />
      <ChatCard
        message="Here's a detailed analysis of your brand elements:"
        sender="agent"
        senderName="BrandChecker AI"
        avatarInitials="AI"
        timestamp={new Date(Date.now() - 60000)}
        messageType="analysis"
        messageData={{
          type: 'analysis',
          content: {
            title: 'Brand Element Analysis',
            status: 'success',
            results: sampleAnalysisResults
          }
        }}
      />
      <ChatCard
        message="Here are my recommendations for improving your brand:"
        sender="agent"
        senderName="BrandChecker AI"
        avatarInitials="AI"
        timestamp={new Date()}
        messageType="recommendations"
        messageData={{
          type: 'recommendations',
          content: {
            title: 'Improvement Recommendations',
            recommendations: sampleRecommendations,
            showPriority: true,
            showStatus: true,
            showTags: true,
            maxItems: 2
          }
        }}
      />
    </div>
  )
};