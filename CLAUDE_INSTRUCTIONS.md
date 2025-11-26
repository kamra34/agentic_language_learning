# Claude AI Assistant Instructions

> Guidelines for AI assistants working on the Svenska Lära project

---

## Project Overview

**Svenska Lära** is a Swedish language learning platform with:
- React PWA frontend (TypeScript, Vite, Tailwind CSS)
- FastAPI backend (Python 3.11, async SQLAlchemy)
- PostgreSQL database (Railway hosted)
- AI chatbots (user-selectable: Claude or OpenAI)

**Base language:** English
**Target language:** Swedish

**Ports:**
- Backend: 5000
- Frontend: 5500

---

## Critical Rules

### 1. READ THIS FILE FIRST
Always read this file and `ROADMAP.md` before making changes to understand:
- Current project state
- What's already implemented
- Coding standards
- File organization

### 2. NO MESS POLICY
This project must remain clean and maintainable. Follow these rules strictly:

#### Files
- **NO test scripts in main folders** - All tests go in `backend/tests/` or `frontend/src/__tests__/`
- **NO scratch files in main folders** - Use `temp/.scratch/` for experiments
- **NO duplicate files** - Check if something exists before creating
- **NO orphaned files** - Delete files that are no longer used
- **NO commented-out code blocks** - Remove dead code, use git history

#### Code Quality
- **NO unused imports** - Clean up imports after refactoring
- **NO console.log/print statements** - Use proper logging
- **NO hardcoded secrets** - Use environment variables
- **NO magic numbers** - Use named constants
- **NO copy-paste code** - Extract common logic into utilities

---

## Environment Setup

### Python Backend

```powershell
# Create virtual environment (Windows)
cd backend
py -3.11 -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

**IMPORTANT:**
- Always use Python 3.11: `py -3.11`
- All packages must be installed in the virtual environment
- Never install packages globally for this project

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

---

## Project Structure

```
agentic_language_learning/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── routes/          # API route handlers
│   │   │   │   ├── auth.py
│   │   │   │   ├── vocabulary.py
│   │   │   │   ├── chat.py
│   │   │   │   └── ...
│   │   │   └── middleware/      # Request middleware
│   │   ├── core/                # Core config, security
│   │   │   ├── config.py        # Settings management (pydantic-settings)
│   │   │   ├── security.py      # JWT auth, password hashing (bcrypt)
│   │   │   └── exceptions.py    # Custom exceptions
│   │   ├── services/            # Business logic
│   │   │   ├── auth.py          # User auth logic
│   │   │   ├── vocabulary.py
│   │   │   ├── chat.py
│   │   │   ├── ai_client.py     # Claude/OpenAI integration
│   │   │   └── srs.py           # Spaced repetition
│   │   ├── models/              # SQLAlchemy models (async)
│   │   │   ├── user.py          # User, AIProvider, CEFRLevel
│   │   │   ├── word.py          # Word, UserWord
│   │   │   ├── chat.py          # ChatSession, ChatMessage
│   │   │   ├── writing.py       # WritingSubmission, SpellingPattern
│   │   │   ├── skill.py         # SkillAssessment
│   │   │   └── ...
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── word.py
│   │   │   └── ...
│   │   └── db/                  # Database config
│   │       └── session.py       # Async session factory
│   ├── alembic/                 # Database migrations
│   │   └── versions/            # Migration files
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/          # Shared components
│   │   │   ├── vocabulary/      # Vocab-specific
│   │   │   ├── grammar/         # Grammar-specific
│   │   │   ├── chatbots/        # Chat interfaces
│   │   │   └── dashboard/       # Dashboard widgets
│   │   ├── pages/               # Route pages
│   │   ├── hooks/               # Custom React hooks
│   │   ├── services/            # API client functions
│   │   ├── store/               # State management
│   │   ├── styles/              # Global styles
│   │   ├── types/               # TypeScript types
│   │   └── utils/               # Helper functions
│   ├── public/
│   └── package.json
│
├── docs/
│   ├── api/                     # API documentation
│   └── architecture/            # Design docs
│
├── temp/
│   └── .scratch/                # Temporary experiments (gitignored)
│
├── .gitignore
├── README.md
├── ROADMAP.md
└── CLAUDE_INSTRUCTIONS.md       # This file
```

---

## Coding Standards

### Python (Backend)

```python
# Use type hints everywhere
def get_user_words(
    user_id: int,
    status: WordStatus | None = None,
    limit: int = 50
) -> list[UserWord]:
    ...

# Use Pydantic for validation
class WordCreate(BaseModel):
    swedish: str
    english: str
    gender: Gender | None = None

    model_config = ConfigDict(str_strip_whitespace=True)

# Use async where appropriate
async def create_chat_completion(
    messages: list[Message],
    user_level: CEFRLevel
) -> str:
    ...

# Descriptive variable names
user_vocabulary_progress = await get_user_vocabulary(user_id)
# NOT: uvp = await guv(uid)

# Constants at module top
MAX_CHAT_HISTORY_LENGTH = 50
DEFAULT_SRS_INTERVAL_DAYS = 1
```

**Python Style:**
- Use `ruff` for linting and formatting
- Follow PEP 8
- Docstrings for public functions (Google style)
- Type hints required

### TypeScript (Frontend)

```typescript
// Define interfaces for all data structures
interface Word {
  id: number;
  swedish: string;
  english: string;
  gender: 'en' | 'ett' | null;
  examples: Example[];
}

// Use functional components with TypeScript
interface FlashcardProps {
  word: Word;
  onAnswer: (correct: boolean) => void;
  showAnswer: boolean;
}

const Flashcard: React.FC<FlashcardProps> = ({ word, onAnswer, showAnswer }) => {
  // ...
};

// Use custom hooks for logic
const useVocabulary = (status?: WordStatus) => {
  const [words, setWords] = useState<Word[]>([]);
  const [loading, setLoading] = useState(true);
  // ...
  return { words, loading, refetch };
};

// Descriptive names
const handleSubmitWritingExercise = async () => { ... };
// NOT: const hndlSbmt = async () => { ... };
```

**TypeScript Style:**
- Strict mode enabled
- No `any` types (use `unknown` if truly needed)
- Interfaces over types for objects
- Use absolute imports (`@/components/...`)

---

## API Design

### Endpoint Patterns

```
# Resources
GET    /api/v1/vocabulary              # List words
POST   /api/v1/vocabulary              # Add word (admin)
GET    /api/v1/vocabulary/{id}         # Get word
PATCH  /api/v1/vocabulary/{id}         # Update word (admin)

# User-specific resources
GET    /api/v1/users/me/vocabulary     # User's vocabulary
POST   /api/v1/users/me/vocabulary/{word_id}/review  # Submit review

# Nested resources
GET    /api/v1/chat/sessions           # List chat sessions
POST   /api/v1/chat/sessions           # Start new session
POST   /api/v1/chat/sessions/{id}/messages  # Send message

# Actions
POST   /api/v1/writing/analyze         # Analyze writing
```

### Response Format

```python
# Success
{
    "data": { ... },
    "meta": {
        "total": 100,
        "page": 1,
        "per_page": 20
    }
}

# Error
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input",
        "details": [...]
    }
}
```

---

## Database Conventions

### Naming
- Tables: `snake_case`, plural (`users`, `chat_sessions`)
- Columns: `snake_case` (`created_at`, `user_id`)
- Foreign keys: `{table_singular}_id` (`user_id`, `word_id`)
- Indexes: `ix_{table}_{column}`
- Constraints: `{table}_{type}_{columns}` (`users_email_unique`)

### Required Columns
Every table should have:
```sql
id          SERIAL PRIMARY KEY
created_at  TIMESTAMP DEFAULT NOW()
updated_at  TIMESTAMP DEFAULT NOW()  -- with trigger
```

### Migrations
- Use Alembic for all schema changes
- Never modify database directly
- Descriptive migration names: `add_user_spelling_errors_table`

---

## Git Conventions

### Commit Messages
```
type(scope): description

feat(vocab): add spaced repetition algorithm
fix(chat): handle empty message submission
refactor(auth): extract token validation to utility
docs(api): add vocabulary endpoints documentation
test(vocab): add SRS calculation tests
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `style`

### Branches
```
main              # Production-ready
develop           # Integration branch
feature/vocab-srs # Feature branches
fix/chat-timeout  # Bug fixes
```

---

## Testing

### Backend Tests
```
backend/tests/
├── unit/
│   ├── test_srs_algorithm.py
│   ├── test_cefr_estimation.py
│   └── ...
├── integration/
│   ├── test_vocabulary_api.py
│   ├── test_chat_flow.py
│   └── ...
└── conftest.py  # Shared fixtures
```

Run tests:
```powershell
cd backend
pytest tests/ -v
pytest tests/unit/ -v  # Unit only
```

### Frontend Tests
```
frontend/src/__tests__/
├── components/
├── hooks/
└── utils/
```

Run tests:
```powershell
cd frontend
npm test
```

---

## Temporary Work

### Using temp/.scratch/
For experiments, debugging, or temporary scripts:

```powershell
# Create temp file
temp/.scratch/test_claude_api.py
temp/.scratch/debug_srs.py
temp/.scratch/scratch_notes.md
```

**Rules:**
- This folder is gitignored
- Clean up when done
- Never reference scratch files from main code
- Don't leave important work here (it won't be saved)

---

## Key Features

### User Settings
Users can configure preferences in their Profile:
- **AI Provider**: Choose between Claude (Anthropic) or GPT (OpenAI) for chatbots
- **Timezone**: Used for scheduling reviews and tracking streaks (default: Europe/Stockholm)

Settings are stored in the `users` table (`preferred_ai_provider`, `timezone` columns).

### CEFR Level Tracking
Independent skill levels tracked for:
- Reading (`reading_level`)
- Writing (`writing_level`)
- Listening (`listening_level`)
- Speaking (`speaking_level`)

All default to A1 for new users.

### AI Chatbots (5 types)
1. **Samtalspartner** (Conversation Partner) - General conversation practice
2. **Grammatikläraren** (Grammar Teacher) - Grammar explanations and exercises
3. **Skrivläraren** (Writing Teacher) - Writing feedback and corrections
4. **Ordläraren** (Word Teacher) - Vocabulary building and word usage
5. **Översättaren** (Translator) - Translation practice and assistance

---

## Common Tasks

### Adding a New API Endpoint

1. Create/update route in `backend/src/api/routes/`
2. Create Pydantic schemas in `backend/src/schemas/`
3. Add business logic in `backend/src/services/`
4. Add tests in `backend/tests/`
5. Update API docs if needed

### Adding a New React Component

1. Create component in appropriate `frontend/src/components/` subfolder
2. Create types in `frontend/src/types/` if needed
3. Export from index file
4. Add tests if complex logic

### Adding Database Changes

1. Modify models in `backend/src/models/`
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Review generated migration
4. Apply: `alembic upgrade head`

---

## Environment Variables

### Backend (.env)
```env
# Database (Railway PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:port/railway

# Auth
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI APIs (at least one required for chatbots)
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
OPENAI_API_KEY=sk-proj-your-openai-key-here

# Environment
ENVIRONMENT=development
DEBUG=true

# Server
HOST=0.0.0.0
PORT=5000

# CORS
CORS_ORIGINS=http://localhost:5500
```

### Frontend (.env.local)
```env
VITE_API_URL=http://localhost:5000/api/v1
```

**NEVER commit .env files!**

---

## Checklist Before Committing

- [ ] Code runs without errors
- [ ] No console.log/print debugging statements
- [ ] No unused imports
- [ ] No scratch files in main folders
- [ ] Tests pass (if applicable)
- [ ] Types are correct (no `any`)
- [ ] Migrations created for DB changes
- [ ] Documentation updated if needed

---

## Questions?

If unsure about something:
1. Check existing code for patterns
2. Read ROADMAP.md for context
3. Ask the user for clarification

**When in doubt, ask rather than guess.**
