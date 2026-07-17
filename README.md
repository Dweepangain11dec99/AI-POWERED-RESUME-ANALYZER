# AI-Powered Resume Analyzer

AI-powered HR platform with resume analysis, ATS scoring, skill gap analysis, and recruiter simulation.

## Features

- **Resume Analysis** — Multi-dimensional resume scoring
- **ATS Compatibility** — Score resumes against job descriptions
- **Skill Gap Analysis** — Identify missing skills with learning roadmaps
- **A/B Testing** — Compare resumes side-by-side
- **Recruiter Simulation** — Simulate hiring decision process
- **Market Intelligence** — Analyze market demand for skills
- **Cover Letter Generation** — Generate job-specific cover letters
- **HR Analytics** — Turnover prediction, performance reviews, compensation analysis

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + TypeScript (or SvelteKit) |
| Backend | FastAPI (Python 3.11+) |
| Database | PostgreSQL with SQLAlchemy ORM |
| AI / LLM | Hugging Face Inference API (Qwen2) |
| Auth | JWT + bcrypt |
| NLP | spaCy + scikit-learn |
| Vector DB | Qdrant (optional) |

## Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Node.js 18+ (for frontend)
- Hugging Face API token (get from https://huggingface.co/settings/tokens)

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Dweepangain11dec99/AI-POWERED-RESUME-ANALYZER.git
cd AI-POWERED-RESUME-ANALYZER
```

### 2. Setup Environment

```bash
cp .env.example .env
# Edit .env with your configuration
# Required: DATABASE_URL, HF_TOKEN, JWT_SECRET
```

### 3. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 4. Initialize Database

```bash
# Create tables (automatic on first run)
python -c "from app.db.database import init_db; init_db()"
```

### 5. Run Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Visit: http://localhost:8000/api/docs

## Docker Deployment

```bash
# Build image
docker-compose build

# Run services
docker-compose up -d

# Check logs
docker-compose logs -f fastapi-app
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `HF_TOKEN` | Yes | Hugging Face API token |
| `JWT_SECRET` | Yes | Secret key for JWT tokens (min 32 chars) |
| `APP_ENV` | No | `development` or `production` |
| `DEBUG` | No | Enable debug logging |
| `CORS_ORIGINS` | No | Comma-separated CORS origins |

## Project Structure

```
├── app/
│   ├── db/
│   │   ├── database.py       # SQLAlchemy setup
│   │   └── models.py         # Database models
│   ├── routes/
│   │   ├── health.py         # Health check endpoint
│   │   ├── auth.py           # Authentication endpoints
│   │   └── __init__.py        # Router discovery
│   ├── services/
│   │   ├── llm.py            # LLM service
│   │   ├── auth.py           # Auth utilities
│   │   └── environment_checks.py
│   ├── middleware/
│   │   └── error_handling.py
│   └── api_docs.py           # OpenAPI config
├── main.py                   # FastAPI app entry point
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Docker compose config
├── Dockerfile                # Docker build config
└── .env.example              # Environment template
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

## Development

### Running Tests

```bash
pytest -v
pytest --cov=app
```

### Code Quality

```bash
pylint app/
black app/ main.py
isort app/ main.py
```

## Troubleshooting

### Database Connection Error
```
Make sure PostgreSQL is running and DATABASE_URL is correct
psql $DATABASE_URL -c "SELECT 1"
```

### spaCy Model Missing
```bash
python -m spacy download en_core_web_sm
```

### Tesseract Not Found
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/Dweepangain11dec99/AI-POWERED-RESUME-ANALYZER/issues
- Documentation: See `/docs` directory
