import { useState, useRef, useEffect, use } from 'react';
import React from 'react';
import './App.css'
import ChatWindow from './components/ChatWindow';

interface Message_history{
  type: string;
  content: string;
}

function App() {

  const [message_history, setMessage_history] = useState<Message_history[]>(
      [{type: 'assistant', 
        content: 'Hello! How can I help you today?'}]
    );
  const [rxBuffer, setRxBuffer] = useState('');
  const [threadId, setThreadId] = useState('');
  const websocket = useRef<WebSocket | null>(null);
  
//notify backend of client startup and initalize server
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
          setMessage_history(data.message_history);

        } catch (error) {
          console.error('Initialization error:', error);
        }
      };
  
      initializeChat();
    }, []);


  //Establish a websocket connection to the backend server
  
  useEffect(() => {
    // Initialize WebSocket connection
    websocket.current = new WebSocket('ws://localhost:8000/chat/ws');
    
    websocket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'chunk') {
        setRxBuffer(prev => prev + data.content);
      } else if (data.type === 'complete') {
        setMessage_history(prev => [
        ...prev,
        { type: 'ai', content: rxBuffer + data.content }
        ]);
        setRxBuffer('');
      }
    }

  });


  return (
    <div className="max-w-4xl mx-auto h-screen">
      <h1 className="text-2xl font-bold p-4 bg-white border-b">AI Companion</h1>
      <ChatWindow message_history={message_history} setMessage_history={setMessage_history} threadId={threadId} websocket={websocket}/>
    </div>
  );
}

export default App
