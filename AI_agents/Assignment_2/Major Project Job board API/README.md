# Major Project — Job Board API (FastAPI + RAG + Agent)

This repository contains a **Job Board backend API** built with **FastAPI** and **PostgreSQL**, extended with an **AI Intelligence Layer** (RAG search, recommendations, job-description improvement, and a ReAct-style agent).

> The application source lives in: `Major Project Job board API/`

---

## System architecture (high level)

### Core API (CRUD)

- **FastAPI app**: `Major Project Job board API/main.py`
- **Routers (HTTP endpoints)**: `Major Project Job board API/src/routers/*`
  - Users, companies, job listings, job seekers, recruiters, applications
- **DB layer**
  - **Models**: `Major Project Job board API/src/models/*` (SQLModel)
  - **CRUD services**: `Major Project Job board API/src/crud/*`
  - **Async DB session**: `Major Project Job board API/src/core/database.py` (SQLAlchemy async + `asyncpg`)
- **Auth & authorization**
  - JWT auth helpers: `Major Project Job board API/src/core/auth.py`
  - **Role-based access middleware**: `Major Project Job board API/src/core/middleware.py`
    - Uses path-to-role mapping (e.g., recruiters vs job seekers)
    - Allows read-only access for some GET routes (see `BYPASS_MIDDLEWARE_PATHS` in `src/core/config.py`)

### AI Intelligence Layer (RAG + embeddings + agent)

The AI functionality is exposed under the **AI router**: `Major Project Job board API/src/routers/chatbotRoute.py` (prefix: `/ai`)

- **Vector store**: **PGVector in PostgreSQL** (LangChain integration)
  - Implemented via `langchain_postgres.PGVector`
- **Embeddings**: **HuggingFace sentence-transformers**
  - Defaults to `all-MiniLM-L6-v2` (configurable)
- **RAG flow** (`GET /ai/ask-ai`)
  - Embed query → retrieve similar docs from PGVector → prompt LLM with retrieved context → return grounded answer
  - Implemented in `src/crud/ai_search.py`
- **Embedding sync** (`POST /ai/sync-embeddings` and `POST /sync/listings/{listing_id}`)
  - Pulls listings from Postgres → builds text chunks → upserts into PGVector collection
  - Implemented in `src/crud/sync_vector_db.py` and `src/routers/embeddingRoute.py`
- **Recommendations** (`POST /ai/recommend`)
  - Embed resume/profile → similarity search in PGVector → LLM produces structured recommendation JSON
  - Implemented in `src/crud/ai_search.py`
- **Improve job description** (`POST /ai/improve-description?mode=...`)
  - LLM rewrites job description with structured output (clarity/grammar/professionalism/SEO)
  - Implemented in `src/crud/ai_search.py`
- **AI Agent** (`POST /ai/ask-agent`)
  - ReAct agent that can call “tools”:
    - semantic vector search
    - call API endpoints (jobs/companies/resumes)
  - Implemented in `src/scripts/agent.py` and `src/scripts/tools.py`

---

## Tools used

### Backend & database

- **FastAPI** (API framework)
- **Uvicorn** (ASGI server)
- **SQLModel + SQLAlchemy** (ORM / models)
- **PostgreSQL**
- **Alembic** (migrations)
- **asyncpg** (async Postgres driver)

### Auth / security

- **JWT** (token-based authentication)
- **passlib / bcrypt** (password hashing)

### AI / RAG / Agent stack

- **LangChain** (chains, prompts, agent/tooling)
- **Groq** (LLM provider via API key; default model is configurable)
- **HuggingFace embeddings** (sentence-transformers)
- **PGVector (via Postgres)** using `langchain_postgres.PGVector`

---

## How to run locally

### 1) Prerequisites

- **Python 3.10+** recommended
- **PostgreSQL** running locally
- **pgvector extension enabled** (required for vector search)

If you manage Postgres yourself, ensure the extension exists in your DB:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2) Create and configure the environment

From the repository root:

```bash
cd "Major Project Job board API"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `Major Project Job board API/` (same directory as `main.py`) and set at minimum:

```bash
# App / DB
DB_HOST=localhost
DB_PORT=5432
DB_USER=YOUR_DB_USER
DB_PASSWORD=YOUR_DB_PASSWORD
DB_NAME_JOB_BOARD_API=YOUR_DB_NAME

# Auth
SECRET_KEY=CHANGE_ME
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# LLM / AI
GROQ_API_KEY=YOUR_GROQ_KEY
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile

# Agent service account (used by tool-calling agent that hits protected endpoints)
AGENT_EMAIL=YOUR_AGENT_USER_EMAIL
AGENT_PASSWORD=YOUR_AGENT_USER_PASSWORD
INTERNAL_SERVICE_TOKEN=OPTIONAL_INTERNAL_TOKEN
```

### 3) Run database migrations (Alembic)

This project includes Alembic migrations in `Major Project Job board API/alembic/`.

**Important:** Alembic reads the DB URL from `Major Project Job board API/alembic.ini` (`sqlalchemy.url`).
Update that value to match your local DB credentials before running:

```bash
cd "Major Project Job board API"
alembic upgrade head
```

### 4) Start the API server

```bash
cd "Major Project Job board API"
uvicorn main:app --reload
```

Then open:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **OpenAPI JSON**: `http://127.0.0.1:8000/openapi.json`

### 5) (Optional) Seed data + build embeddings

To use RAG / recommendation features meaningfully, ensure you have job listings in Postgres, then sync:

- `POST /ai/sync-embeddings` (syncs all listings into PGVector)
- `POST /sync/listings/{listing_id}` (syncs a single listing)

---

## Key AI endpoints (quick reference)

- **RAG Q&A**: `GET /ai/ask-ai?query=...`
- **Agent Q&A**: `POST /ai/ask-agent?query=...`
- **Sync embeddings**: `POST /ai/sync-embeddings`
- **Job recommendation**: `POST /ai/recommend`
- **Improve job description**: `POST /ai/improve-description?mode=SHORT|DETAILED|MARKETING`
