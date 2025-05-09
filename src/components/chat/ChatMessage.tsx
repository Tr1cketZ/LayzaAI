import React from 'react';
import { CheckCircle, User } from 'lucide-react';
import { Message } from '../../types';
import { formatTime } from '../../utils/helpers';
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center mr-2 mt-1">
          <BrainIcon className="w-4 h-4 text-primary-500" />
        </div>
      )}
      
      <div className={`chat-bubble ${isUser ? 'chat-bubble-user' : 'chat-bubble-assistant'}`}>
        {message.attachments && message.attachments.length > 0 && (
          <div className="mb-2">
            {message.attachments.map(attachment => (
              <div key={attachment.id} className="mb-2">
                {attachment.type === 'image' && (
                  <img 
                    src={attachment.url} 
                    alt={attachment.filename}
                    className="max-w-full rounded-lg"
                  />
                )}
                {attachment.type === 'audio' && (
                  <audio 
                    src={attachment.url} 
                    controls 
                    className="max-w-full"
                  />
                )}
              </div>
            ))}
          </div>
        )}
        
        <div className="text-sm">
          {message.isLoading ? (
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
            </div>
          ) : (
            <ReactMarkdown
              components={{
                strong: ({ node, ...props }) => <span className="font-bold" {...props} />,
                em: ({ node, ...props }) => <span className="italic" {...props} />,
                p: ({ node, ...props }) => <p className="mb-2" {...props} />,
              }}
            >
              {message.content}
            </ReactMarkdown>
          )}
        </div>
        
        <div className="flex justify-end items-center mt-1 text-xs text-gray-500">
          <span>{formatTime(message.timestamp)}</span>
          {isUser && <CheckCircle className="w-3 h-3 ml-1 text-primary-500" />}
        </div>
      </div>
      
      {isUser && (
        <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center ml-2 mt-1">
          <User className="w-4 h-4 text-white" />
        </div>
      )}
    </div>
  );
};

// Brain icon component for the assistant
const BrainIcon: React.FC<{ className?: string }> = ({ className }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    strokeWidth="2" 
    strokeLinecap="round" 
    strokeLinejoin="round" 
    className={className}
  >
    <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-5 0v-8a2.5 2.5 0 0 1 2.5-2.5z" />
    <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 5 0v-8a2.5 2.5 0 0 0-2.5-2.5z" />
    <path d="M8 13a6 6 0 0 0 12 0" />
    <path d="M7 10.3C4.6 9.2 3 7.5 3 5.5a2.5 2.5 0 0 1 5 0" />
    <path d="M17 10.3c2.4-1.1 4-2.8 4-4.8a2.5 2.5 0 0 0-5 0" />
  </svg>
);

export default ChatMessage;