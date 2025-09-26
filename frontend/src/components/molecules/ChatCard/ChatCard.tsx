import { Typography } from '../../atoms/Typography';
import { Avatar } from '../../atoms/Avatar';
import { Score } from '../../atoms/Score';
import { TrafficLight } from '../../atoms/TrafficLight';
import { Chart } from '../../atoms/Chart';
import { RecommendationList } from '../../atoms/RecommendationList';
import { ResultCard } from '../../atoms/ResultCard';
import { ColorSwatch } from '../../atoms/ColorSwatch';
import { AnalysisResults } from '../AnalysisResults';
import type { AnalysisResult } from '../../atoms/ResultCard';
import type { ColorData } from '../../atoms/ColorSwatch';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './ChatCard.css';

/**
 * Chat Message Type
 */
export type ChatMessageType = 'text' | 'score' | 'analysis' | 'chart' | 'recommendations' | 'result-card' | 'analysis-results' | 'extraction-results';

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
    console.log('🔍 ChatCard renderRichContent:', { messageType, messageData });
    
    if (!messageData) {
      console.log('❌ No messageData provided');
      return null;
    }

    // Handle extraction-results messageType directly
    if (messageType === 'extraction-results') {
      const extractionResultsData = messageData as any;
      console.log('🎨 Rendering extraction-results:', extractionResultsData);
      return (
        <div className="chat-card__rich-content chat-card__extraction-results">
          {/* Summary ResultCard */}
          {extractionResultsData.summary && (
            <ResultCard
              type="summary"
              variant="compact"
              title="Extraktionszusammenfassung"
              description="Übersicht der extrahierten Elemente aus dem PDF"
              size="sm"
              showScore={false}
              showStatus={false}
              showChart={false}
              showRecommendations={false}
              showDetails={true}
              tags={[
                `${extractionResultsData.summary.total_colors} Farben`,
                `${extractionResultsData.summary.total_fonts} Fonts`,
                `${extractionResultsData.summary.total_pages} Seiten`,
                `${extractionResultsData.summary.total_images} Bilder`
              ]}
              category="PDF-Extraktion"
              timestamp={new Date()}
            />
          )}
          
          {/* Color Analysis with ColorSwatch */}
          {extractionResultsData.extraction_data?.color_analysis?.colors && (
            <div style={{
              backgroundColor: 'var(--color-background-secondary)',
              border: '1px solid var(--color-grey-800)',
              borderRadius: 'var(--border-radius-md)',
              padding: 'var(--space-4)',
              margin: 'var(--space-2) 0'
            }}>
              <Typography variant="h4" size="sm" weight="semibold" style={{ marginBottom: 'var(--space-3)' }}>
                🎨 Farbanalyse
              </Typography>
              <Typography variant="body" size="xs" color="secondary" style={{ marginBottom: 'var(--space-3)' }}>
                Hauptfarben aus dem PDF-Dokument
              </Typography>
              <div style={{ 
                display: 'flex', 
                gap: 'var(--space-2)', 
                flexWrap: 'wrap'
              }}>
                {extractionResultsData.extraction_data.color_analysis.colors.slice(0, 5).map((color: any, index: number) => {
                  const colorData: ColorData = {
                    hex: color.hex,
                    name: color.name,
                    usage_percentage: color.usage_percentage,
                    usage_count: color.usage_count,
                    rgb: color.rgb,
                    description: color.description
                  };
                  
                  return (
                    <ColorSwatch
                      key={index}
                      color={colorData}
                      size="sm"
                      showName={true}
                      showPercentage={true}
                      showCount={false}
                      showRgb={false}
                      showDescription={false}
                      onClick={(color) => console.log('Color clicked:', color)}
                    />
                  );
                })}
              </div>
            </div>
          )}
          
          {/* Font Analysis */}
          {extractionResultsData.extraction_data?.font_analysis?.fonts && (
            <div style={{
              backgroundColor: 'var(--color-background-secondary)',
              border: '1px solid var(--color-grey-800)',
              borderRadius: 'var(--border-radius-md)',
              padding: 'var(--space-4)',
              margin: 'var(--space-2) 0'
            }}>
              <Typography variant="h4" size="sm" weight="semibold" style={{ marginBottom: 'var(--space-3)' }}>
                🔤 Schriftarten-Analyse
              </Typography>
              <Typography variant="body" size="xs" color="secondary" style={{ marginBottom: 'var(--space-3)' }}>
                Verwendete Schriftarten im PDF-Dokument
              </Typography>
              <div style={{ 
                display: 'flex', 
                flexDirection: 'column',
                gap: 'var(--space-2)'
              }}>
                {extractionResultsData.extraction_data.font_analysis.fonts.slice(0, 3).map((font: any, index: number) => (
                  <div key={index} style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: 'var(--space-2)',
                    backgroundColor: 'var(--color-background)',
                    borderRadius: 'var(--border-radius-sm)',
                    border: '1px solid var(--color-grey-800)'
                  }}>
                    <div>
                      <Typography variant="body" size="xs" weight="medium">
                        {font.name}
                      </Typography>
                      <Typography variant="caption" size="xs" color="secondary">
                        {font.size}pt
                      </Typography>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <Typography variant="body" size="xs" weight="semibold">
                        {font.usage_count}x
                      </Typography>
                      <Typography variant="caption" size="xs" color="secondary">
                        verwendet
                      </Typography>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Layout Analysis */}
          {extractionResultsData.extraction_data?.layout_analysis?.alignment_analysis && (
            <div style={{
              backgroundColor: 'var(--color-background-secondary)',
              border: '1px solid var(--color-grey-800)',
              borderRadius: 'var(--border-radius-md)',
              padding: 'var(--space-4)',
              margin: 'var(--space-2) 0'
            }}>
              <Typography variant="h4" size="sm" weight="semibold" style={{ marginBottom: 'var(--space-3)' }}>
                📐 Layout-Analyse
              </Typography>
              <Typography variant="body" size="xs" color="secondary" style={{ marginBottom: 'var(--space-3)' }}>
                Textausrichtung und Struktur
              </Typography>
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', 
                gap: 'var(--space-2)'
              }}>
                <div style={{ textAlign: 'center', padding: 'var(--space-2)', backgroundColor: 'var(--color-background)', borderRadius: 'var(--border-radius-sm)' }}>
                  <Typography variant="body" size="sm" weight="semibold">
                    {extractionResultsData.extraction_data.layout_analysis.alignment_analysis.alignment_counts.left || 0}
                  </Typography>
                  <Typography variant="caption" size="xs" color="secondary">Links</Typography>
                </div>
                <div style={{ textAlign: 'center', padding: 'var(--space-2)', backgroundColor: 'var(--color-background)', borderRadius: 'var(--border-radius-sm)' }}>
                  <Typography variant="body" size="sm" weight="semibold">
                    {extractionResultsData.extraction_data.layout_analysis.alignment_analysis.alignment_counts.right || 0}
                  </Typography>
                  <Typography variant="caption" size="xs" color="secondary">Rechts</Typography>
                </div>
                <div style={{ textAlign: 'center', padding: 'var(--space-2)', backgroundColor: 'var(--color-background)', borderRadius: 'var(--border-radius-sm)' }}>
                  <Typography variant="body" size="sm" weight="semibold">
                    {extractionResultsData.extraction_data.layout_analysis.alignment_analysis.alignment_counts.center || 0}
                  </Typography>
                  <Typography variant="caption" size="xs" color="secondary">Zentriert</Typography>
                </div>
                <div style={{ textAlign: 'center', padding: 'var(--space-2)', backgroundColor: 'var(--color-background)', borderRadius: 'var(--border-radius-sm)' }}>
                  <Typography variant="body" size="sm" weight="semibold">
                    {extractionResultsData.extraction_data.layout_analysis.alignment_analysis.alignment_counts.justified || 0}
                  </Typography>
                  <Typography variant="caption" size="xs" color="secondary">Blocksatz</Typography>
                </div>
              </div>
            </div>
          )}
        </div>
      );
    }

    // Handle other message types with messageData.type
    if (!messageData.type) {
      console.log('❌ No messageData.type provided');
      return null;
    }

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

      case 'analysis-results':
        const analysisResultsData = messageData as any;
        return (
          <div className="chat-card__rich-content chat-card__analysis-results">
            <AnalysisResults results={analysisResultsData} />
          </div>
        );


      default:
        console.log('❌ Unknown messageType:', messageData.type);
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
                  <div style={{ 
                    fontSize: 'var(--font-size-xs)',
                    lineHeight: 'var(--line-height-tight)',
                    color: 'var(--color-text-primary)',
                    fontFamily: 'var(--font-family-sans)',
                    margin: 'var(--space-1) 0'
                  }}>
                    {children}
                  </div>
                ),
                strong: ({ children }) => (
                  <strong style={{ 
                    fontSize: 'var(--font-size-xs)',
                    lineHeight: 'var(--line-height-tight)',
                    color: 'var(--color-text-primary)',
                    fontFamily: 'var(--font-family-sans)',
                    fontWeight: 'var(--font-weight-semibold)'
                  }}>
                    {children}
                  </strong>
                ),
                code: ({ children }) => (
                  <code style={{ 
                    fontSize: 'var(--font-size-xs)',
                    lineHeight: 'var(--line-height-tight)',
                    color: 'var(--color-text-primary)',
                    fontFamily: 'var(--font-family-mono)',
                    backgroundColor: 'var(--color-background-secondary)',
                    padding: 'var(--space-1) var(--space-2)',
                    borderRadius: 'var(--border-radius-sm)',
                    display: 'inline-block'
                  }}>
                    {children}
                  </code>
                ),
                pre: ({ children }) => (
                  <pre style={{ 
                    backgroundColor: 'var(--color-background-secondary)',
                    padding: 'var(--space-3)',
                    borderRadius: 'var(--border-radius-md)',
                    fontFamily: 'var(--font-family-mono)',
                    fontSize: 'var(--font-size-xs)',
                    lineHeight: 'var(--line-height-tight)',
                    color: 'var(--color-text-primary)',
                    overflow: 'auto',
                    margin: 'var(--space-2) 0'
                  }}>
                    {children}
                  </pre>
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