from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core import settings
Base = declarative_base()

engine = create_engine(url=settings.DATABASE_URL )

local_session = sessionmaker(bind=engine)

def get_db():
    session = local_session()
    try:
        yield session
    finally:
        session.close()