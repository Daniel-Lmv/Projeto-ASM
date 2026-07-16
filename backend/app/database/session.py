from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections.abc import Generator
from app.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

def get_session() -> Generator:
    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()