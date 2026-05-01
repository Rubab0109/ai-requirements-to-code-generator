# Demo Video Script — 5 to 7 Minutes

## 0:00–0:30 — Introduction
Assalam-o-Alaikum. My project name is **AI Requirements-to-Code Generator**. This project solves a real software engineering problem: students and junior developers often write requirements, but they struggle to convert those requirements into UML diagrams, ERD, database schema, and starter code.

## 0:30–1:10 — Problem Explanation
In real projects, software requirements and final code often do not match. If requirements are unclear, database design and code structure become weak. My app uses Generative AI to analyze raw requirements and generate software engineering artifacts automatically.

## 1:10–1:45 — Technology Stack
The frontend is built using React.js and Tailwind CSS. The backend is built using FastAPI. The app uses Gemini, Groq, or OpenAI API through an environment file. Mermaid.js is used to preview UML and ERD diagrams. SQLite is used to store previous generated projects.

## 1:45–2:30 — UI Walkthrough
Here is the dark theme dashboard. On the left side, previous generated projects are shown. In the main area, we have a large requirement input editor. The UI has a modern dark theme, professional cards, tabs, copy buttons, and download buttons.

## 2:30–3:20 — Enter Sample Requirement
Now I will enter a sample requirement: campus event and society management system. It includes student registration, society event creation, admin approval, voucher generation, payment tracking, departments, batches, and reports. Then I click the Generate Architecture button.

## 3:20–4:20 — Generated Analysis Output
The first tab shows clean requirement analysis. It also shows functional requirements and non-functional requirements. This helps developers understand project scope before writing code.

## 4:20–5:00 — UML and ERD Diagram Output
Now I open the UML Diagram tab. The app shows a Mermaid class diagram preview. Then I open the ERD tab. It shows database entities and relationships in Mermaid ERD format.

## 5:00–5:40 — Database Schema and Code Skeleton
The Database Schema tab shows SQL `CREATE TABLE` statements. The Code Skeleton tab shows starter code that a developer can use to begin implementation.

## 5:40–6:15 — Tech Stack and Storage
The Tech Stack tab suggests frontend, backend, database, AI, and deployment tools. The generated project is also saved in SQLite, so I can load previous projects again from the left panel.

## 6:15–6:50 — Backend and AI Integration
The backend has a prompt builder and LLM integration service. API keys are stored safely in `.env`. The frontend never directly accesses the API key. If the API key is not configured, demo fallback mode allows the prototype to run for presentation.

## 6:50–7:00 — Conclusion
This project is useful for students, junior developers, and software engineering teams because it converts requirements into implementation-ready artifacts. Thank you.
