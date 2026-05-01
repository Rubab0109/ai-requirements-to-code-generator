# 25–30 Page Report Outline

## Project Title
**AI Requirements-to-Code Generator**

## Suggested Page Distribution

### 1. Title Page — 1 page
- Project title
- Student/group member names
- Roll numbers
- Department
- Semester
- Subject
- Teacher name
- University name
- Submission date
- GitHub link
- Deployment links

### 2. Abstract — 1 page
- Short summary of the problem
- Purpose of the AI app
- Main outputs: analysis, UML, ERD, schema, code skeleton, tech stack
- Technologies used
- Expected benefit for students and junior developers

### 3. Introduction — 2 pages
- Importance of software requirements in software engineering
- Common gap between requirements and final implementation
- Why students struggle with requirement conversion
- Role of AI in software engineering support
- Overview of proposed solution

### 4. Problem Statement — 1 page
- Requirements are often unclear and incomplete
- Manual UML/ERD creation is time-consuming
- Beginner developers struggle with database and code structure
- Need for a guided AI-based requirement conversion tool

### 5. Project Objectives — 1 page
- Generate clean requirement analysis
- Identify functional requirements
- Identify non-functional requirements
- Generate UML class diagrams
- Generate ERD diagrams
- Generate database schema
- Generate starter code skeleton
- Suggest technology stack
- Store project history

### 6. Scope of the Project — 1 page
#### Included Scope
- Requirement input dashboard
- LLM-based generation
- Mermaid diagram preview
- SQLite project history
- Copy/download output

#### Out of Scope
- Fully production-ready generated application
- Automatic deployment of generated code
- Multi-user collaboration in current prototype

### 7. Literature Review / Background Study — 3 pages
Discuss:
- Software Requirement Specification
- UML class diagrams
- Entity Relationship Diagrams
- Database schema design
- Starter code generation
- Generative AI in software engineering
- Prompt engineering for structured outputs

### 8. Existing System — 1 page
- Manual requirement analysis
- Manual diagram creation tools
- Manual database design
- Manual starter code writing
- Problems in existing manual approach

### 9. Proposed System — 2 pages
- AI-powered web application
- User enters raw requirements
- Backend sends structured prompt to LLM
- LLM returns structured JSON output
- Frontend displays outputs in tabs
- Mermaid renders diagrams
- SQLite stores generated projects

### 10. System Architecture — 2 pages
Include diagram and explanation:
- Frontend input UI
- Backend API
- LLM integration service
- Prompt builder
- Mermaid renderer
- SQLite storage
- Output display module

### 11. Technology Stack — 2 pages
#### Frontend
- React.js
- Tailwind CSS
- Mermaid.js

#### Backend
- FastAPI
- Pydantic
- HTTPX

#### AI Integration
- Gemini / Groq / OpenAI API
- API key through `.env`

#### Storage
- SQLite

### 12. Functional Requirements — 1.5 pages
- User enters project requirements
- System validates input
- System generates requirement analysis
- System generates functional requirements
- System generates non-functional requirements
- System generates UML diagram
- System generates ERD diagram
- System generates database schema
- System generates code skeleton
- System suggests technology stack
- System stores previous projects
- User can copy/download outputs

### 13. Non-Functional Requirements — 1.5 pages
- Usability
- Responsiveness
- Security of API keys
- Maintainability
- Reliability
- Error handling
- Performance
- Scalability for future upgrades

### 14. UI/UX Design — 2 pages
- Dark theme dashboard
- Requirement editor
- Generate button
- Output tabs
- Mermaid preview area
- Copy/download buttons
- Previous project history panel
- Responsive layout
- Professional color scheme

### 15. Backend Implementation — 2 pages
Explain files:
- `main.py`
- `config.py`
- `prompts.py`
- `llm_service.py`
- `database.py`
- `mermaid_utils.py`
- `sample_generator.py`

Explain endpoints:
- `/health`
- `/api/generate`
- `/api/projects`
- `/api/projects/{id}`
- `/api/projects/{id}` delete

### 16. LLM Prompt Engineering — 2 pages
- Why structured JSON prompt is used
- Separate tasks included in prompt
- Mermaid rules
- Error handling for invalid response
- Demo fallback mode
- API provider selection through `.env`

### 17. Database Design — 1 page
Table: `projects`
- `id`
- `title`
- `requirements`
- `generated_json`
- `created_at`

Explain why SQLite is selected for prototype.

### 18. Mermaid Diagram Support — 1 page
- UML class diagram generation
- ERD generation
- Mermaid.js rendering in React
- Invalid Mermaid handling
- Copy/download Mermaid syntax

### 19. Testing — 2 pages
Test cases:
1. Empty requirement input
2. Very short requirement
3. Complex requirement
4. API failure
5. Invalid Mermaid output
6. Project storage
7. Project reload from history
8. Copy/download output

Include expected results and actual results table.

### 20. Sample Input and Output — 2 pages
- Add sample requirement paragraph
- Add generated analysis
- Add functional requirements
- Add non-functional requirements
- Add UML Mermaid code
- Add ERD Mermaid code
- Add database schema
- Add code skeleton screenshot or excerpt

### 21. Screenshots — 2 pages
Add screenshots of:
- Dashboard
- Requirement editor
- Analysis tab
- UML tab
- ERD tab
- Database schema tab
- Code skeleton tab
- Previous projects panel

### 22. Deployment Plan — 1 page
- Frontend deployment on Vercel
- Backend deployment on Render/Railway
- Environment variables
- Database storage notes
- CORS configuration

### 23. Limitations — 1 page
- LLM may produce imperfect output
- Mermaid syntax may need correction
- Generated code is starter code only
- SQLite not for large production scale
- API key/rate-limit dependency

### 24. Future Improvements — 1 page
- Authentication
- Export SRS PDF
- Export generated code ZIP
- GitHub integration
- PostgreSQL support
- Real-time streaming
- Team collaboration
- Advanced AI diagram repair

### 25. Conclusion — 1 page
- Summarize problem solved
- Explain how AI improves requirement conversion
- Mention academic and real-world value
- Final statement about future scalability

### 26. References — 1 page
Add references for:
- React.js documentation
- Tailwind CSS documentation
- FastAPI documentation
- Mermaid.js documentation
- Gemini/Groq/OpenAI API documentation
- SQLite documentation

### 27–30. Appendix — optional 3–4 pages
- Important code snippets
- `.env.example`
- API request/response examples
- Test command outputs
- GitHub repository screenshots
