import React from 'react';
import { BrandCheckerChat } from '../components/templates/BrandCheckerChat';
import type { ChatMessage } from '../components/templates/BrandCheckerChat';
import { ProgressBar } from '../components/atoms/ProgressBar';
import { AnalysisResults } from '../components/molecules/AnalysisResults';
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
  const [analysisStatus, setAnalysisStatus] = React.useState<{
    fileId: string;
    status: 'pending' | 'processing' | 'completed' | 'error';
    progress: number;
    message: string;
    results?: any;
  } | null>(null);

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
      id: `user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
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
          id: `agent-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
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
      id: `upload-start-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
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
            id: `upload-success-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            message: messageContent,
            sender: 'agent',
            senderName: 'BrandChecker AI',
            avatarInitials: 'AI',
            timestamp: new Date()
          };
          console.log('💬 Creating success message:', successMessage);
          setMessages(prev => [...prev, successMessage]);

          // Backend-Analyse starten
          console.log('🔍 Starting backend analysis for:', result.original_filename);
          await startBackendAnalysis(result);
        } else {
          // Fehler-Nachricht
          const errorMessage: ChatMessage = {
            id: `upload-error-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
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
          id: `upload-network-error-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
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

  const startBackendAnalysis = async (uploadResult: any) => {
    try {
      console.log('🔍 Sending file to backend for analysis:', uploadResult.relative_path);
      
      // Analyse-Start-Nachricht mit Progress Bar
      const analysisStartMessage: ChatMessage = {
        id: `analysis-start-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        message: `**Analyse gestartet**\n\nVerarbeite ${uploadResult.original_filename}...`,
        sender: 'agent',
        senderName: 'BrandChecker AI',
        avatarInitials: 'AI',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, analysisStartMessage]);

      // Status-Tracking starten
      setAnalysisStatus({
        fileId: uploadResult.file_id,
        status: 'processing',
        progress: 0,
        message: 'Initialisiere Analyse...'
      });

      // Backend-API aufrufen
      const response = await fetch('http://localhost:8000/extract-all-path', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          filepath: uploadResult.relative_path,
          file_id: uploadResult.file_id,
          original_filename: uploadResult.original_filename
        }),
        mode: 'cors',
      });

      console.log('📡 Backend analysis response status:', response.status);
      const analysisResult = await response.json();
      console.log('📦 Backend analysis result:', analysisResult);

      if (response.ok && analysisResult.success) {
        // Status-Polling starten
        startStatusPolling(uploadResult.file_id);
      } else {
        // Analyse-Fehler
        setAnalysisStatus({
          fileId: uploadResult.file_id,
          status: 'error',
          progress: 0,
          message: analysisResult.error || 'Unbekannter Fehler'
        });
        
        const analysisErrorMessage: ChatMessage = {
          id: `analysis-error-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
          message: `**Analyse-Fehler**\n\nFehler bei der Verarbeitung von ${uploadResult.original_filename}:\n\n${analysisResult.error || 'Unbekannter Fehler'}`,
          sender: 'agent',
          senderName: 'BrandChecker AI',
          avatarInitials: 'AI',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, analysisErrorMessage]);
      }
    } catch (error) {
      console.error('❌ Backend analysis error:', error);
      
      // Network-Fehler
      setAnalysisStatus({
        fileId: uploadResult.file_id,
        status: 'error',
        progress: 0,
        message: 'Netzwerk-Fehler'
      });
      
      const networkErrorMessage: ChatMessage = {
        id: `analysis-network-error-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        message: `**Netzwerk-Fehler**\n\nVerbindung zum Analyse-Service fehlgeschlagen:\n\n${error instanceof Error ? error.message : 'Unbekannter Netzwerk-Fehler'}`,
        sender: 'agent',
        senderName: 'BrandChecker AI',
        avatarInitials: 'AI',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, networkErrorMessage]);
    }
  };

  // Send extraction results to n8n webhook
  const sendToN8nWebhook = async (extractionResults: any) => {
    try {
      console.log('📤 Sending extraction results to n8n webhook...');
      console.log('📤 Webhook URL: http://localhost:5680/webhook/analyze_n8n');
      console.log('📤 Payload size:', JSON.stringify(extractionResults).length, 'bytes');
      
      const webhookUrl = 'http://localhost:5680/webhook/analyze_n8n';
      
      const response = await fetch(webhookUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(extractionResults)
      });

      console.log('📤 Response status:', response.status);
      console.log('📤 Response headers:', Object.fromEntries(response.headers.entries()));

      if (response.ok) {
        console.log('✅ Successfully sent extraction results to n8n webhook');
        try {
          const responseData = await response.json();
          console.log('📦 n8n webhook response:', responseData);
        } catch (e) {
          console.log('📦 n8n webhook response (no JSON):', await response.text());
        }
      } else {
        console.error('❌ Failed to send to n8n webhook:', response.status, response.statusText);
        const errorText = await response.text();
        console.error('❌ Error details:', errorText);
      }
    } catch (error) {
      console.error('❌ Error sending to n8n webhook:', error);
      console.error('❌ Error details:', error.message);
      console.error('❌ Error stack:', error.stack);
    }
  };

  const startStatusPolling = (fileId: string) => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`http://localhost:8000/analysis-status/${fileId}`, {
          method: 'GET',
          mode: 'cors',
        });

        if (response.ok) {
          const statusData = await response.json();
          console.log('📊 Status update:', statusData);
          
          setAnalysisStatus({
            fileId: statusData.file_id,
            status: statusData.status,
            progress: statusData.progress,
            message: statusData.message,
            results: statusData.results
          });

          // Wenn Analyse abgeschlossen, Polling stoppen
          if (statusData.status === 'completed' || statusData.status === 'error') {
            clearInterval(pollInterval);
            
            if (statusData.status === 'completed') {
              // Extraktionsdaten für strukturierte Darstellung vorbereiten
              const results = statusData.results;
              let resultsMessage = `**Extraktion abgeschlossen**\n\nDie Datei wurde erfolgreich verarbeitet.`;
              
              // Minimale Text-Nachricht, da die strukturierte Darstellung über messageData erfolgt
              if (results && results.extraction_data) {
                const summary = results.summary;
                resultsMessage += `\n\n**Extrahierte Elemente:** ${summary.total_colors} Farben, ${summary.total_fonts} Fonts, ${summary.total_pages} Seiten, ${summary.total_images} Bilder`;
              }
              
              const analysisSuccessMessage: ChatMessage = {
                id: `analysis-success-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
                message: resultsMessage,
                sender: 'agent',
                senderName: 'BrandChecker AI',
                avatarInitials: 'AI',
                timestamp: new Date(),
                messageType: 'extraction-results',
                messageData: results
              };
              setMessages(prev => [...prev, analysisSuccessMessage]);
              
              // Send complete extraction results to n8n webhook
              console.log('🚀 About to send to n8n webhook, results:', results);
              sendToN8nWebhook(results);
            }
            
            // Status nach 3 Sekunden zurücksetzen
            setTimeout(() => {
              setAnalysisStatus(null);
            }, 3000);
          }
        }
      } catch (error) {
        console.error('❌ Status polling error:', error);
        clearInterval(pollInterval);
      }
    }, 2000); // Alle 2 Sekunden pollen

    // Timeout nach 60 Sekunden
    setTimeout(() => {
      clearInterval(pollInterval);
      setAnalysisStatus(null);
    }, 60000);
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
      
      {/* Analysis Status Progress Bar */}
      {analysisStatus && (
        <div style={{
          position: 'fixed',
          bottom: '20px',
          left: '50%',
          transform: 'translateX(-50%)',
          backgroundColor: 'var(--color-background)',
          border: '1px solid var(--color-grey-800)',
          borderRadius: 'var(--border-radius-md)',
          padding: 'var(--space-4)',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          zIndex: 1000,
          minWidth: '300px',
          maxWidth: '500px'
        }}>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 'var(--space-2)'
          }}>
            <div style={{
              fontSize: 'var(--font-size-sm)',
              fontWeight: 'var(--font-weight-semibold)',
              color: 'var(--color-text-primary)'
            }}>
              Analyse läuft...
            </div>
            <ProgressBar
              value={analysisStatus.progress}
              variant="linear"
              size="md"
              showPercentage={true}
              color={analysisStatus.status === 'error' ? 'error' : 'primary'}
            />
            <div style={{
              fontSize: 'var(--font-size-xs)',
              color: 'var(--color-text-secondary)',
              textAlign: 'center'
            }}>
              {analysisStatus.message}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
