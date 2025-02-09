import { useState, useEffect, useRef } from "react";
import "./App.css";

const ChatInterface = () => {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatBoxRef = useRef(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    // Add user message
    const userMessage = { text: question, sender: "user" };
    setMessages(prev => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let botResponse = "";

      // Add initial bot message
      setMessages(prev => [...prev, { text: "", sender: "bot" }]);

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        botResponse += chunk;

        // Update bot message
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1] = {
            text: botResponse,
            sender: "bot"
          };
          return newMessages;
        });
      }
    } catch (error) {
      setMessages(prev => [
        ...prev,
        { text: "Error fetching response", sender: "bot" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <div className="chat-header">
          <h1>SQL Agent Chat</h1>
        </div>
        
        <div className="messages-container">
          <div className="chat-box" ref={chatBoxRef}>
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message ${msg.sender === "user" ? "user-message" : "bot-message"}`}
              >
                <div className="message-content">
                  <span className="message-sender">{msg.sender === "user" ? "You" : "Bot"}</span>
                  <div className="message-text">{msg.text}</div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="message bot-message loading-message">
                <div className="loading-dots">
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="input-wrapper">
          <form className="input-container" onSubmit={handleSubmit}>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={loading}
              placeholder="Type your message..."
            />
            <button type="submit" disabled={loading}>
              {loading ? <div className="spinner"></div> : "Send"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;