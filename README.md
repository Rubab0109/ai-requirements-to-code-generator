# AI Requirements-to-Code Generator

A complete working web application that converts raw software requirements into software engineering artifacts using Generative AI / LLM integration.

## Project Purpose

Software requirements often do not match final code. Students and junior developers struggle to convert requirement statements into clean requirement analysis, UML diagrams, ERD diagrams, database schema, starter code, and technology stack decisions. This app solves that problem by acting like an AI software architect.

## Core Features

- Enter raw software project requirements
- Generate clean requirement analysis
- Generate functional requirements
- Generate non-functional requirements
- Generate UML class diagram in Mermaid syntax
- Generate ERD in Mermaid syntax
- Generate database schema SQL
- Generate starter code skeleton
- Suggest technology stack
- Preview Mermaid diagrams in the frontend
- Copy/download generated outputs
- Store previous generated projects in SQLite
- Demo fallback mode when API key is not configured

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, Vite, Tailwind CSS |
| Diagram Rendering | Mermaid.js |
| Backend | FastAPI, Pydantic, HTTPX |
| LLM API | Gemini default, Groq/OpenAI optional |
| Storage | SQLite |
| Config | `.env` file |
| Testing | Pytest + FastAPI TestClient |

## System Architecture

```text
User Browser
  ↓
React + Tailwind Dashboard
  ↓ REST API
FastAPI Backend
  ├── Validation Layer
  ├── Prompt Builder
  ├── LLM Integration Service
  ├── Mermaid Cleaner/Validator
  └── SQLite Storage
  ↓
Gemini / Groq / OpenAI API
```

## Folder Structure

```text
ai_requirements_to_code_generator/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── llm_service.py
│   │   ├── mermaid_utils.py
│   │   ├── prompts.py
│   │   ├── sample_generator.py
│   │   └── schemas.py
│   ├── tests/
│   │   └── test_api.py
│   ├── .env.example
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .env.example
│   ├── package.json
│   ├── postcss.config.js
│   └── tailwind.config.js
├── docs/
│   ├── demo_video_script.md
│   └── sample_input_output.md
├── report_outline.md
└── README.md
```

## Backend Setup

Open terminal in the project root.

```bash
cd backend
python -m venv venv
```

### Activate virtual environment

Windows PowerShell:

```powershell
venv\Scripts\activate
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again.

### Install backend dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Copy example file:

Windows:

```powershell
copy .env.example .env
```

Mac/Linux:

```bash
cp .env.example .env
```

Open `backend/.env` and add your API key.

Default Gemini setup:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
ALLOW_DEMO_FALLBACK=true
```

If no key is added, the app still runs in demo fallback mode for classroom prototype testing.

### Run backend

```bash
python -m uvicorn main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

## Frontend Setup

Open a second terminal in project root.

```bash
cd frontend
npm install
```

Copy frontend environment file:

Windows:

```powershell
copy .env.example .env
```

Mac/Linux:

```bash
cp .env.example .env
```

Run frontend:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Backend health check |
| POST | `/api/generate` | Generate analysis, diagrams, schema, code |
| GET | `/api/projects` | List saved projects |
| GET | `/api/projects/{id}` | Load saved project |
| DELETE | `/api/projects/{id}` | Delete saved project |

## LLM Integration Explanation

The backend contains a dedicated service file:

```text
backend/app/llm_service.py
```

Flow:

1. User enters requirement in React UI.
2. React sends requirement to FastAPI endpoint `/api/generate`.
3. FastAPI validates input.
4. `prompts.py` creates a strict JSON prompt for the LLM.
5. `llm_service.py` sends the prompt to Gemini, Groq, or OpenAI depending on `.env`.
6. LLM response is parsed as JSON.
7. Mermaid diagrams are cleaned and lightly validated.
8. Final generated project is stored in SQLite.
9. Frontend displays all outputs in tabs.

## Prompting Strategy

The app uses a structured prompt that forces the LLM to return JSON with these keys:

- `analysis`
- `assumptions`
- `functional_requirements`
- `non_functional_requirements`
- `uml_mermaid`
- `erd_mermaid`
- `database_schema`
- `code_skeleton`
- `tech_stack`
- `testing_notes`

This makes the output easy to render in a web dashboard.

## Testing

Run backend tests:

```bash
cd backend
python -m pytest
```

Included tests:

- Empty requirement input
- Very short requirement
- Complex requirement
- API failure handling
- Invalid Mermaid output handling

## Sample Input

```text
Build a campus event and society management system where students can register, societies can create events, admin can approve events, generate fee vouchers, track payments, manage departments/batches, and export attendance/reports. The system should have role based dashboards for admin, society head, and student.
```

## Sample Output Sections

The app generates:

- Analysis paragraph
- Functional requirements list
- Non-functional requirements list
- Mermaid UML class diagram
- Mermaid ERD diagram
- SQL database schema
- Starter API code skeleton
- Technology stack recommendation

See `docs/sample_input_output.md` for a longer sample.

## Deployment Suggestions

### Frontend

Deploy `frontend/` on Vercel.

Add environment variable:

```env
VITE_API_BASE_URL=https://your-backend-url.com
```

### Backend

Deploy `backend/` on Render or Railway.

Start command:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

Add environment variables from `backend/.env.example`.

## Limitations

- LLM output can sometimes contain invalid Mermaid syntax.
- Starter code requires developer review before production use.
- SQLite is suitable for prototype/demo but not ideal for high-scale production.
- Generated architecture depends on requirement quality.
- API costs and rate limits depend on selected LLM provider.

## Future Improvements

- User login system
- Export full SRS PDF report
- Export generated code as ZIP
- Version history for generated outputs
- Real-time streaming response
- Advanced Mermaid repair using parser feedback
- PostgreSQL support
- Team collaboration and comments
- Integration with GitHub repository creation

## Academic Deliverables Covered

- UI: React dark dashboard
- Backend: FastAPI API
- LLM integration: Gemini/Groq/OpenAI through `.env`
- Storage: SQLite
- Diagrams: Mermaid.js
- Testing: Pytest
- Documentation: README, report outline, demo script, sample output
