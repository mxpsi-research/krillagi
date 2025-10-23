"use client"

import { useEffect, useState } from "react";

import TaskFlowGraph from "../components/TaskFlowGraph";
import AgenticChat from "../components/AgenticChat";
import { fetchSessions, fetchAnalytics, fetchAgents } from "../utils/api";

export default function Dashboard() {
  const [sessions, setSessions] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<any[]>([]);
  const [agents, setAgents] = useState<any[]>([]);
  const [activeSession, setActiveSession] = useState<number | null>(null);

  useEffect(() => {
    fetchSessions().then(setSessions).catch(console.error);
    fetchAgents().then(setAgents).catch(console.error);
  }, []);

  // Polling for analytics and agentic results
  useEffect(() => {
    if (!activeSession) return;
    const interval = setInterval(() => {
      fetchAnalytics(activeSession).then(setAnalytics).catch(console.error);
      // Optionally, fetch other agentic results here
    }, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, [activeSession]);

  // Delete message handler for ChatUI (stub)
  const handleDeleteMessage = (msgIdx: number) => {
    // TODO: Implement backend deletion and update state
  };

  return (
    <main className="min-h-screen bg-white text-gray-900">
      <h1 className="text-3xl font-bold mb-6 text-center">krillAGI Dashboard</h1>
      <div className="flex gap-6 max-w-7xl mx-auto">
        {/* Left column: Agentic Chat */}
        <div className="w-1/3 flex flex-col border-r border-gray-200 bg-white">
          <section className="p-4">
            <AgenticChat onSessionCreated={setActiveSession} />
          </section>
          {/* Optionally, show session list and ChatUI for legacy/history */}
          <section className="p-4">
            <h2 className="text-xl font-semibold mb-2">Sessions</h2>
            <ul className="mb-4">
              {sessions.map((s) => (
                <li key={s.id} className="mb-2">
                  <button
                    className={`font-bold px-2 py-1 rounded ${activeSession === s.id ? "bg-blue-200" : "bg-gray-100"}`}
                    onClick={() => setActiveSession(s.id)}
                  >
                    {s.name}
                  </button>
                  <span className="ml-2 text-sm text-gray-500">({s.topic || "No topic"})</span>
                </li>
              ))}
            </ul>
          </section>
        </div>
        {/* Right column: Graphs, Agent Data, Analytics */}
        <div className="w-2/3 flex flex-col gap-6 p-4 bg-white">
          <section>
            <h2 className="text-xl font-semibold mb-2">Agentic Task Flow Visualization</h2>
            <TaskFlowGraph />
          </section>
          <section>
            <h2 className="text-xl font-semibold mb-2">Agents</h2>
            <ul>
              {agents.map((a) => (
                <li key={a.id} className="mb-2">
                  <span className="font-bold">{a.name}</span> <span className="text-xs text-gray-500">({a.type})</span> - {a.description}
                </li>
              ))}
            </ul>
          </section>
          {activeSession && (
            <section>
              <h2 className="text-xl font-semibold mb-2">Analytics</h2>
              <ul>
                {analytics.map((a, idx) => (
                  <li key={idx} className="mb-1">
                    <span className="font-bold">{a.metric}:</span> {a.value} <span className="text-xs text-gray-500">({a.created_at})</span>
                  </li>
                ))}
              </ul>
            </section>
          )}
        </div>
      </div>
    </main>
  );
}
