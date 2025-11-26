# Svenska Lära - Development Roadmap

> Swedish Language Learning Platform with AI-Powered Chatbots

---

## Project Vision

A comprehensive Swedish learning platform combining structured learning (grammar, vocabulary) with AI-powered practice (specialized chatbots), tied together by a smart tracking system that adapts to user progress and estimates CEFR levels across all four skills.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18+ (TypeScript), Tailwind CSS, PWA |
| Backend | FastAPI (Python 3.11), SQLAlchemy, Alembic |
| Database | PostgreSQL |
| AI | Claude API (Anthropic) |
| Auth | JWT with refresh tokens |

---

## CEFR Skill Tracking

The platform tracks four skills independently:

| Skill | How Measured |
|-------|--------------|
| **Reading** | Comprehension quizzes, text difficulty levels |
| **Writing** | Error analysis, vocabulary range, complexity |
| **Listening** | Audio comprehension scores |
| **Speaking** | Conversation bot interactions, fluency metrics |

---

## Development Phases

### Phase 0: Foundation [CURRENT]
> Project setup and infrastructure

- [x] Initialize git repository
- [x] Create project structure
- [x] Create documentation (README, ROADMAP, INSTRUCTIONS)
- [ ] Set up backend (FastAPI scaffold)
- [ ] Set up frontend (React + Vite + TypeScript)
- [ ] Set up PostgreSQL database
- [ ] Create database schema and initial migrations
- [ ] Configure development environment

---

### Phase 1: Core Authentication & User System
> Estimated: First milestone

**Backend:**
- [ ] User model and schema
- [ ] JWT authentication (access + refresh tokens)
- [ ] Registration and login endpoints
- [ ] Password hashing (bcrypt)
- [ ] User profile endpoints

**Frontend:**
- [ ] Login page (mobile-optimized)
- [ ] Registration page
- [ ] Auth context/state management
- [ ] Protected routes
- [ ] Token refresh handling

**Database:**
- [ ] users table
- [ ] refresh_tokens table

---

### Phase 2: Vocabulary System (SRS)
> Spaced Repetition System for word learning

**Backend:**
- [ ] Word model with full Swedish linguistic data
- [ ] User-word relationship (progress tracking)
- [ ] SRS algorithm implementation (SM-2 or similar)
- [ ] Vocabulary API endpoints
- [ ] Import initial Swedish word list (frequency-based)

**Frontend:**
- [ ] Vocabulary dashboard
- [ ] Flashcard component (swipe-friendly)
- [ ] Word detail view
- [ ] Review session interface
- [ ] Progress statistics

**Database:**
- [ ] words table (swedish, english, pronunciation, gender, examples)
- [ ] user_words table (status, review dates, ease factor)
- [ ] word_categories table

**Word Statuses:**
```
new → learning → familiar → mastered → review_needed
```

---

### Phase 3: AI Chatbots (Core Two)
> Start with Conversation Partner and Writing Teacher

**Backend:**
- [ ] Chat session management
- [ ] Claude API integration service
- [ ] Bot personality/system prompt templates
- [ ] Message history storage
- [ ] Context injection (user level, known words)

**Chatbot 1: Samtalspartner (Conversation Partner)**
- [ ] System prompt design
- [ ] Level-appropriate responses
- [ ] Gentle correction mechanism
- [ ] Word encounter tracking

**Chatbot 2: Skrivläraren (Writing Teacher)**
- [ ] Writing prompt generation
- [ ] Text analysis and correction
- [ ] Error categorization (spelling, grammar, vocabulary)
- [ ] Detailed feedback formatting

**Frontend:**
- [ ] Chat interface (mobile-first)
- [ ] Bot selection screen
- [ ] Message bubbles with corrections display
- [ ] Writing submission interface
- [ ] Typing indicators

**Database:**
- [ ] chat_sessions table
- [ ] chat_messages table
- [ ] writing_submissions table
- [ ] user_spelling_errors table

---

### Phase 4: Writing Analysis & Skill Tracking
> Comprehensive writing feedback and CEFR estimation

**Backend:**
- [ ] Writing analysis service
- [ ] Spelling error pattern detection
- [ ] Grammar error categorization
- [ ] Vocabulary richness scoring
- [ ] CEFR level estimation algorithm (per skill)
- [ ] Historical progress tracking

**Frontend:**
- [ ] Writing history view
- [ ] Error pattern visualization
- [ ] Skill progress dashboard (4 skills)
- [ ] CEFR level display with breakdown

**Database:**
- [ ] user_skill_levels table
- [ ] skill_assessments table
- [ ] user_spelling_patterns table

---

### Phase 5: Grammar Curriculum
> Structured grammar lessons with exercises

**Backend:**
- [ ] Grammar topic model
- [ ] Lesson content structure
- [ ] Exercise generation
- [ ] Quiz scoring
- [ ] Prerequisites and progression

**Grammar Topics (Swedish-specific):**
1. [ ] V2 word order rule
2. [ ] En/Ett noun genders
3. [ ] Definite/indefinite forms
4. [ ] Present tense conjugation
5. [ ] Past tense (preteritum)
6. [ ] Supine and perfect tense
7. [ ] Adjective agreement
8. [ ] Pronouns
9. [ ] Prepositions
10. [ ] Subordinate clause word order

**Frontend:**
- [ ] Lesson browser
- [ ] Lesson viewer with examples
- [ ] Interactive exercises
- [ ] Quiz interface
- [ ] Grammar progress tracker

**Database:**
- [ ] grammar_topics table
- [ ] grammar_exercises table
- [ ] user_grammar_progress table

---

### Phase 6: Remaining Chatbots
> Complete the AI assistant suite

**Chatbot 3: Grammatikläraren (Grammar Teacher)**
- [ ] Grammar explanation capability
- [ ] Exercise generation
- [ ] Socratic teaching method
- [ ] Link to formal lessons

**Chatbot 4: Ordläraren (Word Teacher)**
- [ ] Contextual word introduction
- [ ] Mnemonic suggestions
- [ ] Usage examples
- [ ] Related words/synonyms

**Chatbot 5: Översättaren (Translator)**
- [ ] Translation with explanations
- [ ] False friends warnings
- [ ] Nuance explanations
- [ ] Idiomatic expressions

---

### Phase 7: Reading & Listening
> Passive skill development

**Reading:**
- [ ] Graded text library
- [ ] Reading comprehension quizzes
- [ ] Vocabulary highlighting
- [ ] Difficulty estimation

**Listening:**
- [ ] Audio content integration
- [ ] Listening exercises
- [ ] Comprehension questions
- [ ] Speed adjustment

---

### Phase 8: PWA & Polish
> Mobile optimization and offline support

- [ ] Service worker implementation
- [ ] Offline vocabulary review
- [ ] Push notifications (where supported)
- [ ] App manifest
- [ ] Install prompts
- [ ] Performance optimization

---

### Phase 9: Gamification & Engagement
> Keep users motivated

- [ ] Daily streak tracking
- [ ] Achievement system
- [ ] XP and levels
- [ ] Daily challenges
- [ ] Statistics and insights

---

### Future Considerations

- [ ] Native iOS app (React Native/Expo)
- [ ] Audio pronunciation feedback
- [ ] Speech-to-text for speaking practice
- [ ] Community features
- [ ] Additional languages

---

## Current Focus

**Next Steps:**
1. Set up FastAPI backend scaffold
2. Set up React frontend with Vite
3. Configure PostgreSQL and create initial schema
4. Implement user authentication

---

## Status Legend

- [ ] Not started
- [x] Completed
- 🚧 In progress

---

*Last updated: 2024*
