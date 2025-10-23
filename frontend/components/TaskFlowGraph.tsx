import CytoscapeComponent from "react-cytoscapejs";

const elements = [
  { data: { id: "user", label: "User" } },
  { data: { id: "researcher", label: "Researcher" } },
  { data: { id: "summarizer", label: "Summarizer" } },
  { data: { id: "coder", label: "Coder" } },
  { data: { id: "planner", label: "Planner" } },
  { data: { source: "user", target: "researcher" } },
  { data: { source: "researcher", target: "summarizer" } },
  { data: { source: "summarizer", target: "coder" } },
  { data: { source: "coder", target: "planner" } },
];

export default function TaskFlowGraph() {
  return (
    <CytoscapeComponent
      elements={elements}
      style={{ width: "100%", height: "400px" }}
      layout={{ name: "breadthfirst" }}
    />
  );
}
