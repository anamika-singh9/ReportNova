from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

from config.settings import settings
from app.database.base import Base

# Import models so Alembic can detect their tables
from app.models.user import User
from app.models.report import Report


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Use DATABASE_URL from .env
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL.replace("%", "%%"),
)


# Alembic will compare this metadata with the database
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without creating an Engine."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with a database connection."""

    configuration = config.get_section(
        config.config_ini_section,
        {}
    )

    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()