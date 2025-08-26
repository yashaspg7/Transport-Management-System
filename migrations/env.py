"""
Alembic environment configuration with asyncpg support for SQLModel-based TMS.

This module configures Alembic to work with asyncpg driver directly, using
SQLAlchemy's async capabilities for database migrations.
"""

import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_database_url() -> str:
    """
    Get the async database URL from application settings.

    Returns:
        str: Async database URL for asyncpg
    """
    try:
        from src.core.config import settings

        url = settings.DATABASE_URL
        print(f"Using database URL: {url}")
        return url

    except ImportError as e:
        print(f"Warning: Could not import settings: {e}")
        # Fallback to a default async URL
        fallback_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/tms_db"
        print(f"Using fallback URL: {fallback_url}")
        return fallback_url
    except Exception as e:
        print(f"Error getting database URL: {e}")
        # Fallback to a default async URL
        fallback_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/tms_db"
        print(f"Using fallback URL: {fallback_url}")
        return fallback_url


def load_models():
    """
    Import all SQLModel models to register them with the metadata.
    """
    try:
        print("Loading SQLModel models...")

        # Import all models to register them with SQLModel metadata
        from src.models.vendor import Vendor

        # Add future model imports here as you create them:
        # from src.models.customer import Customer
        # from src.models.order import Order
        # from src.models.vehicle import Vehicle

        models = [Vendor]  # Add future models to this list
        print(f"Loaded {len(models)} models: {[model.__name__ for model in models]}")

    except ImportError as e:
        print(f"Warning: Could not import models: {e}")
        print("Make sure all models are properly defined and importable")
    except Exception as e:
        print(f"Error loading models: {e}")


# Load all models to register with SQLModel metadata
load_models()

# Set target metadata for autogenerate support
target_metadata = SQLModel.metadata

# Set the database URL in config
try:
    database_url = get_database_url()
    config.set_main_option("sqlalchemy.url", database_url)
except Exception as e:
    print(f"Error setting database URL: {e}")


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine.
    This approach generates SQL scripts rather than executing them directly.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Run migrations with the provided connection.

    Args:
        connection: SQLAlchemy database connection
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        # Additional options for better migration detection
        render_item=None,
        include_name=None,
        include_schemas=False,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Run migrations in async mode using asyncpg.

    This creates an async engine and runs migrations within an async context.
    """
    try:
        # Get the database URL
        database_url = get_database_url()

        # Create async engine with asyncpg
        connectable = create_async_engine(
            database_url,
            poolclass=pool.NullPool,
            echo=False,  # Set to True for SQL debugging
        )

        # Run migrations in async context
        async with connectable.connect() as connection:
            # Run the migration in a sync context within the async connection
            await connection.run_sync(do_run_migrations)

        # Dispose of the engine
        await connectable.dispose()

    except Exception as e:
        print(f"Error in async migrations: {e}")
        print("Please check your database connection and URL configuration")
        print("Make sure PostgreSQL is running and accessible")
        raise


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode using asyncpg.

    This creates an async engine and runs the migrations asynchronously.
    """
    try:
        # Run the async migrations
        asyncio.run(run_async_migrations())

    except Exception as e:
        print(f"Error running online migrations: {e}")
        raise


# Determine which migration mode to use
if context.is_offline_mode():
    print("Running migrations in offline mode...")
    run_migrations_offline()
else:
    print("Running migrations in online mode with asyncpg...")
    run_migrations_online()
