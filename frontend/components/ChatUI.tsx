// ChatUI.tsx
import { useState, useEffect, useRef } from "react";
import { fetchSessionHistory, postFeedback } from "../utils/api";

export default function ChatUI({ sessionId, onDeleteMessage }: { sessionId: number | null, onDeleteMessage: (msgIdx: number) => void }) {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (sessionId !== null) {
      fetchSessionHistory(sessionId).then(setMessages).catch(console.error);
    }
  }, [sessionId]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || sessionId === null) return;
    setLoading(true);
    // Simulate sending prompt to backend (replace with actual API call)
    // Here, just add to messages for demo
    setMessages((msgs) => [...msgs, { prompt: input, response: "(pending...)" }]);
    setInput("");
    setLoading(false);
    // TODO: Call backend to process chat and update history
  };

  return (
    <div className="flex flex-col h-full bg-white border-r border-gray-200">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, idx) => (
          <div key={idx} className="mb-4">
            <div className="flex justify-between items-center">
              <span className="font-semibold text-blue-700">You:</span>
              <button className="text-xs text-red-500 ml-2" onClick={() => onDeleteMessage(idx)}>Delete</button>
            </div>
            <div className="bg-gray-100 rounded p-2 mt-1 text-gray-900">{msg.prompt}</div>
            <div className="mt-2 flex justify-between items-center">
              <span className="font-semibold text-green-700">Agent:</span>
            </div>
            <div className="bg-blue-50 rounded p-2 mt-1 text-gray-900">{msg.response}</div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <div className="p-4 border-t border-gray-200 bg-white">
        <form
          className="flex"
          onSubmit={e => {
            e.preventDefault();
            handleSend();
          }}
        >
          <input
            className="flex-1 border border-gray-300 rounded px-3 py-2 mr-2 focus:outline-none focus:ring focus:border-blue-400 bg-white text-gray-900"
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
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
    </div>
  );
}
