import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Conversation, Message, StudentProgress, Subject } from '../types';
import { generateId, getWelcomeMessage } from '../utils/helpers';

interface ChatState {
  conversations: Conversation[];
  activeConversationId: string | null;
  isRecording: boolean;
  isProcessing: boolean;
  studentProgress: StudentProgress[];
  
  // Actions
  startNewConversation: (subject: Subject) => string;
  setActiveConversation: (id: string | null) => void;
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void;
  updateMessage: (id: string, updates: Partial<Message>) => void;
  setIsRecording: (value: boolean) => void;
  setIsProcessing: (value: boolean) => void;
  updateProgress: (subject: Subject, questionsAnswered?: number) => void;
}

export const useStore = create<ChatState>()(
  persist(
    (set, get) => ({
      conversations: [],
      activeConversationId: null,
      isRecording: false,
      isProcessing: false,
      studentProgress: [],
      
      startNewConversation: (subject) => {
        const id = generateId();
        const welcomeMessage = getWelcomeMessage(subject);
        const newConversation: Conversation = {
          id,
          subject,
          title: `Nova conversa - ${new Date().toLocaleDateString('pt-BR')}`,
          messages: [welcomeMessage],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };
        
        set((state) => ({
          conversations: [newConversation, ...state.conversations],
          activeConversationId: id,
        }));
        
        return id;
      },
      
      setActiveConversation: (id) => {
        set({ activeConversationId: id });
      },
      
      addMessage: (messageData) => {
        const { activeConversationId, conversations } = get();
        
        if (!activeConversationId) return;
        
        const message: Message = {
          ...messageData,
          id: generateId(),
          timestamp: new Date().toISOString(),
        };
        
        set({
          conversations: conversations.map((conversation) => 
            conversation.id === activeConversationId
              ? {
                  ...conversation,
                  messages: [...conversation.messages, message],
                  updatedAt: new Date().toISOString(),
                }
              : conversation
          ),
        });
      },
      
      updateMessage: (id, updates) => {
        const { activeConversationId, conversations } = get();
        
        if (!activeConversationId) return;
        
        set({
          conversations: conversations.map((conversation) => 
            conversation.id === activeConversationId
              ? {
                  ...conversation,
                  messages: conversation.messages.map((message) => 
                    message.id === id ? { ...message, ...updates } : message
                  ),
                }
              : conversation
          ),
        });
      },
      
      setIsRecording: (value) => {
        set({ isRecording: value });
      },
      
      setIsProcessing: (value) => {
        set({ isProcessing: value });
      },
      
      updateProgress: (subject, questionsAnswered) => {
        const { studentProgress } = get();
        const now = new Date().toISOString();
        
        const existingProgress = studentProgress.find(p => p.subject === subject);
        
        if (existingProgress) {
          set({
            studentProgress: studentProgress.map(p => 
              p.subject === subject
                ? { 
                    ...p, 
                    questionsAnswered: questionsAnswered 
                      ? questionsAnswered 
                      : p.questionsAnswered + 1,
                    lastActive: now,
                  }
                : p
            ),
          });
        } else {
          set({
            studentProgress: [
              ...studentProgress,
              {
                subject,
                questionsAnswered: questionsAnswered || 1,
                lastActive: now,
              },
            ],
          });
        }
      },
    }),
    {
      name: 'layza-chat-storage',
    }
  )
);