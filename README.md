# ReviewPal — LLM-Based Restaurant Review Generation Service

A production-style **LLM inference service prototype** built with FastAPI.
It generates restaurant reviews from user input, grounded by retrieval 
layer over a local restaurant knowledge base.

---

## Project Structure

```
Review_Generator/
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── api/
│   │   └── routes.py           # API endpoints
│   ├── core/
│   │   ├── config.py           # Settings (pydantic-settings)
│   │   └── logging.py          # Logger setup
│   ├── schemas/
│   │   └── contract.py         # Pydantic request models
│   ├── services/
│   │   ├── retrieval.py        # Context retrieval
│   │   ├── generation.py       # OpenAI call
│   │   └── pipeline.py         # Orchestration (retrieve → prompt → generate)
│   └── utils/
│       └── metrics.py          # In-memory counters
├── data/
│   └── restaurants_info.json   # Local knowledge base
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── .dockerignore
└── README.md
```

---

## Quick Start (Local)

### 1. Clone and enter the project

```bash
git clone https://github.com/Ming031121/Review_Generator.git
cd Review_Generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn app.main:app --reload
```

Service will be available at:
- API: http://127.0.0.1:8000
---

## Environment Variables

| Name | Required | Default | Description |
|------|----------|---------|-------------|
| `OPENAI_API_KEY` | yes | — | OpenAI API key |
| `MODEL_NAME` | no | `gpt-4o-mini` | Model used for generation |
| `MAX_OUTPUT_TOKENS` | no | `300` | LLM max output tokens |
| `REQUEST_TIMEOUT_SECONDS` | no | `30` | Upstream request timeout |
| `APP_NAME` | no | `ReviewPal API` | App display name |
| `APP_ENV` | no | `dev` | Environment name |
| `APP_DEBUG` | no | `false` | Debug flag |

See [`.env.example`](.env.example) for a template.
---
