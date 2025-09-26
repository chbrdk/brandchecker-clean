import React from 'react';
import { BrandCheckerChat } from '../components/templates/BrandCheckerChat';
import type { ChatMessage } from '../components/templates/BrandCheckerChat';
import './App.css';

/**
 * Standalone BrandChecker App
 * 
 * Uses the existing BrandCheckerChat template without modifications
 */
function App() {
  const [messages, setMessages] = React.useState<ChatMessage[]>([
    {
      id: '1',
      content: 'Willkommen beim BrandChecker! Laden Sie Ihre Dateien hoch, um eine Markenanalyse zu starten.',
      sender: 'agent',
      timestamp: new Date(),
      avatar: '🤖'
    }
  ]);

  const handleSendMessage = (content: string) => {
    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date(),
      avatar: '👤'
    };

    setMessages(prev => [...prev, newMessage]);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: 'Ich habe Ihre Nachricht erhalten und analysiere sie...',
        sender: 'agent',
        timestamp: new Date(),
        avatar: '🤖'
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  const handleFilesUpload = (files: File[]) => {
    console.log('Files uploaded:', files);
    
    const uploadMessage: ChatMessage = {
      id: Date.now().toString(),
      content: `${files.length} Datei(en) hochgeladen. Starte Analyse...`,
      sender: 'agent',
      timestamp: new Date(),
      avatar: '📁'
    };

    setMessages(prev => [...prev, uploadMessage]);
  };

  return (
    <div className="app">
      <BrandCheckerChat
        initialMessages={messages}
        placeholder="Nachricht eingeben..."
        onSendMessage={handleSendMessage}
        onFilesUpload={handleFilesUpload}
      />
    </div>
  );
}

export default App;
