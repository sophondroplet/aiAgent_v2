import { useState, useRef, useEffect} from 'react';
import './App.css'
import ChatWindow from './components/ChatWindow';
import { Message } from './types';

function App() {
  const [message_history, setMessage_history] = useState<Message[]>([
    {
      type: 'assistant', 
      content: 'Hello! How can I help you today?'
    }
  ]);
  const [threadId, setThreadId] = useState('');
  const websocket = useRef<WebSocket | null>(null);
  
  //notify backend of client startup and initialize server
  useEffect(() => {
    const initializeChat = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/init', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        const data = await response.json();
        setThreadId(data.thread_id);
        setMessage_history(prev => [...prev, ...data.messages]);
      } catch (error) {
        console.error('Initialization error:', error);
      }
    };

    initializeChat();
  }, []);

  //Establish a websocket connection to the backend server
  useEffect(() => {
    if (!threadId) return; // Only connect when we have a threadId

    // Initialize WebSocket connection
    const ws = new WebSocket('ws://localhost:8000/chat/ws');
    websocket.current = ws;
    
    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    //process incoming messages from backend
    ws.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data);
      if (data.type === 'chunk') {
        // Update the last message if it's from assistant, or create a new one
        setMessage_history(prev => {
          const lastMessage = prev[prev.length - 1];
          if (lastMessage?.type === 'assistant' && !lastMessage.isComplete) {
            const newMessages = [...prev];
            newMessages[prev.length - 1] = {
              ...lastMessage,
              content: data.content
            };
            return newMessages;
          } else {
            return [...prev, { type: 'assistant', content: data.content, isComplete: false }];
          }
        });
      } else if (data.type === 'complete') {
        // Mark the last message as complete and remove any cursor indicator
        setMessage_history(prev => {
          const newMessages = [...prev];
          const lastMessage = newMessages[prev.length - 1];
          if (lastMessage?.type === 'assistant') {
            newMessages[prev.length - 1] = {
              ...lastMessage,
              content: data.content,
              isComplete: true
            };
          } 
          return newMessages;
        });
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return
  }, [threadId]); // Only reconnect when threadId changes

  return (
    <div className="max-w-4xl mx-auto h-screen">
      <h1 className="text-2xl font-bold p-4 bg-white border-b">AI Companion</h1>
      <ChatWindow message_history={message_history} setMessage_history={setMessage_history} threadId={threadId} websocket={websocket}/>
    </div>
  );
}

export default App;
