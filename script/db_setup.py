import logging
import asyncpg
from sentence_transformers import SentenceTransformer
from script.data.products_description import PRODUCT_DESCRIPTIONS
from src.config.secrets import secrets

logger = logging.getLogger(__name__)


async def initialize_database(pool: asyncpg.Pool, reset: bool = True):
    """
    Uses the application's connection pool to initialize the database.
    If reset=True, drops and recreates the products table.
    """
    logger.info("Starting database initialization...")
    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                logger.info(
                    f"Loading embedding model '{secrets.EMBEDDING_MODEL_NAME}'..."
                )
                model = SentenceTransformer(secrets.EMBEDDING_MODEL_NAME)
                embedding_dim = model.get_sentence_embedding_dimension()

                await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")

                if reset:
                    logger.warning("Dropping and recreating 'products' table!")
                    await conn.execute("DROP TABLE IF EXISTS products;")

                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL UNIQUE,
                    embedding VECTOR({embedding_dim})
                );
                """
                await conn.execute(create_table_query)
                logger.info("Table 'products' is ready.")

                if reset or (await conn.fetchval("SELECT COUNT(*) FROM products;")) == 0:
                    if not reset:
                        logger.info("'products' table is empty. Seeding data...")
                    embeddings = model.encode(
                        PRODUCT_DESCRIPTIONS, show_progress_bar=True
                    )
                    records_to_insert = [
                        (desc, str(emb.tolist()))
                        for desc, emb in zip(PRODUCT_DESCRIPTIONS, embeddings)
                    ]
                    await conn.executemany(
                        "INSERT INTO products (content, embedding) VALUES ($1, $2)",
                        records_to_insert,
                    )
                    logger.info(
                        f"Successfully seeded {len(records_to_insert)} products."
                    )
                else:
                    logger.info(
                        "'products' table already contains data. Skipping seeding."
                    )
    except Exception as e:
        logger.error(f"Database initialization failed: {e}", exc_info=True)
        raise
