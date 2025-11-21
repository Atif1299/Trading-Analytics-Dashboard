/**
 * Chat Interface Component
 * Simple AI chat for asking questions about trading data
 */
import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, Loader, Sparkles } from 'lucide-react';
import apiService from '../services/api';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I can help you analyze your trading data. Ask me anything like "Show me strong uptrend stocks" or "What\'s the average sentiment?"'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  const scrollToBottom = () => {
    if (chatContainerRef.current && messagesEndRef.current) {
      // Scroll within the container, not the entire page
      const container = chatContainerRef.current;
      const element = messagesEndRef.current;
      const containerRect = container.getBoundingClientRect();
      const elementRect = element.getBoundingClientRect();
      
      // Only scroll if the element is not fully visible in the container
      if (elementRect.bottom > containerRect.bottom) {
        element.scrollIntoView({ behavior: 'smooth', block: 'end' });
      }
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);

    // Get AI response
    setLoading(true);
    try {
      const response = await apiService.chat(userMessage);
      
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: response.response,
          data: response.data
        }
      ]);
    } catch (error) {
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please make sure the backend is running and you\'ve synced the data.'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Quick suggestion buttons
  const suggestions = [
    "Show me strong uptrend stocks",
    "What's the average sentiment?",
    "List high volatility stocks",
    "Top 5 performing stocks"
  ];

  const handleSuggestion = (suggestion) => {
    setInput(suggestion);
  };

  return (
    <div className="card flex flex-col h-[600px]">
      {/* Header */}
      <div className="flex items-center gap-2 mb-4 pb-4 border-b">
        <div className="p-2 bg-primary-100 rounded-lg">
          <Sparkles className="w-5 h-5 text-primary-600" />
        </div>
        <div>
          <h3 className="text-lg font-bold">AI Trading Assistant</h3>
          <p className="text-sm text-gray-500">Ask questions about your trading data</p>
        </div>
      </div>

      {/* Messages */}
      <div ref={chatContainerRef} className="flex-1 overflow-y-auto space-y-4 mb-4 scroll-smooth">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                message.role === 'user'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              
              {/* Show data if available */}
              {message.data && message.data.length > 0 && (
                <div className="mt-2 pt-2 border-t border-gray-300">
                  <p className="text-xs font-semibold mb-1">Found {message.data.length} stocks:</p>
                  <div className="space-y-1 max-h-48 overflow-y-auto">
                    {message.data.map((stock, i) => (
                      <p key={i} className="text-xs">
                        {stock.Symbol || stock.symbol} - {stock.Trend || stock.trend}
                      </p>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-3">
              <Loader className="w-5 h-5 animate-spin text-primary-600" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggestions */}
      {messages.length === 1 && (
        <div className="mb-3 flex flex-wrap gap-2">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestion(suggestion)}
              className="text-xs px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-gray-700 transition-colors"
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about your trading data..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="btn-primary px-4"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
