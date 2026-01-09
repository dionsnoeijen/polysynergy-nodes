"""Database session management for section nodes"""

import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, Session


def _create_engine_from_env(prefix: str, defaults: dict):
    """
    Create SQLAlchemy engine from individual environment variables.

    Args:
        prefix: Environment variable prefix (e.g., 'DATABASE' or 'SECTIONS_DB')
        defaults: Default values for host, port, database, username, password
    """
    url = URL.create(
        drivername="postgresql",
        username=os.getenv(f'{prefix}_USER', defaults.get('username')),
        password=os.getenv(f'{prefix}_PASSWORD', defaults.get('password')),
        host=os.getenv(f'{prefix}_HOST', defaults.get('host')),
        port=int(os.getenv(f'{prefix}_PORT', defaults.get('port', 5432))),
        database=os.getenv(f'{prefix}_NAME', defaults.get('database')),
    )
    print(f"[db_session] {prefix} -> {url.render_as_string(hide_password=True)}")
    return create_engine(url, pool_pre_ping=True)


# Create engines from environment variables
main_engine = _create_engine_from_env('DATABASE', {
    'username': 'polysynergy_user',
    'password': 'securepassword',
    'host': 'db',
    'port': 5432,
    'database': 'ps_db',
})

sections_engine = _create_engine_from_env('SECTIONS_DB', {
    'username': 'sections_user',
    'password': 'sections_password',
    'host': 'sections_db',
    'port': 5432,
    'database': 'sections_db',
})

# Session factories
MainSessionLocal = sessionmaker(bind=main_engine, autoflush=False, autocommit=False)
SectionsSessionLocal = sessionmaker(bind=sections_engine, autoflush=False, autocommit=False)

# Export URL for use in other modules (e.g., NodeSectionRepository)
# IMPORTANT: Use render_as_string(hide_password=False) because str(url) masks password to '***'
SECTIONS_DATABASE_URL = sections_engine.url.render_as_string(hide_password=False)


@contextmanager
def get_main_db_session():
    """
    Context manager for main database session.

    This database contains section metadata (configurations).

    Usage:
        with get_main_db_session() as db:
            section_repo = NodeSectionRepository(db)
            section_info = section_repo.get_by_id(section_id)
    """
    db = MainSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_sections_db_session():
    """
    Context manager for sections database session.

    This database contains the actual content tables for sections.

    Usage:
        with get_sections_db_session() as db:
            # Direct SQL queries on content tables
            result = db.execute(text("SELECT * FROM ..."))
    """
    db = SectionsSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
