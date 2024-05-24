from __future__ import with_statement
import logging.config
from alembic import context
from sqlalchemy import engine_from_config, pool
from flask import current_app

# Включаем конфигурацию логирования
logging.config.fileConfig(context.config.config_file_name)

# Вытаскиваем конфигурацию из текущего приложения Flask
config = context.config
config.set_main_option('sqlalchemy.url', current_app.config.get('SQLALCHEMY_DATABASE_URI'))

target_metadata = current_app.extensions['migrate'].db.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = current_app.extensions['migrate'].db.engine

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
