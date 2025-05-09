import React, { useState, useRef } from 'react';
import { Send, Mic, PaperclipIcon, X } from 'lucide-react';
import Button from '../ui/Button';
import { useStore } from '../../store';
import { uploadAudio, uploadImage } from '../../services/api';
import toast from 'react-hot-toast';

interface ChatInputProps {
  onSendMessage: (message: string, attachments?: { type: 'image' | 'audio', url: string, filename: string }[]) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(e.target.value);
  };
  
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };
  
  const handleSendMessage = async () => {
    if (!message.trim() && !selectedFile) return;
    
    let attachments = [];
    
    // Handle file upload if present
    if (selectedFile) {
      setIsUploading(true);
      try {
        const data = await uploadImage(selectedFile);
        if (!data.error) {
          attachments.push({
            type: 'image' as const,
            url: data.url,
            filename: selectedFile.name,
          });
        } else {
          toast.error('Falha ao enviar imagem. Tente novamente.');
        }
      } catch (error) {
        toast.error('Erro ao enviar imagem');
      } finally {
        setIsUploading(false);
      }
    }
    
    // Send message and reset state
    onSendMessage(message.trim(), attachments.length > 0 ? attachments : undefined);
    setMessage('');
    setSelectedFile(null);
    setPreviewUrl(null);
  };
  
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('A imagem deve ter no máximo 5MB');
      return;
    }
    
    // Check file type
    if (!file.type.startsWith('image/')) {
      toast.error('Apenas imagens são permitidas');
      return;
    }
    
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  };
  
  const handleRecordStart = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];
      
      mediaRecorder.ondataavailable = (e) => {
        audioChunksRef.current.push(e.data);
      };
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/mp3' });
        
        // Upload audio file
        setIsUploading(true);
        try {
          const data = await uploadAudio(audioBlob);
          if (!data.error) {
            onSendMessage('🎤 Áudio enviado', [
              {
                type: 'audio' as const,
                url: data.url,
                filename: 'gravacao.mp3',
              },
            ]);
          } else {
            toast.error('Falha ao enviar áudio. Tente novamente.');
          }
        } catch (error) {
          toast.error('Erro ao enviar áudio');
        } finally {
          setIsUploading(false);
        }
        
        // Stop all tracks in the stream
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorder.start();
      setIsRecording(true);
      
      // Auto stop after 30 seconds
      setTimeout(() => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
          stopRecording();
        }
      }, 30000);
      
    } catch (error) {
      console.error('Error accessing microphone:', error);
      toast.error('Não foi possível acessar o microfone');
    }
  };
  
  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };
  
  const handleClearFile = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };
  
  return (
    <div className="border-t bg-white p-4">
      {/* File preview */}
      {previewUrl && (
        <div className="mb-3 relative">
          <img 
            src={previewUrl} 
            alt="Preview" 
            className="h-20 object-cover rounded-lg border border-gray-200"
          />
          <button
            onClick={handleClearFile}
            className="absolute top-1 right-1 bg-gray-800 bg-opacity-70 rounded-full p-1 text-white"
            aria-label="Remover imagem"
          >
            <X size={14} />
          </button>
        </div>
      )}
      
      <div className="flex items-center space-x-2">
        {/* File upload button */}
        <Button
          variant="ghost"
          className="p-2 text-gray-600 hover:text-primary-500"
          onClick={() => fileInputRef.current?.click()}
          aria-label="Anexar imagem"
        >
          <PaperclipIcon size={20} />
        </Button>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={handleFileSelect}
        />
        
        {/* Recording button */}
        <Button
          variant="ghost"
          className={`p-2 ${isRecording ? 'text-red-500 animate-pulse' : 'text-gray-600 hover:text-primary-500'}`}
          onClick={isRecording ? stopRecording : handleRecordStart}
          aria-label={isRecording ? 'Parar gravação' : 'Iniciar gravação'}
        >
          <Mic size={20} />
        </Button>
        
        {/* Text input */}
        <div className="flex-1 relative">
          <input
            type="text"
            value={message}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder={isRecording ? "Gravando áudio... Clique no microfone para parar" : "Digite sua mensagem..."}
            className="w-full px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
            disabled={isRecording || isUploading}
          />
          {isRecording && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <div className="h-2 w-2 rounded-full bg-red-500 animate-pulse"></div>
            </div>
          )}
        </div>
        
        {/* Send button */}
        <Button
          variant="primary"
          className="rounded-full p-2 h-10 w-10 flex items-center justify-center"
          onClick={handleSendMessage}
          disabled={(!message.trim() && !selectedFile) || isRecording || isUploading}
          aria-label="Enviar mensagem"
          isLoading={isUploading}
        >
          <Send size={18} />
        </Button>
      </div>
      
      {isRecording && (
        <div className="text-xs text-center mt-2 text-red-500">
          Gravando áudio (máx. 30 segundos)
        </div>
      )}
    </div>
  );
};

export default ChatInput;