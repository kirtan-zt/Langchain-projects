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


## Demonstration of Agent Executor chain

Testing AI-agent with a question and check the terminal response:

```bash
  Find out job listings that offer Hybrid mode of work and the salary range is more than 3L
```

```bash
> Entering new AgentExecutor chain...
Thought: Do I need to use a tool? Yes
Action: vector_job_search
Action Input: "Hybrid mode of work" and "salary range more than 3L"Role: Mechanical design engineer. Company: Reliance Industries Limited (RIL). Location: modes.on_site. Details: A candidate who has the potential to carry out successful 3D design of a thermal power plant and manage resources carefully

Role: Business Analyst. Company: Google LLC. Location: modes.hybrid. Details: Act as a liaison between business teams, IT, and management, translating needs and validating requirements, Support the design of technical solutions and participate in Quality Assurance (QA) and User Acceptance Testing (UAT).

Role: Senior Backend Developer. Company: Google LLC. Location: modes.hybrid. Details: Strong proficiency in backend languages (e.g., Python, Java, Node.js, C#), Experience with frameworks (e.g., Spring Boot, Express, Django) and DevOps tools (Docker, Kubernetes)Thought: The observation from the previous action provides some job listings that offer Hybrid mode of work, but it does not explicitly mention the salary range for each job listing. To find job listings that offer Hybrid mode of work and a salary range of more than 3L, I need to filter the results based on the salary range.

Action: vector_job_search
Action Input: "Hybrid mode of work" and "salary range more than 3L" and "job listings with salary information"Role: Business Analyst. Company: Google LLC. Location: modes.hybrid. Details: Act as a liaison between business teams, IT, and management, translating needs and validating requirements, Support the design of technical solutions and participate in Quality Assurance (QA) and User Acceptance Testing (UAT).

Role: Mechanical design engineer. Company: Reliance Industries Limited (RIL). Location: modes.on_site. Details: A candidate who has the potential to carry out successful 3D design of a thermal power plant and manage resources carefully

Role: Senior Backend Developer. Company: Google LLC. Location: modes.hybrid. Details: Strong proficiency in backend languages (e.g., Python, Java, Node.js, C#), Experience with frameworks (e.g., Spring Boot, Express, Django) and DevOps tools (Docker, Kubernetes)Thought: The observation from the previous action still does not provide the salary range for each job listing. To find job listings that offer Hybrid mode of work and a salary range of more than 3L, I need to use a different approach. I can try to list all the jobs and then filter the results based on the location and salary range.

Action: list_jobs
Action Input: NoneINFO:     Request for POST method started
INFO:     Response for POST method completed with status code 200 in 0.35s
INFO:     127.0.0.1:50924 - "POST /users/login HTTP/1.1" 200 OK
INFO:     Request for GET method started
INFO:     Response for GET method completed with status code 200 in 0.07s
INFO:     127.0.0.1:50926 - "GET /listings/ HTTP/1.1" 200 OK
[{"listing_id": 6, "title": "Database administrator", "Type of work": "Part-Time", "Status": "Still accepting"}, {"listing_id": 7, "title": "Mechanical design engineer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 8, "title": "Senior Frontend Developer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 9, "title": "Senior Backend Developer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 10, "title": "Lead Maintenance Engineer", "Type of work": "Full-Time", "Status": "Still accepting"}]Thought: The observation from the previous action provides a list of job listings, but it does not include information about the location or salary range. To find job listings that offer Hybrid mode of work and a salary range of more than 3L, I need to use a different approach. I can try to use the vector_job_search tool with a more specific query that includes the salary range.

Action: vector_job_search
Action Input: "Hybrid mode of work" and "salary range more than 3L" and "job listings with salary information"Role: Business Analyst. Company: Google LLC. Location: modes.hybrid. Details: Act as a liaison between business teams, IT, and management, translating needs and validating requirements, Support the design of technical solutions and participate in Quality Assurance (QA) and User Acceptance Testing (UAT).

Role: Mechanical design engineer. Company: Reliance Industries Limited (RIL). Location: modes.on_site. Details: A candidate who has the potential to carry out successful 3D design of a thermal power plant and manage resources carefully

Role: Senior Backend Developer. Company: Google LLC. Location: modes.hybrid. Details: Strong proficiency in backend languages (e.g., Python, Java, Node.js, C#), Experience with frameworks (e.g., Spring Boot, Express, Django) and DevOps tools (Docker, Kubernetes)Thought: It seems that the previous actions did not provide the desired results. The vector_job_search tool is not able to provide job listings with salary information. To find job listings that offer Hybrid mode of work and a salary range of more than 3L, I need to think of a different approach. 

Action: list_jobs
Action Input: NoneINFO:     Request for GET method started
INFO:     Response for GET method completed with status code 200 in 0.01s
INFO:     127.0.0.1:50928 - "GET /listings/ HTTP/1.1" 200 OK
[{"listing_id": 6, "title": "Database administrator", "Type of work": "Part-Time", "Status": "Still accepting"}, {"listing_id": 7, "title": "Mechanical design engineer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 8, "title": "Senior Frontend Developer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 9, "title": "Senior Backend Developer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 10, "title": "Lead Maintenance Engineer", "Type of work": "Full-Time", "Status": "Still accepting"}]Thought: It seems that the previous actions did not provide the desired results. The vector_job_search tool is not able to provide job listings with salary information, and the list_jobs tool does not provide information about the location or salary range. To find job listings that offer Hybrid mode of work and a salary range of more than 3L, I need to think of a different approach. 

Since the tools provided do not seem to be able to provide the desired results, I will try to analyze the observations from the previous actions. From the observations, I can see that there are some job listings that offer Hybrid mode of work, but the salary range is not explicitly mentioned. 

Action: list_companies
Action Input: NoneINFO:     Request for GET method started
INFO:     Response for GET method completed with status code 200 in 0.03s
INFO:     127.0.0.1:50929 - "GET /companies/ HTTP/1.1" 200 OK
[{"Company name": "Google LLC", "ID": 11, "Industry": "Information Technology"}, {"Company name": "Reliance Industries Limited (RIL)", "ID": 13, "Industry": "Chemical"}]Thought: Based on the observations from the previous actions, I can see that there are some job listings that offer Hybrid mode of work, but the salary range is not explicitly mentioned. I can try to analyze the job listings that offer Hybrid mode of work and see if I can find any information about the salary range.

Action: vector_job_search
Action Input: "Hybrid mode of work" and "job listings with salary information"Role: Business Analyst. Company: Google LLC. Location: modes.hybrid. Details: Act as a liaison between business teams, IT, and management, translating needs and validating requirements, Support the design of technical solutions and participate in Quality Assurance (QA) and User Acceptance Testing (UAT).

Role: Senior Backend Developer. Company: Google LLC. Location: modes.hybrid. Details: Strong proficiency in backend languages (e.g., Python, Java, Node.js, C#), Experience with frameworks (e.g., Spring Boot, Express, Django) and DevOps tools (Docker, Kubernetes)

Role: Mechanical design engineer. Company: Reliance Industries Limited (RIL). Location: modes.on_site. Details: A candidate who has the potential to carry out successful 3D design of a thermal power plant and manage resources carefullyThought: Based on the observations from the previous actions, I can see that there are some job listings that offer Hybrid mode of work, but the salary range is not explicitly mentioned. However, I can try to analyze the job listings that offer Hybrid mode of work and see if I can find any information about the salary range. 

From the observations, I can see that the job listings that offer Hybrid mode of work are from companies such as Google LLC. Based on industry standards and market trends, I can infer that the salary range for these job listings is likely to be more than 3L.

Action: None
Final Answer: Based on the analysis of the job listings that offer Hybrid mode of work, I can provide the following job listings that are likely to have a salary range of more than 3L:

1. Business Analyst at Google LLC - This job listing offers Hybrid mode of work and is likely to have a salary range of more than 3L based on industry standards and market trends.
2. Senior Backend Developer at Google LLC - This job listing offers Hybrid mode of work and is likely to have a salary range of more than 3L based on industry standards and market trends.

Please note that the salary range is not explicitly mentioned in the job listings, and the inference is based on industry standards and market trends. It is recommended to contact the companies directly to confirm the salary range for these job listings.

> Finished chain.
INFO:     Response for POST method completed with status code 200 in 13.85s
INFO:     127.0.0.1:50922 - "POST /ai/ask-agent?query=Find%20out%20job%20listings%20that%20offer%20Hybrid%20mode%20of%20work%20and%20the%20salary%20range%20is%20more%20than%203L HTTP/1.1" 200 OK
```

### Response body output
```json
{
    "status": "success",
    "output": "Based on the analysis of the job listings that offer Hybrid mode of work, I can provide the following job listings that are likely to have a salary range of more than 3L:\n\n1. Business Analyst at Google LLC - This job listing offers Hybrid mode of work and is likely to have a salary range of more than 3L based on industry standards and market trends.\n2. Senior Backend Developer at Google LLC - This job listing offers Hybrid mode of work and is likely to have a salary range of more than 3L based on industry standards and market trends.\n\nPlease note that the salary range is not explicitly mentioned in the job listings, and the inference is based on industry standards and market trends. It is recommended to contact the companies directly to confirm the salary range for these job listings."
}
```

### Testing the AI Agent with irrelevant questions 
```bash
What is the weather in California today?
```

```bash
> Entering new AgentExecutor chain...
Thought: Do I need to use a tool? No
The tools provided are related to job searching and recruitment, and none of them seem to be relevant to checking the weather in California. 

Final Answer: I'm afraid I'm a Job Board Executive Agent and do not have access to real-time weather information. However, I can suggest checking a weather website or app, such as AccuWeather or Weather.com, for the current weather in California. If you have any job-related questions or need assistance with finding a job, I'd be happy to help!

> Finished chain.
INFO:     Response for POST method completed with status code 200 in 0.77s
```

### Response body output
```json
{
    "status": "success",
    "output": "I'm afraid I'm a Job Board Executive Agent and do not have access to real-time weather information. However, I can suggest checking a weather website or app, such as AccuWeather or Weather.com, for the current weather in California. If you have any job-related questions or need assistance with finding a job, I'd be happy to help!"
}
```