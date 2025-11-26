# Svenska Lära

> A comprehensive Swedish language learning platform with AI-powered tutoring

---

## Overview

Svenska Lära is a mobile-first Progressive Web App (PWA) for learning Swedish. It combines structured learning (vocabulary, grammar) with AI-powered chatbots for personalized practice, all tied together by intelligent progress tracking that estimates your CEFR level across all four language skills.

### Key Features

- **Vocabulary Training** - Spaced repetition system (SRS) for efficient memorization
- **Grammar Lessons** - Structured curriculum covering Swedish grammar
- **AI Chatbots** - Five specialized AI tutors for different learning needs
- **Writing Analysis** - Detailed feedback on spelling, grammar, and style
- **CEFR Tracking** - Independent skill tracking for Reading, Writing, Listening, Speaking
- **Mobile-First** - Optimized for learning on the go

### AI Tutors

| Bot | Swedish Name | Purpose |
|-----|--------------|---------|
| Conversation Partner | Samtalspartner | Free conversation practice |
| Grammar Teacher | Grammatikläraren | Grammar explanations and exercises |
| Writing Teacher | Skrivläraren | Writing prompts and corrections |
| Word Teacher | Ordläraren | Vocabulary in context |
| Translator | Översättaren | Translation with explanations |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, TypeScript, Tailwind CSS, Vite |
| Backend | FastAPI, Python 3.11, SQLAlchemy |
| Database | PostgreSQL |
| AI | Claude API (Anthropic) |
| Auth | JWT with refresh tokens |

---

## Getting Started

### Prerequisites

- Python 3.11
- Node.js 18+
- PostgreSQL 14+
- Anthropic API key

### Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment
py -3.11 -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env
# Edit .env with your settings

# Run migrations
alembic upgrade head

# Start server
uvicorn src.main:app --reload
```

### Frontend Setup

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Copy environment template
copy .env.example .env.local
# Edit .env.local with your settings

# Start development server
npm run dev
```

### Database Setup

```sql
-- Create database
CREATE DATABASE svenskalara;

-- Create user (optional)
CREATE USER svenskalara_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE svenskalara TO svenskalara_user;
```

---

## Project Structure

```
agentic_language_learning/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # Route handlers
│   │   ├── core/           # Config, security
│   │   ├── services/       # Business logic
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── db/             # Database config
│   ├── alembic/            # Migrations
│   └── tests/              # Backend tests
│
├── frontend/               # React PWA
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Route pages
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API clients
│   │   ├── store/          # State management
│   │   └── types/          # TypeScript types
│   └── public/             # Static assets
│
├── docs/                   # Documentation
├── temp/                   # Temporary files (gitignored)
├── ROADMAP.md             # Development roadmap
├── CLAUDE_INSTRUCTIONS.md # AI assistant guidelines
└── README.md              # This file
```

---

## Development

### Running Tests

```powershell
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm test
```

### Code Quality

```powershell
# Backend linting
cd backend
ruff check src/
ruff format src/

# Frontend linting
cd frontend
npm run lint
```

---

## Documentation

- [ROADMAP.md](./ROADMAP.md) - Development phases and progress
- [CLAUDE_INSTRUCTIONS.md](./CLAUDE_INSTRUCTIONS.md) - AI coding guidelines
- [docs/api/](./docs/api/) - API documentation
- [docs/architecture/](./docs/architecture/) - Design documents

---

## License

Private project - All rights reserved

---

## Acknowledgments

- Powered by [Claude](https://anthropic.com) from Anthropic
- Swedish frequency lists from various linguistic sources
