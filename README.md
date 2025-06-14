# Product Query Bot (RAG System)

A Python-based API that answers user queries using Retrieval-Augmented Generation. It leverages FastAPI, PostgreSQL with pgvector, and a background worker to process queries asynchronously.

---

## Features

- **Semantic Search:** Identifies similar products using vector embeddings.
- **Stubbed LLM Response:** Returns a generated answer based on retrieved product context.
- **Webhook Callback:** Delivers final answers to a configurable callback URL.
- **Asynchronous Processing:** Enqueues queries for quick responses.
- **Dockerized Deployment:** Easy setup with Docker Compose.

---

## Quick Start

### 1. Clone and Navigate

```sh
git clone https://github.com/cotixmol/zubale-rag
cd zubale-rag
```

### 2. Configure Environment

Copy the example environment file and customize values:

```sh
cp .env.example .env
```

Edit `.env` with database credentials and callback URL. For instance:

```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name
DATABASE_URL=postgresql://user:password@db:5432/db_name
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
LOG_LEVEL=INFO
CALLBACK_URL=http://www.example.com
```

### 3. Launch

Use Docker Compose or Make commands:

```sh
docker-compose up --build
# or
make up
```

Visit [http://localhost:8000](http://localhost:8000) for the API.

### 4. Stop / Restart

```sh
docker-compose down
# or
make down

docker-compose restart
# or
make restart
```

Check logs with:

```sh
docker-compose logs -f
# or
make logs
```

---

## How It Works

1. **Request Enqueue:** User calls `/query` with their prompt; it’s placed in a queue.  
2. **Background Worker:**  
   - Finds relevant products via semantic search.  
   - Generates an answer with a stubbed LLM.  
   - Sends the response to the specified callback URL.  
3. **Database:** The PostgreSQL + pgvector database supports vector-based similarity.

---

## Project Structure

- **main.py** — FastAPI setup, background worker.  
- **src/api/routes.py** — Defines the API endpoints.  
- **src/services/** — Retrieval, generation, and callback logic.  
- **src/repositories/** — Database interaction.  
- **src/config/** — Logging, secrets, queue, and DB configuration.  
- **script/db_setup.py** — Initializes and seeds the database.

---

## Requirements

- Docker, Docker Compose  
- Python 3.11

---

## Testing

Run tests:

```sh
pytest
```

---