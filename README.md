# Product Query Bot (RAG System)

A FastAPI-based Retrieval-Augmented Generation (RAG) system for product queries, using a LangGraph-powered multi-agent workflow, dependency injection, and a modular architecture to process queries asynchronously.

-----

## Features

  - **Semantic Search:** Identifies similar products using vector embeddings.
  - **Multi-Agent Orchestration:** Uses **LangGraph** to manage a workflow between a Retriever Agent, a Responder Agent, and a Callback Agent.
  - **Real LLM Integration:** Uses **Langchain** and **OpenAI's API** to generate human-like answers.
  - **Asynchronous Processing:** Enqueues queries for quick API responses, with a background worker handling the heavy lifting.
  - **Webhook Callback:** Delivers final answers to a configurable callback URL.
  - **Dockerized Deployment:** Setup with Docker Compose for easy launch and deployment.

-----

## Quick Start

### 1\. Clone and Navigate

First, get the project files on your local machine.

```sh
git clone https://github.com/cotixmol/zubale-rag
cd zubale-rag
```

### 2\. Configure Environment

The application uses an `.env` file for configuration. Copy the example file to create your own:

```sh
cp .env.example .env
```

Now, edit the `.env` file. You **must provide your own OpenAI API key**. The other values can be customized as needed.

```
# --- OpenAI Configuration ---
# Replace with your actual OpenAI API key
OPENAI_API_KEY="sk-..."
OPENAI_MODEL="gpt-3.5-turbo"

# --- Database and App Configuration ---
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name
DATABASE_URL=postgresql://user:password@db:5432/db_name
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
LOG_LEVEL=INFO
CALLBACK_URL=http://localhost:8000/callback
```

### 3\. Launch the Application

With Docker installed, you can launch the **entire application** (API and database) using a single command.
The `Makefile` provides convenient shortcuts for Docker commands.

To build and start the services:

```sh
# Using the shortcut
make up

# Or with Docker Compose directly
docker-compose up --build
```

The API will be available at [http://localhost:8000/docs](http://localhost:8000/docs), where you can interact with the Swagger UI.

Or, you can use Postman (or any API client) to send a request to the `/query` endpoint. Example payload:

```json
{
  "user_id": "1",
  "query": "Videogames"
}
```

-----

## How It Works

The system processes product queries through a robust, multi-agent workflow orchestrated by **LangGraph**.

1.  **Request Enqueue:** A user sends a question to the `/query` endpoint. The API immediately enqueues the request and responds with a `202 Accepted` status.
2.  **Background Worker:** A separate worker process picks up the query from the queue and hands it off to the **LangGraph Orchestrator**.
3.  **Graph Execution:** The orchestrator executes a predefined graph of agents to process the query from start to finish:
      * **Retriever Agent:** The first node in the graph. It converts the user's query into a vector embedding and finds the most relevant products from the database.
      * **Responder Agent:** The retrieved products and the original query are passed to this agent. It constructs a detailed prompt and calls the **OpenAI API** to generate a helpful, natural language answer.
      * **Callback Agent:** The final node in the graph. It takes the generated response and the user's ID and sends the final answer to the configured `CALLBACK_URL`.

### Database Setup Script

When the application starts, the `script/db_setup.py` file automatically prepares the database. Here's what it does:

  - **Initializes pgvector:** It enables the `vector` extension in PostgreSQL.
  - **Creates Product Table:** It defines and creates the `products` table to store descriptions and their embeddings.
  - **Seeds the Data:** The script uses the `all-MiniLM-L6-v2` model to convert product descriptions into vector embeddings and inserts them into the database, enabling semantic search.

### Viewing the Final Answer

To make testing simple, the `CALLBACK_URL` is pre-configured to point back to the API itself. This endpoint's only job is to log the answer it receives.

To see the final, generated answer for your query, you can watch the logs from the API container.

```sh
# Using the shortcut
make logs

# Or with Docker Compose directly
docker-compose logs -f api
```

After you submit a query, you will see a log entry in the Docker terminal:

```
{
  "user_id": "1",
  "query": "I want a gift for my two years old kid."
}
```
```
INFO:     Callback Payload:
{'user_id': '1', 'answer': "For your two-year-old kid, I recommend the Kids' Tablet from our catalog. It comes with parental controls, a protective case, and pre-loaded educational apps, making it a fun and safe gift option for your child."}
```

### 4\. Stop / Restart

To stop the application:

```sh
# Using the shortcut
make down

# Or with Docker Compose directly
docker-compose down
```

-----

## Project Structure

  - **main.py** — FastAPI setup, background worker, and application lifespan events.
  - **src/orchestration/langgraph_orchestrator.py** — Defines the multi-agent graph and workflow using LangGraph.
  - **src/api/routes.py** — Defines the API endpoints (`/query`, `/callback`).
  - **src/services/** — Contains the core logic for retrieval (vector search), generation (OpenAI calls), and callbacks.
  - **src/repositories/** — Handles all database interactions via `asyncpg`.
  - **src/config/** — Manages logging, secrets, the queue, and DB configuration.
  - **script/db\_setup.py** — Initializes and seeds the database with product data.

-----

## Requirements
  - Docker & Docker Compose
  - Python 3.11
  - An OpenAI API Key

-----

## Testing

The project includes unit tests to ensure the orchestration and key components work as expected. To run the tests:

```sh
pytest
```