from typing import Annotated
from fastapi import Depends
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core import settings

logger = logging.getLogger("uvicorn.error")

Base = declarative_base()

engine = create_engine(url=settings.DATABASE_URL)

# Verify database connection on startup
try:
    with engine.connect() as connection:
        logger.info("🟢 Database connection established successfully.")
except OperationalError as e:
    logger.error("🔴 Database connection failed!")
    logger.error(f"OperationalError: {e}")

local_session = sessionmaker(bind=engine)

def get_db():
    session = local_session()
    try:
        yield session
    finally:
        session.close()


DB_Session = Annotated[
    Session,
    Depends(get_db),
]