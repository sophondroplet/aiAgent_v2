import { useState, useRef, useEffect } from 'react';
import React from 'react';

const ChatWindow = ({websocket, message_history, setMessage_history, threadId}) => {
  const [inputMessage, setInputMessage] = useState('');
  const messageEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [message_history]);

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!inputMessage.trim()) return;

    // Add user message to hisory
    const userMessage = { content: inputMessage, isUser: true };
    setMessage_history(prev => [...prev, userMessage]);
    
    // Simulate AI response (replace with actual API call)
    const aiResponse = { content: 'This is a mock AI response', isUser: false };
    
    const message = {
      thread_id: threadId,
      user_input: inputMessage,
    };

    if (websocket.current.readyState === WebSocket.OPEN) {
      websocket.current.send(JSON.stringify(message));
    }

    setInputMessage('');
    
    // Add fake delay for realism
    setTimeout(() => {
      setMessage_history(prev => [...prev, aiResponse]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-screen bg-blue-50">
      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {message_history.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xl p-4 rounded-lg ${
                message.isUser
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-800 shadow-md'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        <div ref={messageEndRef} />
      </div>

      {/* Input Area */}
      <form 
        onSubmit={handleSubmit}
        className="border-t bg-white p-4 sticky bottom-0"
      >
        <div className="flex gap-2 max-w-4xl mx-auto">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            autoFocus
          />
          <button
            type="submit"
            className="px-4 py-2 bg-red text-red rounded-lg hover:bg-blue-600 transition-colors"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatWindow;