import React, { useState } from 'react';
import { useChatKit, ChatKitProvider, MessageList, MessageInput } from '@openai/chatkit-react';
import { MessageCircle, X } from 'lucide-react';

const ChatInterface = () => {
  const chatkit = useChatKit({
    api: {
      getClientSecret: async () => {
        const res = await fetch('/api/chatkit/session', { method: 'POST' });
        if (!res.ok) throw new Error('Failed to fetch session');
        const data = await res.json();
        return data.client_secret;
      },
    },
  });

  return (
    <div className="flex flex-col h-[500px] w-[400px] bg-white border border-gray-200 rounded-lg shadow-xl overflow-hidden">
      <div className="bg-blue-600 p-4 text-white font-bold flex justify-between items-center">
        <span>Todo AI Assistant</span>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <MessageList
          chatkit={chatkit}
          theme={{
            variant: 'minimal',
            colorScheme: 'light'
          }}
        />
      </div>

      <div className="p-4 border-t border-gray-100">
        <MessageInput
          chatkit={chatkit}
          placeholder="Ask me to add, list, or complete tasks..."
        />
      </div>
    </div>
  );
};

export const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="relative">
          <ChatInterface />
          <button
            onClick={() => setIsOpen(false)}
            className="absolute -top-3 -right-3 bg-gray-100 p-1 rounded-full border border-gray-300 hover:bg-gray-200 transition-colors"
          >
            <X size={16} />
          </button>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-all transform hover:scale-105 flex items-center justify-center"
        >
          <MessageCircle size={24} />
        </button>
      )}
    </div>
  );
};
