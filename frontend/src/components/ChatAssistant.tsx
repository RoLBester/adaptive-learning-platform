// frontend/src/components/ChatAssistant.tsx
import React, { useState } from "react";
import apiClient from "../api/apiClient.ts";

interface ChatMessage {
  sender: "user" | "bot";
  text: string;
}

const ChatAssistant: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    // 1) Adds user's message to local state
    const userMsg: ChatMessage = { sender: "user", text: trimmed };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");

    try {
      // 2) Sends entire conversation (just the text part) to the backend
      const response = await apiClient.post("/api/chat/", {
        conversation: newMessages.map((msg) => msg.text),
      });
      // 3) The backend returns { reply: "some text" } or { error: "..." }
      if (response.data.reply) {
        const botMsg: ChatMessage = {
          sender: "bot",
          text: response.data.reply,
        };
        setMessages([...newMessages, botMsg]);
      } else if (response.data.error) {
        const errorMsg: ChatMessage = {
          sender: "bot",
          text: `Error: ${response.data.error}`,
        };
        setMessages([...newMessages, errorMsg]);
      }
    } catch (err) {
      console.error("Error sending chat message:", err);
      // Optionally shows an error message in the conversation
      const errorMsg: ChatMessage = {
        sender: "bot",
        text: "Error calling AI service.",
      };
      setMessages([...newMessages, errorMsg]);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow max-w-3xl mx-auto h-[80vh] flex flex-col">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">AI Chat</h2>
      <div className="flex-grow overflow-auto mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`my-2 flex ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`px-4 py-2 rounded-md max-w-xs ${
                msg.sender === "user"
                  ? "bg-indigo-600 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </div>
      <div className="flex">
        <input
          className="border border-gray-300 rounded-l px-3 py-2 w-full focus:outline-none"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          className="bg-indigo-600 text-white px-4 py-2 rounded-r hover:bg-indigo-700 transition"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatAssistant;
