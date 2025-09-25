import { useState, useEffect, useRef } from 'react';
import { Typography } from '../../atoms/Typography';
import { ChatToolbar } from '../../molecules/ChatToolbar';
import { ChatCard } from '../../molecules/ChatCard';
import './BrandCheckerChat.css';

export interface ChatMessage {
  id: string;
  message: string;
  sender: 'user' | 'agent';
  senderName?: string;
  avatarInitials?: string;
  timestamp: Date;
  messageType?: 'text' | 'score' | 'analysis' | 'chart' | 'recommendations' | 'result-card';
  messageData?: any;
}

/**
 * BrandChecker Chat Props
 */
export interface BrandCheckerChatProps {
  /** Initial messages to display */
  initialMessages?: ChatMessage[];
  /** Placeholder text for input */
  placeholder?: string;
  /** Send message handler */
  onSendMessage?: (message: string) => void;
  /** File upload handler */
  onFilesUpload?: (files: File[]) => void;
  /** Additional CSS class */
  className?: string;
}

/**
 * BrandChecker Chat Component
 */
export const BrandCheckerChat = ({
  initialMessages = [],
  placeholder = 'Ask about your brand...',
  onSendMessage,
  onFilesUpload,
  className = ''
}: BrandCheckerChatProps) => {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [isAgentTyping, setIsAgentTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isAgentTyping]);

  useEffect(() => {
    setMessages(initialMessages);
  }, [initialMessages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = (text: string) => {
    if (!text.trim()) return;

    const newUserMessage: ChatMessage = {
      id: `msg-${Date.now()}-user`,
      message: text,
      sender: 'user',
      senderName: 'You',
      avatarInitials: 'U',
      timestamp: new Date(),
    };

    setMessages((prevMessages) => [...prevMessages, newUserMessage]);
    onSendMessage?.(text);

    // Simulate AI response for demo
    if (!onSendMessage) {
      setIsAgentTyping(true);
      setTimeout(() => {
        const aiResponse: ChatMessage = {
          id: `msg-${Date.now()}-agent`,
          message: `Thanks for your message: "${text}". I'm processing your request.`,
          sender: 'agent',
          senderName: 'BrandChecker AI',
          avatarInitials: 'AI',
          timestamp: new Date(),
        };
        setMessages((prevMessages) => [...prevMessages, aiResponse]);
        setIsAgentTyping(false);
      }, 1500);
    }
  };

  const handleFilesUpload = (files: File[]) => {
    const fileNames = files.map(file => file.name).join(', ');
    const uploadMessage: ChatMessage = {
      id: `msg-${Date.now()}-upload`,
      message: `Uploaded files: ${fileNames}`,
      sender: 'user',
      senderName: 'You',
      avatarInitials: 'U',
      timestamp: new Date(),
    };
    setMessages((prevMessages) => [...prevMessages, uploadMessage]);
    onFilesUpload?.(files);

    // Simulate AI response for demo
    if (!onFilesUpload) {
      setIsAgentTyping(true);
      setTimeout(() => {
        const aiResponse: ChatMessage = {
          id: `msg-${Date.now()}-agent-upload-ack`,
          message: `Received your files. I'll start analyzing them now.`,
          sender: 'agent',
          senderName: 'BrandChecker AI',
          avatarInitials: 'AI',
          timestamp: new Date(),
        };
        setMessages((prevMessages) => [...prevMessages, aiResponse]);
        setIsAgentTyping(false);
      }, 2000);
    }
  };

  return (
    <div className={`brandchecker-chat ${className}`}>
      <div className="brandchecker-chat__header">
        <Typography variant="h2" size="lg" weight="semibold">
          BrandChecker Chat
        </Typography>
        <Typography variant="body" color="secondary">
          Ask questions about your brand or request specific analyses
        </Typography>
      </div>
      
      <div className="brandchecker-chat__messages">
        {messages.length === 0 ? (
          <div className="brandchecker-chat__empty">
            <Typography variant="body" color="secondary" align="center">
              Start a conversation with BrandChecker AI
            </Typography>
          </div>
        ) : (
          messages.map((msg) => (
            <ChatCard
              key={msg.id}
              message={msg.message}
              sender={msg.sender}
              senderName={msg.senderName}
              avatarInitials={msg.avatarInitials}
              timestamp={msg.timestamp}
              messageType={msg.messageType}
              messageData={msg.messageData}
            />
          ))
        )}
        {isAgentTyping && (
          <ChatCard
            message="BrandChecker AI is typing..."
            sender="agent"
            senderName="BrandChecker AI"
            avatarInitials="AI"
            timestamp={new Date()}
          />
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="brandchecker-chat__toolbar">
        <ChatToolbar
          placeholder={placeholder}
          onSendMessage={handleSendMessage}
          onFilesUpload={handleFilesUpload}
          disabled={isAgentTyping}
          loading={isAgentTyping}
        />
      </div>
    </div>
  );
};

BrandCheckerChat.displayName = 'BrandCheckerChat';