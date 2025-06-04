import React, { useState, useEffect } from 'react';
import ChatContainer from './components/ChatContainer';
import HistorySection from './components/HistorySection';
import SplashScreen from './components/SplashScreen';
import './App.css';

function App() 
{
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showSplash, setShowSplash] = useState(true);

  // API base URL - use environment variable or default to localhost in development
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

  useEffect(() => {
    const fetchHistory = async () => {
      try 
      {
        const response = await fetch(`${API_URL}/api/history`);

        if (!response.ok) throw new Error('Failed to fetch history');

        const data = await response.json();
        setHistory(data.map(item => item.question));

      } 
      catch (error) 
      {
        console.error('Error fetching history:', error);
      }
    };
    
    fetchHistory();
  }, []);

  const handleSendMessage = async () => 
  {
    if (input.trim() === '') return;

    const userMessage = {
      content: input,
      role: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setInput('');

    try 
    {
      const response = await fetch(`${API_URL}/api/ask`, 
      {
        method: 'POST',
        headers: 
        {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: input })
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();

      const aiMessage = 
      {
        content: data.answer,
        role: 'assistant',
      };

      setMessages(prev => [...prev, aiMessage]);
      setHistory(prev => [input, ...prev]);

    } 
    catch (error) 
    {
      console.error('Error:', error);

      const errorMessage = 
      {
        content: 'Sorry, there was an error processing your request.',
        role: 'assistant'
      };

      setMessages(prev => [...prev, errorMessage]);

    } 
    finally 
    {
      setIsLoading(false);
    }
  };

  const handleHistoryClick = (prompt) => {
    setInput(prompt);
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  return (
    <>
      {showSplash && <SplashScreen onFinished={() => setShowSplash(false)} />}
      <div className="app-container">
        <div className="app-header">
          <div className="logo-container">
            <span className="logo-text">RIT</span>
            <span className="logo-text-secondary">Buddy</span>
          </div>
          <div className="tagline">Your AI Campus Assistant</div>
        </div>
        <div className="main-content">
          <div className="chat-column">
            <ChatContainer 
              messages={messages} 
              input={input} 
              setInput={setInput} 
              handleSendMessage={handleSendMessage} 
              isLoading={isLoading}
            />
          </div>
          <div className="history-column">
            <h2>Conversation History</h2>
            <HistorySection 
              history={history} 
              handleHistoryClick={handleHistoryClick} 
              handleClearChat={handleClearChat} 
            />
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
