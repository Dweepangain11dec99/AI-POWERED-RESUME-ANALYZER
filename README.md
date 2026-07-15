# ResumeMind AI — AI-Powered Resume Analyzer

AI-powered HR platform with a 9-agent AI Council for resume analysis, ATS scoring, skill gap analysis, market intelligence, and recruiter simulation. Uses Hugging Face Inference API for LLM and embeddings, Supabase PostgreSQL for storage.

## Features

- **AI Council** — 9 specialized AI agents (ATS Scanner, Role Matcher, Skill Analyst, Culture Fit, Career Coach, Resume Writer, Recruiter Sim, Market Intel, Debugger) + Consensus Engine
- **Resume Analysis** — Upload or paste resume text, get multi-dimensional scoring
- **ATS Compatibility** — Score resumes against job descriptions
- **Skill Gap Analysis** — Identify missing skills and get a 30/60/90 day learning roadmap
- **A/B Testing** — Compare two resumes side-by-side against a job description
- **Recruiter Simulation** — Simulate the full hiring decision process
- **Market Intelligence** — Analyze market demand for candidate skills
- **GitHub & Portfolio Analysis** — Enrich resume analysis with GitHub profile and portfolio review
- **Cover Letter Generation** — Generate job-specific cover letters
- **Resume Timeline** — Track resume versions and improvement over time
- **HR Analytics** — Turnover prediction, performance reviews, learning paths, compensation analysis, attendance tracking, diversity metrics

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | SvelteKit + TailwindCSS 3 |
| Backend | FastAPI (Python) |
| Database | Supabase PostgreSQL via SQLAlchemy |
| AI / LLM | Hugging Face Inference API (Qwen3-32B) |
| Embeddings | Hugging Face `BAAI/bge-large-en-v1.5` |
| Auth | JWT (python-jose) + bcrypt |
| NLP | spaCy + scikit-learn |
| Infrastructure | Single-port dev server (Vite proxy → FastAPI) |

## Project Structure

```
├── frontend/               # SvelteKit SPA
│   └── src/routes/         # App pages (login, app/, analyze, etc.)
├── routes/                 # FastAPI route handlers
│   ├── auth.py             # JWT authentication (login, register)
│   ├── council.py          # AI Council endpoints
│   ├── resume_fit.py       # Resume-job matching
│   ├── interview.py        # Interview management
│   ├── turnover_retention.py  # Turnover prediction
│   └── ...                 # Other HR modules
├── services/               # Business logic & AI services
│   ├── llm.py              # Hugging Face LLM client
│   ├── embeddings.py       # Hugging Face embeddings
│   ├── auth.py             # JWT & password utilities
│   ├── council/            # AI Council agents + orchestrator
│   ├── skill_extractor.py  # spaCy + ML skill extraction
│   └── ...                 # Other services
├── db/                     # Database layer
│   ├── database.py         # SQLAlchemy engine + session
│   └── models.py           # All ORM models
├── middleware/              # Error handling, rate limiting
├── schemas/                # Pydantic request/response schemas
├── ai_engine/              # ML model training & inference
├── main.py                 # FastAPI app entry point
├── run.bat                 # Local dev launcher (Windows)
└── requirements.txt        # Python dependencies
```

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- A Supabase PostgreSQL database (or any PostgreSQL)
- A Hugging Face API token

### Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd ResumeMind-AI
   ```

2. **Set up environment variables**
   Copy `.env.example` to `.env` and fill in:
   ```
   DATABASE_URL=postgresql://user:pass@host:5432/db
   HF_TOKEN=hf_your_huggingface_token
   JWT_SECRET=your_random_secret_string
   ```

3. **Run the launcher**
   ```bash
   run.bat
   ```
   This will:
   - Create a Python virtual environment (`.venv`)
   - Install Python dependencies
   - Install Node.js dependencies
   - Start the FastAPI backend (port 8000)
   - Start the SvelteKit frontend (port 8080)

   Wait ~45 seconds for startup (spaCy model loading), then open `http://localhost:8080`.

### Manual Start

```bash
# Backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev -- --port 8080
```

## API Documentation

Once running, visit:
- API Docs: `http://localhost:8000/api/docs`
- Health Check: `http://localhost:8000/api/health`

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string (Supabase) |
| `HF_TOKEN` | Yes | Hugging Face API token |
| `JWT_SECRET` | Yes | Secret key for JWT tokens |
| `SUPABASE_URL` | No | Supabase project URL (optional) |
| `SUPABASE_KEY` | No | Supabase anon/public key (optional) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Token expiry (default: 60) |

## Tests

```bash
pytest -q           # Python tests
cd frontend && npm test  # Svelte tests
```
