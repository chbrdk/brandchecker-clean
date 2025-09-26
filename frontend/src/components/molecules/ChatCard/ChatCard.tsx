import { Typography } from '../../atoms/Typography';
import { Score } from '../../atoms/Score';
import { TrafficLight } from '../../atoms/TrafficLight';
import { Chart } from '../../atoms/Chart';
import { RecommendationList } from '../../atoms/RecommendationList';
import { ResultCard } from '../../atoms/ResultCard';
import type { AnalysisResult } from '../../atoms/ResultCard';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import './ChatCard.css';

/**
 * Chat Message Type
 */
export type ChatMessageType = 'text' | 'score' | 'analysis' | 'chart' | 'recommendations' | 'result-card';

/**
 * Chat Message Data
 */
export interface ChatMessageData {
  type: ChatMessageType;
  content: any; // Flexible content based on type
}

/**
 * Chat Card Props
 */
export interface ChatCardProps {
  /** Message content */
  message: string;
  /** Sender type */
  sender: 'user' | 'agent';
  /** Sender name */
  senderName?: string;
  /** Avatar initials */
  avatarInitials?: string;
  /** Timestamp */
  timestamp?: Date | string;
  /** Message type */
  messageType?: ChatMessageType;
  /** Message data for rich content */
  messageData?: ChatMessageData;
  /** Additional CSS class */
  className?: string;
}

/**
 * Chat Card Component
 * 
 * Displays chat messages with support for various content types including
 * text, scores, analysis results, charts, recommendations, and result cards.
 * 
 * Features:
 * - Multiple message types (text, score, analysis, chart, recommendations, result-card)
 * - Rich content rendering with atomic components
 * - Alternating layout (user right, agent left)
 * - Timestamp display
 * - Responsive design
 * - Design token integration
 * 
 * @param props - ChatCardProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Text message
 * <ChatCard 
 *   message="Hello! How can I help you?" 
 *   sender="agent" 
 *   senderName="BrandChecker AI" 
 * />
 * 
 * // Score message
 * <ChatCard 
 *   message="Here's your brand consistency score:" 
 *   sender="agent" 
 *   messageType="score" 
 *   messageData={{ type: 'score', content: { value: 85, label: 'Brand Score' } }} 
 * />
 * ```
 */
export const ChatCard = ({
  message,
  sender,
  senderName,
  avatarInitials,
  timestamp,
  messageType = 'text',
  messageData,
  className = ''
}: ChatCardProps) => {
  const classes = [
    'chat-card',
    `chat-card--${sender}`,
    `chat-card--${messageType}`,
    className
  ].filter(Boolean).join(' ');

  const formatTimestamp = (ts: Date | string) => {
    const date = typeof ts === 'string' ? new Date(ts) : ts;
    return date.toLocaleTimeString('de-DE', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  // Render rich content based on message type
  const renderRichContent = () => {
    if (!messageData) return null;

    switch (messageData.type) {
      case 'score':
        const scoreData = messageData.content;
        return (
          <div className="chat-card__rich-content chat-card__score">
            <Score
              value={scoreData.value}
              max={scoreData.max || 100}
              label={scoreData.label}
              size="md"
              showPercentage={scoreData.showPercentage !== false}
              iconName={scoreData.iconName}
            />
          </div>
        );

      case 'analysis':
        const analysisData = messageData.content;
        return (
          <div className="chat-card__rich-content chat-card__analysis">
            <div className="chat-card__analysis-header">
              <Typography variant="h4" size="sm" weight="semibold" color="primary">
                {analysisData.title || 'Analysis Results'}
              </Typography>
              <TrafficLight
                status={analysisData.status || 'success'}
                size="sm"
                showLabel={true}
              />
            </div>
            {analysisData.results && analysisData.results.length > 0 && (
              <div className="chat-card__analysis-results">
                {analysisData.results.map((result: AnalysisResult, index: number) => (
                  <div key={index} className="chat-card__analysis-item">
                    <div className="chat-card__analysis-item-header">
                      <Typography variant="body" size="sm" weight="medium" color="primary">
                        {result.category}
                      </Typography>
                      <div className="chat-card__analysis-item-score">
                        <Score value={result.score} size="sm" showPercentage />
                        <TrafficLight status={result.status} size="sm" showLabel={false} />
                      </div>
                    </div>
                    {result.details && (
                      <Typography variant="body" size="xs" color="secondary">
                        {result.details}
                      </Typography>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        );

      case 'chart':
        const chartData = messageData.content;
        return (
          <div className="chat-card__rich-content chat-card__chart">
            <Chart
              type={chartData.type || 'bar'}
              data={chartData.data}
              title={chartData.title}
              size="sm"
              showLegend={chartData.showLegend !== false}
              showValues={chartData.showValues !== false}
            />
          </div>
        );

      case 'recommendations':
        const recommendationsData = messageData.content;
        return (
          <div className="chat-card__rich-content chat-card__recommendations">
            <RecommendationList
              recommendations={recommendationsData.recommendations}
              title={recommendationsData.title}
              size="sm"
              showPriority={recommendationsData.showPriority !== false}
              showStatus={recommendationsData.showStatus !== false}
              showTags={recommendationsData.showTags !== false}
              maxItems={recommendationsData.maxItems || 3}
            />
          </div>
        );

      case 'result-card':
        const resultCardData = messageData.content;
        return (
          <div className="chat-card__rich-content chat-card__result-card">
            <ResultCard
              type={resultCardData.type || 'summary'}
              variant={resultCardData.variant || 'default'}
              title={resultCardData.title}
              description={resultCardData.description}
              score={resultCardData.score}
              status={resultCardData.status}
              analysisResults={resultCardData.analysisResults}
              chartData={resultCardData.chartData}
              recommendations={resultCardData.recommendations}
              iconName={resultCardData.iconName}
              size="sm"
              showScore={resultCardData.showScore !== false}
              showStatus={resultCardData.showStatus !== false}
              showChart={resultCardData.showChart}
              showRecommendations={resultCardData.showRecommendations}
              showDetails={resultCardData.showDetails}
            />
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className={classes}>
      <div className="chat-card__avatar">
        <div className="chat-card__avatar-circle">
          {avatarInitials || (sender === 'user' ? 'U' : 'AI')}
        </div>
      </div>
      
      <div className="chat-card__content">
        <div className="chat-card__header">
          {senderName && (
            <span className="chat-card__sender-name">
              {senderName}
            </span>
          )}
          {timestamp && (
            <span className="chat-card__timestamp">
              {formatTimestamp(timestamp)}
            </span>
          )}
        </div>
        
        <div className="chat-card__message">
          {message.includes('<img') ? (
            // Direktes HTML-Rendering für Nachrichten mit Bildern
            <div 
              style={{
                fontSize: 'var(--font-size-xs)',
                lineHeight: 'var(--line-height-tight)',
                color: 'var(--color-text-primary)',
                fontFamily: 'var(--font-family-sans)'
              }}
              dangerouslySetInnerHTML={{ 
                __html: message
                  .replace(/\*\*(.*?)\*\*/g, '<strong style="font-weight: var(--font-weight-semibold);">$1</strong>')
                  .replace(/\n/g, '<br>')
              }} 
            />
          ) : (
            // Markdown-Rendering für normale Nachrichten
            <ReactMarkdown 
              remarkPlugins={[remarkGfm]}
              components={{
                p: ({ children }) => (
                  <Typography variant="body" size="xs" color="primary">
                    {children}
                  </Typography>
                ),
                strong: ({ children }) => (
                  <Typography variant="body" size="xs" weight="semibold" color="primary">
                    {children}
                  </Typography>
                ),
                code: ({ children }) => (
                  <Typography 
                    variant="body" 
                    size="xs" 
                    color="primary"
                    style={{ 
                      backgroundColor: 'var(--color-background-secondary)',
                      padding: 'var(--space-1) var(--space-2)',
                      borderRadius: 'var(--border-radius-sm)',
                      fontFamily: 'var(--font-family-mono)',
                      display: 'inline-block'
                    }}
                  >
                    {children}
                  </Typography>
                ),
                pre: ({ children }) => (
                  <div style={{ 
                    backgroundColor: 'var(--color-background-secondary)',
                    padding: 'var(--space-3)',
                    borderRadius: 'var(--border-radius-md)',
                    fontFamily: 'var(--font-family-mono)',
                    fontSize: 'var(--font-size-xs)',
                    overflow: 'auto',
                    margin: 'var(--space-2) 0'
                  }}>
                    <Typography variant="body" size="xs" color="primary">
                      {children}
                    </Typography>
                  </div>
                )
              }}
            >
              {message}
            </ReactMarkdown>
          )}
        </div>

        {renderRichContent()}
      </div>
    </div>
  );
};

ChatCard.displayName = 'ChatCard';