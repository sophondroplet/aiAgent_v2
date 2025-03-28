import { useState, useRef, useEffect } from 'react';
import './App.css'
import ChatWindow from './components/ChatWindow';


function App() {

  const [messages, setMessages] = useState([
      { content: 'Hello! How can I help you today?', isUser: false }
    ]);
  const [userInput, setUserInput] = useState('');
  const [currentResponse, setCurrentResponse] = useState('');
  const [threadId, setThreadId] = useState('');
  
  useEffect(() => {
      const initializeChat = async () => {
        try {
          const response = await fetch('/api/init', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
          });
          
          const data = await response.json();
          setThreadId(data.thread_id);
          setMessages(data.messages || []);

          console.log(threadId, messages)

        } catch (error) {
          console.error('Initialization error:', error);
        }
      };
  
      initializeChat();
    }, []);

  return (
    <div className="max-w-4xl mx-auto h-screen">
      <h1 className="text-2xl font-bold p-4 bg-white border-b">AI Companion</h1>
      <ChatWindow userInput={userInput} setUserInput={setUserInput} messages={messages} setMessages={setMessages} currentResponse={currentResponse} setCurrentResponse={setCurrentResponse} threadId={threadId} setThreadId={setThreadId}/>
    </div>
  );
}

export default App
