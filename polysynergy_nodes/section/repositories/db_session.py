"""Database session management for section nodes"""

import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


# Get main database URL (where sections are configured)
# This is the same database that api-local uses for storing section metadata
MAIN_DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://polysynergy_user:securepassword@db:5432/ps_db'
)

# Get sections database URL (where actual content tables live)
# This is where the dynamic section content is stored
SECTIONS_DATABASE_URL = os.getenv(
    'SECTIONS_DATABASE_URL',
    'postgresql://sections_user:sections_password@sections_db:5432/sections_db'
)

# Debug logging
print(f"[db_session] MAIN_DATABASE_URL: {MAIN_DATABASE_URL}")
print(f"[db_session] SECTIONS_DATABASE_URL: {SECTIONS_DATABASE_URL}")

# Create engines and session factories
main_engine = create_engine(MAIN_DATABASE_URL, pool_pre_ping=True)
MainSessionLocal = sessionmaker(bind=main_engine, autoflush=False, autocommit=False)

sections_engine = create_engine(SECTIONS_DATABASE_URL, pool_pre_ping=True)
SectionsSessionLocal = sessionmaker(bind=sections_engine, autoflush=False, autocommit=False)


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
