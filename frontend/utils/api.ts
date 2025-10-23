export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchSessions() {
  const res = await fetch(`${API_URL}/sessions`);
  if (!res.ok) throw new Error("Failed to fetch sessions");
  return res.json();
}

export async function fetchSessionHistory(sessionId: number) {
  const res = await fetch(`${API_URL}/session/${sessionId}/history`);
  if (!res.ok) throw new Error("Failed to fetch session history");
  return res.json();
}

export async function fetchAnalytics(sessionId: number) {
  const res = await fetch(`${API_URL}/analytics/${sessionId}`);
  if (!res.ok) throw new Error("Failed to fetch analytics");
  return res.json();
}

export async function fetchAgents() {
  const res = await fetch(`${API_URL}/agents`);
  if (!res.ok) throw new Error("Failed to fetch agents");
  return res.json();
}

export async function postFeedback(sessionId: number, agentId: number | null, feedback: string) {
  const res = await fetch(`${API_URL}/session/${sessionId}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ agent_id: agentId, feedback }),
  });
  if (!res.ok) throw new Error("Failed to post feedback");
  return res.json();
}
