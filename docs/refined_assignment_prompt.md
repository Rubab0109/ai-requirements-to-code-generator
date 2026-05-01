# Refined Assignment Prompt

You are a senior software engineer and AI product developer.

Build a complete working web application named **AI Requirements-to-Code Generator**.

## Main Problem
Software requirements often do not match final implementation. Students and junior developers struggle to convert raw requirements into proper requirement analysis, UML diagrams, ERD diagrams, database schema, starter code, and technology stack decisions.

## Goal
Create an AI-powered web application where a user enters raw software requirements and the system generates implementation-ready software engineering artifacts.

## Required Outputs
The system must generate:

1. Clean requirement analysis
2. Functional requirements
3. Non-functional requirements
4. UML class diagram in Mermaid syntax
5. ERD diagram in Mermaid syntax
6. Database schema SQL
7. Initial code skeleton
8. Suggested technology stack
9. Testing notes

## Technology Stack
Use:

- Frontend: React.js + Tailwind CSS
- Backend: FastAPI
- LLM API: Gemini by default, Groq/OpenAI optional through `.env`
- Diagram Support: Mermaid.js
- Storage: SQLite
- API Key Handling: `.env` file only

## UI Requirements
Create a modern, professional dark theme dashboard with:

- Responsive dashboard layout
- Large requirement input editor
- Project title input
- Generate button
- Previous projects sidebar
- Tabs for generated outputs:
  - Analysis
  - UML Diagram
  - ERD Diagram
  - Database Schema
  - Code Skeleton
  - Tech Stack
- Mermaid diagram preview area
- Copy and download buttons
- Professional cards, gradients, and clean spacing

## Backend Requirements
Backend must include:

- Input validation
- LLM prompt builder
- LLM API integration service
- Mermaid syntax cleaning/light validation
- SQLite storage module
- API routes for generate/list/load/delete projects
- Demo fallback mode for classroom presentation without API key

## Testing Requirements
Add tests for:

- Empty requirement input
- Very short requirement input
- Complex requirement input
- API failure handling
- Invalid Mermaid output handling

## Documentation Deliverables
Include:

- Professional README
- `.env.example`
- 25–30 page report outline
- 5–7 minute demo video script
- Sample input and sample output
- LLM integration explanation
- Limitations and future improvements

## Important Implementation Rule
Frontend must never call the LLM API directly. All LLM API calls must happen only in the backend so API keys remain secure.
