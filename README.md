# AI-Powered Resume Analyzer

AI-Powered Resume Analyzer is an open-source toolkit for analyzing resumes, extracting skills and experience, and scoring fit against job descriptions using a combination of ML models and LLM-assisted heuristics. It provides utilities for resume parsing, skill extraction, fit scoring, learning-path recommendations, and interview preparation assistance.

## Features

- Resume parsing and structured extraction (skills, titles, dates, education)
- Resume-to-job matching and fit scoring
- Skill gap analysis and suggested learning paths
- Interview question generation and feedback
- Integration-ready for embeddings and vector search backends

## Tech stack

- Frontend: React 18 + TypeScript + Vite + Tailwind CSS
- Backend: Express (TypeScript) + Python services for ML/data processing
- ML: Python (spaCy, scikit-learn, sentence-transformers, etc.)
- Tooling: pnpm, Docker, Alembic, Vitest, pytest

## Repository layout (high level)

- client/ — React SPA (TypeScript, Vite)
- server/ — Node/TypeScript server tooling and build scripts
- app/, services/, ml/ — Python application code, service layers and ML models
- data/ — datasets and training CSVs
- scripts/ — helper scripts for DB init and setup
- tests/ — unit and integration tests (pytest / Vitest)

## Quick start (development)

Prerequisites:
- Node.js (recommended >= 18) and pnpm
- Python 3.8+
- Docker (optional)

1. Clone the repository

```bash
git clone <repo-url>
cd SMART-RESUME-ANALYZER--master
```

2. Install dependencies

```bash
pnpm install
python -m venv .venv
.venv\\Scripts\\activate   # Windows
pip install -r requirements.txt
```

3. Initialize the database (local)

```bash
python init_db.py
# or use scripts/init_database.py if you prefer
```

4. Start development server (client + server)

```bash
pnpm dev
```

This project uses a combined dev server for frontend and backend; API endpoints are typically prefixed with `/api/`.

## Running tests

- JavaScript/TypeScript: `pnpm test`
- Python: `pytest -q`

## Production / Docker

Build and run with Docker Compose:

```bash
docker-compose up --build -d
```

Or build the frontend and run the production server:

```bash
pnpm build
pnpm start
```

## Environment variables

Create a `.env` file at the project root and add any required API keys and configuration used by services (for example, LLM keys, `DATABASE_URL`, or vector DB credentials). Search the `services/` directory for the specific environment variables required by each module.

## Contributing

Contributions are welcome — open an issue or submit a pull request. Please run linters and tests before submitting changes.

## License

See the `LICENSE` file in the repository root.
