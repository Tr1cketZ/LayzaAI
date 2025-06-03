import React, { useEffect, useRef, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import ChatFeedback from './ChatFeedback';
import { useStore } from '../../store';
import { Subject } from '../../types';
import { getRandomLoadingMessage, getSubjectName } from '../../utils/helpers';
import { sendMessage } from '../../services/api';
import { Sparkle } from 'lucide-react';
import { motion } from 'framer-motion';

const ChatContainer: React.FC = () => {
  const { subject } = useParams<{ subject: string }>();
  const navigate = useNavigate();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  
  const {
    conversations,
    activeConversationId,
    startNewConversation,
    addMessage,
    updateMessage,
    updateProgress,
  } = useStore();
  
  // Initialize chat with the correct subject
  useEffect(() => {
    if (!subject) return;
    
    // Validate subject
    if (!['math', 'science', 'portuguese'].includes(subject)) {
      navigate('/');
      return;
    }
    
    // Start a new conversation if none exists
    if (!activeConversationId) {
      startNewConversation(subject as Subject);
    }
  }, [subject, activeConversationId, startNewConversation, navigate]);
  
  // Get active conversation
  const activeConversation = activeConversationId
    ? conversations.find(c => c.id === activeConversationId)
    : null;
  
  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [activeConversation?.messages]);
  
  // Handle scroll to show feedback
  useEffect(() => {
    if (!activeConversation || activeConversation.messages.length < 4) return;
    
    // Show feedback after a meaningful conversation
    if (activeConversation.messages.length >= 6 && !showFeedback) {
      setShowFeedback(true);
    }
  }, [activeConversation, showFeedback]);
  
  // Handle chat scroll
  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const { scrollTop } = e.currentTarget;
    setIsScrolled(scrollTop > 50);
  };
  
  // Handle sending new message
  const handleSendMessage = async (message: string, attachments?: { type: 'image' | 'audio', url: string, filename: string }[]) => {
    if (!activeConversationId || !subject) return;
    
    // Add user message
    addMessage({
      role: 'user',
      content: message,
      attachments,
    });
    
    // Add loading message from assistant
    const loadingMessageId = Date.now().toString();
    addMessage({
      id: loadingMessageId,
      role: 'assistant',
      content: getRandomLoadingMessage(),
      isLoading: true,
    });
    
    try {
      // Send to API
      const response = await sendMessage(message, subject);
      
      // Update the loading message with the real response
      updateMessage(loadingMessageId, {
        content: response.response || 'Desculpe, não consegui processar sua mensagem.',
        isLoading: false,
      });
      
      // Update progress
      updateProgress(subject as Subject);
      
    } catch (error) {
      // Handle error
      updateMessage(loadingMessageId, {
        content: 'Ops, tive um probleminha para te responder agora. Pode tentar de novo? 😅',
        isLoading: false,
      });
    }
  };
  
  if (!activeConversation) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-pulse text-gray-500">Carregando...</div>
      </div>
    );
  }
  
  return (
    <div className="flex flex-col h-full max-h-[calc(100vh-4rem)]">
      {/* Chat header */}
      <div className="bg-white border-b py-3 px-4 sticky top-0 z-10">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-bold text-gray-800">
            {getSubjectName(subject as Subject)}
          </h1>
          <Sparkle className="h-5 w-5 text-primary-500" />
        </div>
      </div>
      
      {/* Chat messages */}
      <div 
        className="flex-1 overflow-y-auto px-4 py-4 bg-gray-50"
        onScroll={handleScroll}
      >
        {activeConversation.messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
        
        {showFeedback && (
          <ChatFeedback conversationId={activeConversation.id} />
        )}
      </div>
      
      {/* Scroll to bottom button */}
      {isScrolled && (
        <motion.button
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 10 }}
          className="absolute bottom-24 right-6 bg-primary-500 text-white rounded-full p-2 shadow-lg hover:bg-primary-600 transition-colors"
          onClick={() => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })}
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </motion.button>
      )}
      
      {/* Chat input */}
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatContainer;