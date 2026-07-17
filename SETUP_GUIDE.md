# Setup Guide - AI-Powered Resume Analyzer

## Complete Setup Instructions

### Prerequisites Check

```bash
# Check Python version (need 3.11+)
python --version

# Check PostgreSQL
psql --version

# Check Node.js (if building frontend)
node --version
```

### Step 1: Clone Repository

```bash
git clone https://github.com/Dweepangain11dec99/AI-POWERED-RESUME-ANALYZER.git
cd AI-POWERED-RESUME-ANALYZER
```

### Step 2: Create Virtual Environment

```bash
# Create venv
python -m venv .venv

# Activate venv
# Linux/macOS:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### Step 3: Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```ini
# Get HF token from https://huggingface.co/settings/tokens
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx

# Generate JWT secret (32+ random characters)
JWT_SECRET=your_random_secret_key_min_32_chars

# PostgreSQL connection
DATABASE_URL=postgresql://user:password@localhost:5432/resume_analyzer

# App settings
APP_ENV=development
DEBUG=true
```

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Download NLP Models

```bash
# Download spaCy English model
python -m spacy download en_core_web_sm
```

### Step 6: Database Setup

#### Option A: Using PostgreSQL Locally

```bash
# Create database and user
sudo -u postgres psql

CREATE USER resume_user WITH PASSWORD 'secure_password';
CREATE DATABASE resume_analyzer OWNER resume_user;
ALTER ROLE resume_user SET client_encoding TO 'utf8';
ALTER ROLE resume_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE resume_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE resume_analyzer TO resume_user;
\q
```

Update `.env`:
```
DATABASE_URL=postgresql://resume_user:secure_password@localhost:5432/resume_analyzer
```

#### Option B: Using Docker

```bash
docker-compose up -d postgres
```

### Step 7: Initialize Database Tables

```bash
python -c "from app.db.database import init_db; init_db()"
```

### Step 8: Run Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Application will be available at: http://localhost:8000

### Step 9: Verify Installation

```bash
# Test health endpoint
curl http://localhost:8000/health

# View API documentation
# Open in browser: http://localhost:8000/api/docs
```

## Full Docker Setup

If using Docker:

```bash
# Create .env.prod for production
cp .env.example .env.prod
# Edit .env.prod with your settings

# Build and run all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Troubleshooting

### 1. PostgreSQL Connection Error

```bash
# Test connection
psql postgresql://user:password@localhost:5432/resume_analyzer

# If fails, check PostgreSQL is running
# Linux/macOS:
sudo service postgresql status

# macOS with brew:
brew services list

# Windows:
# Check Services tab in Task Manager
```

### 2. spaCy Model Not Found

```bash
python -m spacy download en_core_web_sm
```

### 3. HF_TOKEN Not Set

```bash
# Get token from: https://huggingface.co/settings/tokens
# Add to .env:
echo "HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx" >> .env
```

### 4. Port 8000 Already in Use

```bash
# Use different port
uvicorn main:app --port 8001

# Or find and kill process using port 8000
# Linux/macOS:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## Next Steps

1. **Build Frontend** (if using React/SvelteKit)
   ```bash
   npm install
   npm run dev
   ```

2. **Run Tests**
   ```bash
   pytest -v
   ```

3. **Deploy to Production**
   - Use `docker-compose.yml` for deployment
   - Update `.env.prod` with production settings
   - Use environment variables for secrets

## Quick Commands

```bash
# Activate environment
source .venv/bin/activate

# Run development server
uvicorn main:app --reload

# Run with custom port
uvicorn main:app --port 8001

# Run tests
pytest -v

# Format code
black app/ main.py

# Lint code
pylint app/

# Check imports
isort --check-only app/

# View logs
tail -f logs/app.log
```

## Support

For issues:
1. Check logs: `tail -f logs/app.log`
2. Review GitHub Issues: https://github.com/Dweepangain11dec99/AI-POWERED-RESUME-ANALYZER/issues
3. Check documentation: See `/docs` directory
