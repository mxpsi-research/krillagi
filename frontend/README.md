
# krillAGI Frontend

This is the Next.js/Tailwind dashboard for krillAGI, providing a modern UI for agentic chat, session history, analytics, and visualization.

## Features
- Chat UI (left column) with session history, message deletion, and navigation
- Agentic task flow graph (Cytoscape.js)
- Agent data and analytics (right column, live updates)
- Light mode, high-contrast two-column layout
- Integration with FastAPI backend

## Getting Started

1. Install Node dependencies:
	```bash
	npm install
	```
2. Start the development server:
	```bash
	npm run dev
	```
3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure
- `app/page.tsx` - Main dashboard layout
- `components/ChatUI.tsx` - Chat interface
- `components/TaskFlowGraph.tsx` - Agentic graph visualization
- `utils/api.ts` - API utility functions

## Environment
- Set `NEXT_PUBLIC_API_URL` in `.env.local` to point to your backend (default: `http://localhost:8000`)

## License
MIT
