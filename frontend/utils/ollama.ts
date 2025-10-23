export async function fetchOllamaModels() {
  const res = await fetch("http://localhost:11434/api/tags");
  if (!res.ok) throw new Error("Failed to fetch Ollama models");
  const data = await res.json();
  return data.models ? data.models.map((m: any) => m.name) : [];
}
