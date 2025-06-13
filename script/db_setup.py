import asyncpg
from sentence_transformers import SentenceTransformer  # Back to the simple import
from script.data.products_description import PRODUCT_DESCRIPTIONS
from src.config.secrets import secrets


async def initialize_database(pool: asyncpg.Pool):
    """
    Uses the application's connection pool to initialize the database.
    This version uses the simpler 'sentence-transformers' library.
    """
    async with pool.acquire() as conn:
        async with conn.transaction():
            print(
                f"DB_SETUP: Loading embedding model '{secrets.EMBEDDING_MODEL_NAME}'..."
            )
            model = SentenceTransformer(secrets.EMBEDDING_MODEL_NAME)
            embedding_dim = model.get_sentence_embedding_dimension()

            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL UNIQUE,
                embedding VECTOR({embedding_dim})
            );
            """

            await conn.execute(create_table_query)
            print("DB_SETUP: Table 'products' is ready.")

            product_count = await conn.fetchval("SELECT COUNT(*) FROM products;")
            if product_count == 0:
                print("DB_SETUP: 'products' table is empty. Seeding data...")

                embeddings = model.encode(PRODUCT_DESCRIPTIONS, show_progress_bar=True)

                records_to_insert = [
                    (desc, emb.tolist())
                    for desc, emb in zip(PRODUCT_DESCRIPTIONS, embeddings)
                ]

                await conn.executemany(
                    "INSERT INTO products (content, embedding) VALUES ($1, $2)",
                    records_to_insert,
                )
                print(
                    f"DB_SETUP: Successfully seeded {len(records_to_insert)} products."
                )
            else:
                print(
                    "DB_SETUP: 'products' table already contains data. Skipping seeding."
                )
