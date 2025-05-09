import React from 'react';
import ChatContainer from '../components/chat/ChatContainer';

const ChatPage: React.FC = () => {
  return (
    <div className="h-[calc(100vh-64px)]">
      <ChatContainer />
    </div>
  );
};

export default ChatPage;