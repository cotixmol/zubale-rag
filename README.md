# zubale-rag

Python 3.11.11

## Docker Setup

1. **Create a `.env` file in the project root:**
   ```
   POSTGRES_USER=youruser
   POSTGRES_PASSWORD=yourpassword
   POSTGRES_DB=yourdb
   DATABASE_URL=postgresql://<youruser>:<yourpassword>@db:5432/<yourdb>
   ```
   Replace `<youruser>`, `<yourpassword>`, and `<yourdb>` with your desired values.

2. **Build and start the containers:**
   ```sh
   docker-compose up --build
   ```
   ```sh
   make up
   ```

3. **Stop the containers:**
   ```sh
   docker-compose down
   ```
   ```sh
   make down
   ```

4. **View logs:**
   ```sh
   docker-compose logs -f
   ```
   ```sh
   make logs
   ```

## Project Structure

- **api**: FastAPI app, served by Uvicorn on port 8000.
- **db**: PostgreSQL 16 with pgvector extension, data persisted in a Docker volume.

## Notes

- The API will be available at [http://localhost:8000](http://localhost:8000).
- Database data is persisted in the `pgvector_data` Docker volume.
- Environment variables are loaded from the `.env` file for both the API and database containers.