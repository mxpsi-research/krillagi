// AgenticChat.tsx
"use client"

import React, { useState, useEffect, ChangeEvent, FormEvent } from "react";
import { fetchOllamaModels } from "../utils/ollama";
import { API_URL } from "../utils/api";

type Message = {
  role: "user" | "agent" | "orchestrator" | "error";
  text: string;
  agent?: string;
  time?: number;
};

interface AgenticChatProps {
  onSessionCreated: (sessionId: number) => void;
}

const AgenticChat: React.FC<AgenticChatProps> = ({ onSessionCreated }) => {
  const [input, setInput] = useState<string>("");
  const [sessionName, setSessionName] = useState<string>("");
  const [topic, setTopic] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [models, setModels] = useState<string[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>("");

  useEffect(() => {
    fetchOllamaModels().then(setModels).catch(() => setModels([]));
  }, []);

  const handleStartChat = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setMessages((msgs: Message[]) => [...msgs, { role: "user", text: input }]);
    let data: any;
    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input, session_name: sessionName, topic, model: selectedModel }),
      });
      data = await res.json();
      setMessages((msgs: Message[]) => [...msgs, { role: "orchestrator", text: "Orchestrator decomposed your prompt into agent tasks." }]);
      data.subtasks.forEach((subtask: any, idx: number) => {
        setMessages((msgs: Message[]) => [...msgs, {
          role: "agent",
          agent: data.results[idx].agent,
          text: `Agent '${data.results[idx].agent}' is working on: ${subtask.prompt}`,
          time: data.results[idx].time
        }]);
        setMessages((msgs: Message[]) => [...msgs, {
          role: "agent",
          agent: data.results[idx].agent,
          text: `Result: ${data.results[idx].result}`,
          time: data.results[idx].time
        }]);
      });
      setMessages((msgs: Message[]) => [...msgs, { role: "orchestrator", text: `Orchestrator aggregated results: ${data.output}` }]);
      if (onSessionCreated) onSessionCreated(data.session_id);
      setInput("");
    } catch (err: any) {
      setMessages((msgs: Message[]) => [...msgs, { role: "error", text: `Error: ${err.message || err}` }]);
    }
    setLoading(false);
  };

  return (
    <div className="bg-white p-4 rounded shadow border border-gray-200 flex flex-col h-full">
      <h2 className="text-xl font-semibold mb-2">Agentic Chat</h2>
      <div className="mb-2 flex gap-2">
        <select
          className="border border-gray-300 rounded px-2 py-1 flex-1"
          value={selectedModel}
          onChange={e => setSelectedModel(e.target.value)}
        >
          <option value="">Select Ollama model...</option>
          {models.map(m => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>
        <input
          className="border border-gray-300 rounded px-2 py-1 flex-1"
          type="text"
          value={sessionName}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setSessionName(e.target.value)}
          placeholder="Session name (optional)"
        />
        <input
          className="border border-gray-300 rounded px-2 py-1 flex-1"
          type="text"
          value={topic}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setTopic(e.target.value)}
          placeholder="Topic (optional)"
        />
      </div>
      <div className="flex-1 overflow-y-auto mb-2 bg-gray-50 rounded p-2" style={{ minHeight: 200 }}>
        {messages.map((msg: Message, idx: number) => (
          <div key={idx} className={`mb-3 flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-lg px-3 py-2 rounded shadow-sm ${msg.role === "user" ? "bg-blue-100 text-blue-900" : msg.role === "agent" ? "bg-green-100 text-green-900" : msg.role === "orchestrator" ? "bg-yellow-100 text-yellow-900" : "bg-red-100 text-red-900"}`}>
              {msg.role === "agent" && <span className="font-bold mr-1">{msg.agent}:</span>}
              {msg.text}
              {msg.time && <span className="ml-2 text-xs text-gray-500">({msg.time}s)</span>}
            </div>
          </div>
        ))}
        {loading && (
          <div className="mb-3 flex justify-start">
            <div className="max-w-lg px-3 py-2 rounded shadow-sm bg-yellow-100 text-yellow-900">Agents are working...</div>
          </div>
        )}
      </div>
      <form
        className="flex gap-2"
        onSubmit={(e: FormEvent<HTMLFormElement>) => {
          e.preventDefault();
          handleStartChat();
        }}
      >
        <input
          className="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-400 bg-white text-gray-900"
          type="text"
          value={input}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded font-semibold hover:bg-blue-700 disabled:opacity-50"
          disabled={loading || !input.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default AgenticChat;
