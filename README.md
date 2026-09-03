# AI Plagiarism Detector

A full-stack plagiarism detection system that combines **semantic similarity**
(sentence embeddings) with **lexical similarity** (TF-IDF n-gram overlap) to
catch both paraphrased and near-verbatim copying — with sentence-level match
highlighting and corpus-wide similarity search via `pgvector`.

## Architecture

```
React (Vite)  →  Spring Boot API  →  FastAPI AI Microservice
  :5173             :8080                  :8000
                      │                      │
                      └──────► PostgreSQL + pgvector ◄──────┘
                                    :5432

Everything containerized with Docker Compose; CI via GitHub Actions.
```

**Why this architecture:** the AI microservice is isolated from the business
logic (auth, persistence, request routing) so it can be scaled, redeployed,
or swapped independently — e.g. moved to a GPU-backed instance for larger
models without touching the backend. This mirrors how ML features are
actually shipped in production systems (a lightweight app server calling
out to a dedicated inference service) rather than embedding ML code in the
same process as the web layer.

## How the detection works

1. **Text extraction** — PyMuPDF (PDF) / python-docx (DOCX) / plain text pull
   raw text out of uploads regardless of format.
2. **Chunking + embedding** — text is split into overlapping word chunks and
   sentences, embedded with `all-MiniLM-L6-v2` (Sentence-Transformers).
3. **Two similarity signals, blended:**
   - **Semantic** (65% weight): cosine similarity between document
     embeddings — catches reworded/paraphrased plagiarism that keyword
     matching misses.
   - **Lexical** (35% weight): TF-IDF over 1–3 word n-grams — catches
     near-verbatim copying, which embeddings can sometimes under-score.
4. **Sentence-level matching** — every sentence in doc A is compared against
   every sentence in doc B; pairs above a similarity threshold are surfaced
   in the UI so the user sees *exactly* which sentences were flagged, not
   just an aggregate score.
5. **Corpus-wide search** — `pgvector`'s cosine-distance operator (`<=>`)
   does nearest-neighbor search over every previously submitted document,
   so a new submission is checked against everything in the database, not
   just one file at a time.

## Features

- Upload PDF / DOCX / TXT files
- Direct A/B document comparison with sentence-level highlighting
- "Analyze" mode: checks a document against the entire stored corpus and
  indexes it for future checks
- JWT-based auth (register/login) with submission history per user
- Fully dockerized; one command spins up all four services

## Running locally

**Requirements:** Docker + Docker Compose.

```bash
git clone <your-repo-url>
cd plagiarism-detector
docker compose up --build
```

Then visit:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8080
- AI service docs (Swagger): http://localhost:8000/docs

### Running services individually (development)

```bash
# AI microservice
cd ai-service
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload --port 8000

# Backend
cd backend
mvn spring-boot:run

# Frontend
cd frontend
npm install
npm run dev
```

You'll need a local Postgres with the `vector` extension, or just run
`docker compose up db` and point the other services at it.

## Project structure

```
plagiarism-detector/
├── frontend/           # React + Vite SPA
├── backend/             # Spring Boot REST API (auth, persistence, orchestration)
├── ai-service/           # FastAPI microservice (extraction, embeddings, similarity)
├── db/init.sql            # pgvector extension setup
├── docker-compose.yml      # orchestrates all 4 services
└── .github/workflows/ci.yml # build + test pipeline
```

## API overview

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register` | — | Create an account, returns JWT |
| POST | `/api/auth/login` | — | Log in, returns JWT |
| POST | `/api/documents/compare` | — | Compare two uploaded files directly |
| POST | `/api/documents/analyze` | ✅ | Full check against the corpus; persists result |
| GET | `/api/documents/history` | ✅ | List the current user's past submissions |

## Possible extensions

- Swap `all-MiniLM-L6-v2` for a larger model (e.g. `all-mpnet-base-v2`) behind
  a feature flag and A/B the accuracy/latency tradeoff
- Add a web-search-backed check against external sources (not just the
  internal corpus)
- Async processing with a queue (Celery/RabbitMQ) for large document batches
- Per-paragraph plagiarism heatmap in the UI instead of a flat sentence list

## Resume bullet (adapt with real numbers once you've run it)

> Built a full-stack AI plagiarism detection system (React, Spring Boot,
> FastAPI, PostgreSQL/pgvector) that combines sentence-transformer embeddings
> with TF-IDF lexical analysis to detect both paraphrased and verbatim
> plagiarism; implemented corpus-wide nearest-neighbor search with pgvector,
> JWT authentication, and a Dockerized CI/CD pipeline via GitHub Actions.

Fill in real metrics once you've tested it: how many documents/sec it can
process, embedding latency, detection accuracy on a labeled test set (you
could build a small one from Wikipedia paraphrase pairs), etc. — numbers are
what make a resume bullet credible in an interview.
