import React, { useState, useRef, useEffect } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatInterfaceProps {
  onTaskUpdate?: () => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ onTaskUpdate }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: userMessage,
          conversation_id: conversationId
        })
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || 'Failed to send message');
      }

      const data = await response.json();
      setConversationId(data.conversation_id);
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);

      // Refresh task list if the response indicates a successful task operation
      if (data.response && (
        data.response.includes('✓ Task added:') ||
        data.response.includes('✓ Completed:') ||
        data.response.includes('✓ Deleted:') ||
        data.response.includes('Current tasks:')
      )) {
        // Call the callback to refresh tasks in the main page
        onTaskUpdate?.();
      }
    } catch (error: any) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${error.message}. Make sure you've set up your Google API key!`
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '500px',
      width: '400px',
      backgroundColor: 'white',
      border: '1px solid #e5e7eb',
      borderRadius: '8px',
      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
      overflow: 'hidden'
    }}>
      {/* Header */}
      <div style={{
        backgroundColor: '#2563eb',
        padding: '16px',
        color: 'white',
        fontWeight: 'bold'
      }}>
        <div>Todo AI Assistant</div>
        <div style={{ fontSize: '12px', fontWeight: 'normal', marginTop: '4px', opacity: 0.9 }}>
          Powered by Google Gemini
        </div>
      </div>

      {/* Messages */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '16px',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }}>
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: '#6b7280', marginTop: '32px' }}>
            <p style={{ marginBottom: '8px' }}>👋 Hi! I can help you manage your tasks.</p>
            <p style={{ fontSize: '14px' }}>Try saying:</p>
            <div style={{ fontSize: '12px', marginTop: '8px' }}>
              <p>• "Add task buy groceries"</p>
              <p>• "List my tasks"</p>
              <p>• "Complete groceries"</p>
              <p>• "Delete task groceries"</p>
            </div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              display: 'flex',
              justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
            }}
          >
            <div
              style={{
                maxWidth: '80%',
                borderRadius: '8px',
                padding: '12px 16px',
                backgroundColor: msg.role === 'user' ? '#2563eb' : '#f3f4f6',
                color: msg.role === 'user' ? 'white' : '#111827'
              }}
            >
              <div style={{ fontSize: '14px', whiteSpace: 'pre-wrap' }}>{msg.content}</div>
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
            <div style={{
              backgroundColor: '#f3f4f6',
              borderRadius: '8px',
              padding: '12px 16px'
            }}>
              <div style={{ display: 'flex', gap: '8px' }}>
                <div style={{
                  width: '8px',
                  height: '8px',
                  backgroundColor: '#9ca3af',
                  borderRadius: '50%',
                  animation: 'bounce 1s infinite'
                }}></div>
                <div style={{
                  width: '8px',
                  height: '8px',
                  backgroundColor: '#9ca3af',
                  borderRadius: '50%',
                  animation: 'bounce 1s infinite 0.1s'
                }}></div>
                <div style={{
                  width: '8px',
                  height: '8px',
                  backgroundColor: '#9ca3af',
                  borderRadius: '50%',
                  animation: 'bounce 1s infinite 0.2s'
                }}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div style={{
        padding: '16px',
        borderTop: '1px solid #f3f4f6'
      }}>
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            style={{
              flex: 1,
              padding: '8px 16px',
              border: '1px solid #d1d5db',
              borderRadius: '8px',
              fontSize: '14px',
              outline: 'none'
            }}
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            style={{
              backgroundColor: loading || !input.trim() ? '#d1d5db' : '#2563eb',
              color: 'white',
              padding: '8px 16px',
              borderRadius: '8px',
              border: 'none',
              cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
              fontSize: '14px',
              fontWeight: '500'
            }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

interface SimpleChatWidgetProps {
  onTaskUpdate?: () => void;
}

export const SimpleChatWidget: React.FC<SimpleChatWidgetProps> = ({ onTaskUpdate }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div style={{
      position: 'fixed',
      bottom: '24px',
      right: '24px',
      zIndex: 50
    }}>
      {isOpen ? (
        <div style={{ position: 'relative' }}>
          <ChatInterface onTaskUpdate={onTaskUpdate} />
          <button
            onClick={() => setIsOpen(false)}
            style={{
              position: 'absolute',
              top: '-12px',
              right: '-12px',
              backgroundColor: '#f3f4f6',
              padding: '4px',
              borderRadius: '50%',
              border: '1px solid #d1d5db',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '24px',
              height: '24px'
            }}
          >
            ✕
          </button>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          style={{
            backgroundColor: '#2563eb',
            color: 'white',
            padding: '16px',
            borderRadius: '50%',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            border: 'none',
            cursor: 'pointer',
            transition: 'all 0.3s',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '60px',
            height: '60px',
            fontSize: '24px'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.backgroundColor = '#1d4ed8';
            e.currentTarget.style.transform = 'scale(1.05)';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.backgroundColor = '#2563eb';
            e.currentTarget.style.transform = 'scale(1)';
          }}
        >
          💬
        </button>
      )}
    </div>
  );
};
