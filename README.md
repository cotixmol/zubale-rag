# Product Query Bot (RAG System)

A Python service that answers user queries. It uses FastAPI, PostgreSQL with pgvector, and a background worker to process queries asynchronously.

-----

## Features

  - **Semantic Search:** Identifies similar products using vector embeddings.
  - **Stubbed LLM Response:** Returns a generated answer based on retrieved product context.
  - **Webhook Callback:** Delivers final answers to a configurable callback URL.
  - **Asynchronous Processing:** Enqueues queries for quick responses.
  - **Dockerized Deployment:** Setup with Docker Compose.

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

Now, you can edit the `.env` file. These are the values that work without any secret being exposed, but you can customize them according to your machine.

```
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

The system is designed to process product queries efficiently without making the user wait.

1.  **Request Enqueue:** A user sends a question to the `/query` endpoint. The API immediately accepts the request and places it into a processing queue, then responds with a `202 Accepted` status.
2.  **Background Worker:** A separate worker process, running in the background, picks up the query from the queue.
3.  **Retrieval:** The worker finds the most relevant products by converting the user's query into a vector embedding and comparing it against the product embeddings in the database.
4.  **Generation:** It then passes the retrieved product information (the context) and the original query to a stubbed LLM function, which generates an answer.
5.  **Callback:** Finally, the worker sends the generated answer to the configured `CALLBACK_URL`.

### Database Setup Script

When the application starts for the first time, the `script/db_setup.py` file automatically prepares the database. Here's what it does:

  * **Initializes pgvector:** It enables the `vector` extension in PostgreSQL, which is necessary for storing and searching embeddings.
  * **Creates Product Table:** It defines and creates a `products` table to store product descriptions and their corresponding vector embeddings.
  * **Seeds the Data:** The script takes the list of `PRODUCT_DESCRIPTIONS`, uses the `all-MiniLM-L6-v2` model to convert each description into a numerical vector (an embedding), and inserts both the text and the vector into the database. This process is what enables semantic search.

### Viewing the Final Answer

To make testing simple, the `CALLBACK_URL` in the `.env` file is pre-configured to point back to an endpoint within the API itself (`http://api:8000/callback`). This endpoint's only job is to log the answer it receives.

To see the final, generated answer for your query, you can watch the logs from the API container.

```sh
# Using the shortcut
make logs

# Or with Docker Compose directly
docker-compose logs -f api
```

After you submit a query, you will see a log entry similar to this appear in the terminal:

```
INFO:     Callback Payload:
{'user_id': 'user123', 'answer': '\n        LLM stubbed generated answer based on the prompt: \n        \n\n        Product catalog:\n        - Wireless Bluetooth Headphones: Features noise-cancellation, a 20-hour battery life, and comes with a charging case.\n- Noise-Cancelling Earplugs: Reusable silicone design to reduce ambient noise, with multiple size options for a snug fit.\n        \n        What the user asked for: I need something to block out noise\n        \n        Provide an answer based on the Product Catalog and the what the user asked for.\n        \n        '}
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
  - **src/api/routes.py** — Defines the API endpoints (`/query`, `/callback`).
  - **src/services/** — Contains the core logic for retrieval, generation, and callbacks.
  - **src/repositories/** — Handles all database interactions.
  - **src/config/** — Manages logging, secrets, the queue, and DB configuration.
  - **script/db\_setup.py** — Initializes and seeds the database with product data.

-----

## Requirements

  - Docker & Docker Compose
  - Python 3.11

-----

## Testing

The project includes unit tests to ensure key components work as expected. To run the test:

```sh
pytest
```