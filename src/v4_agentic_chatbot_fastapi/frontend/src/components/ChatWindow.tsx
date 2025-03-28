import { useState, useRef, useEffect } from 'react';


const ChatWindow = ({messages, setMessages, threadId, setThreadId}) => {
  const [inputMessage, setInputMessage] = useState('');
  // const [messages, setMessages] = useState<Message[]>([
  //   { content: 'Hello! How can I help you today?', isUser: false }
  // ]);
  // const [userInput, setUserInput] = useState('');
  // const [currentResponse, setCurrentResponse] = useState('');
  // const [threadId, setThreadId] = useState('');
  // const [isInitializing, setIsInitializing] = useState(true);
  // const websocket = useRef(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  

  // //establish wewb socket connection
  // useEffect(() => {
  //   // Generate new thread ID when component mounts
  //   const newThreadId = crypto.randomUUID();
  //   setThreadId(newThreadId);
    
  //   // Initialize WebSocket connection
  //   websocket.current = new WebSocket('ws://localhost:8000/chat/ws');
    
  //   websocket.current.onmessage = (event) => {
  //     const data = JSON.parse(event.data);
  //     if (data.type === 'chunk') {
  //       setCurrentResponse(prev => prev + data.content);
  //     } else if (data.type === 'complete') {
  //       setMessages(prev => [
  //         ...prev,
  //         { type: 'ai', content: currentResponse + data.content }
  //       ]);
  //       setCurrentResponse('');
  //     }
  //   }

  // });

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  
  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!inputMessage.trim()) return;

    // Add user message
    const userMessage = { content: inputMessage, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    
    // Simulate AI response (replace with actual API call)
    const aiResponse = { content: 'This is a mock AI response', isUser: false };
    
    setInputMessage('');
    
    // Add fake delay for realism
    setTimeout(() => {
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-screen bg-blue-50">
      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
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
        <div ref={messagesEndRef} />
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