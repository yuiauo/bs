from logging.config import fileConfig

from alembic import context
from bet_maker.settings import settings
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from bet_maker.models import Base


config = context.config
config.set_main_option(
    name='sqlalchemy.url',
    value=settings.env.PG_MIGRATIONS_URL
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations()
