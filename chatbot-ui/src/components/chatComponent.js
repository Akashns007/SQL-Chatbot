import React, { useState, useEffect } from "react";

const ChatComponent = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/chat");
        ws.onmessage = (event) => {
            setMessages((prev) => [...prev, { text: event.data, sender: "bot" }]);
        };
        setSocket(ws);
        return () => ws.close();
    }, []);

    const sendMessage = () => {
        if (socket && input.trim()) {
            setMessages([...messages, { text: input, sender: "user" }]);
            socket.send(input);
            setInput("");
        }
    };

    return (
        <div>
            <div>
                {messages.map((msg, index) => (
                    <p key={index} style={{ textAlign: msg.sender === "user" ? "right" : "left" }}>
                        <strong>{msg.sender}:</strong> {msg.text}
                    </p>
                ))}
            </div>
            <input value={input} onChange={(e) => setInput(e.target.value)} />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default ChatComponent;
