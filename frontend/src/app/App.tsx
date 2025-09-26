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
      message: 'Willkommen beim BrandChecker! Laden Sie Ihre Dateien hoch, um eine Markenanalyse zu starten.',
      sender: 'agent',
      senderName: 'BrandChecker AI',
      avatarInitials: 'AI',
      timestamp: new Date()
    }
  ]);

  const [pendingFiles, setPendingFiles] = React.useState<File[]>([]);

  const handleSendMessage = async (content: string, files?: File[]) => {
    console.log('🔵 handleSendMessage called with:', { content, files: files?.map(f => f.name), pendingFilesCount: pendingFiles.length });
    
    // User-Nachricht erstellen
    let userContent = content;
    
    // Wenn Dateien vorhanden sind, füge sie zur Nachricht hinzu
    const filesToUse = files || pendingFiles;
    if (filesToUse.length > 0) {
      console.log('📎 Files found:', filesToUse.map(f => f.name));
      const fileInfo = filesToUse.map(file => 
        `**${file.name}** (${(file.size / (1024 * 1024)).toFixed(2)} MB)`
      ).join('\n');
      
      userContent = content ? 
        `${content}\n\n${fileInfo}` : 
        `Starte Analyse:\n\n${fileInfo}`;
    }

    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      message: userContent,
      sender: 'user',
      senderName: 'You',
      avatarInitials: 'U',
      timestamp: new Date()
    };

    console.log('💬 Creating user message:', newMessage);
    setMessages(prev => {
      const updated = [...prev, newMessage];
      console.log('📝 Messages updated, new count:', updated.length);
      return updated;
    });

    // Wenn Dateien vorhanden sind, lade sie hoch
    if (filesToUse.length > 0) {
      console.log('⬆️ Starting file upload...');
      await uploadFiles(filesToUse);
      setPendingFiles([]); // Lösche pending files nach Upload
      console.log('✅ Files uploaded and pendingFiles cleared');
    } else {
      console.log('💭 No files, creating normal AI response...');
      // Normale Chat-Antwort ohne Dateien
      setTimeout(() => {
        const aiResponse: ChatMessage = {
          id: (Date.now() + 1).toString(),
          message: 'Ich habe Ihre Nachricht erhalten und analysiere sie...',
          sender: 'agent',
          senderName: 'BrandChecker AI',
          avatarInitials: 'AI',
          timestamp: new Date()
        };
        console.log('🤖 Creating AI response:', aiResponse);
        setMessages(prev => [...prev, aiResponse]);
      }, 1000);
    }
  };

  const handleFilesUpload = (files: File[]) => {
    console.log('📁 handleFilesUpload called with:', files.map(f => f.name));
    
    // Speichere Dateien für späteren Upload beim Send
    setPendingFiles(prev => {
      const updated = [...prev, ...files];
      console.log('💾 pendingFiles updated:', updated.map(f => f.name));
      return updated;
    });
    
    // KEINE Chat-Nachricht hier - Dateien werden nur in der Toolbar angehängt
  };

  const uploadFiles = async (files: File[]) => {
    console.log('⬆️ uploadFiles called with:', files.map(f => f.name));
    
    // Upload-Start-Nachricht
    const uploadStartMessage: ChatMessage = {
      id: Date.now().toString(),
      message: `📤 Lade ${files.length} Datei(en) hoch...`,
      sender: 'agent',
      senderName: 'BrandChecker AI',
      avatarInitials: 'AI',
      timestamp: new Date()
    };
    console.log('📤 Creating upload start message:', uploadStartMessage);
    setMessages(prev => [...prev, uploadStartMessage]);

    // Dateien einzeln hochladen
    for (const file of files) {
      try {
        console.log('📤 Uploading file:', file.name);
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('http://localhost:8006/upload', {
          method: 'POST',
          body: formData,
          mode: 'cors',
        });

        console.log('📡 Upload response status:', response.status);
        const result = await response.json();
        console.log('📦 Upload result:', result);

        if (response.ok && result.success) {
          console.log('✅ Upload successful for:', result.original_filename);
          console.log('🖼️ Preview available:', result.preview?.available);
          
          // Erfolgreiche Upload-Nachricht mit Preview
          let messageContent = `**${result.original_filename}** erfolgreich hochgeladen!\n\n`;
          
          // Füge Preview hinzu wenn verfügbar
          if (result.preview && result.preview.available && result.preview.base64) {
            console.log('🖼️ Adding preview to message, base64 length:', result.preview.base64.length);
            console.log('🖼️ Base64 start:', result.preview.base64.substring(0, 50));
            console.log('🖼️ Base64 format check:', result.preview.base64.startsWith('data:'));
            
            // Verwende HTML statt Markdown für Base64-Bilder
            const htmlImage = `<img src="${result.preview.base64}" alt="${result.original_filename}" style="max-width: 100%; height: auto; border-radius: 8px; margin: 8px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />`;
            console.log('🖼️ HTML image syntax:', htmlImage.substring(0, 100) + '...');
            
            // Dateieigenschaften unter das Preview-Bild
            const fileDetails = `<div style="margin-top: 8px; font-size: var(--font-size-xs); color: var(--color-text-secondary);">
              <div><strong>Dateityp:</strong> ${result.file_type.toUpperCase()}</div>
              <div><strong>Größe:</strong> ${result.file_size_mb} MB</div>
              <div><strong>Pfad:</strong> ${result.relative_path}</div>
            </div>`;
            
            messageContent += `${htmlImage}${fileDetails}\n\n`;
          } else {
            console.log('❌ No preview available:', result.preview);
            // Fallback ohne Preview
            messageContent += `**Dateityp:** ${result.file_type.toUpperCase()}\n` +
                             `**Größe:** ${result.file_size_mb} MB\n` +
                             `**Pfad:** ${result.relative_path}\n\n`;
          }
          
          messageContent += `Die Datei steht nun für die Analyse zur Verfügung.`;

          const successMessage: ChatMessage = {
            id: (Date.now() + Math.random()).toString(),
            message: messageContent,
            sender: 'agent',
            senderName: 'BrandChecker AI',
            avatarInitials: 'AI',
            timestamp: new Date()
          };
          console.log('💬 Creating success message:', successMessage);
          setMessages(prev => [...prev, successMessage]);
        } else {
          // Fehler-Nachricht
          const errorMessage: ChatMessage = {
            id: (Date.now() + Math.random()).toString(),
            message: `❌ **Fehler beim Upload von ${file.name}:**\n\n${result.error || 'Unbekannter Fehler'}`,
            sender: 'agent',
            senderName: 'BrandChecker AI',
            avatarInitials: 'AI',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, errorMessage]);
        }
      } catch (error) {
        // Network-Fehler
        const networkErrorMessage: ChatMessage = {
          id: (Date.now() + Math.random()).toString(),
          message: `🔌 **Netzwerk-Fehler beim Upload von ${file.name}:**\n\n${error instanceof Error ? error.message : 'Verbindung zum Upload-Service fehlgeschlagen'}`,
          sender: 'agent',
          senderName: 'BrandChecker AI',
          avatarInitials: 'AI',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, networkErrorMessage]);
      }
    }
  };

  // Debug: Log current state
  React.useEffect(() => {
    console.log('🔄 App state changed - messages:', messages.length, 'pendingFiles:', pendingFiles.length);
  }, [messages, pendingFiles]);

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
