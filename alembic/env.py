import sys
import os

sys.path.append(os.getcwd())
import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

from sqlmodel import SQLModel

load_dotenv()

config = context.config


from app.models.user import User
from app.models.signal import Signal

target_metadata = SQLModel.metadata

DATABASE_URL = os.getenv("DATABASE_URL")


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async def run():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()