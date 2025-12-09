from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database stored in the project folder
DATABASE_URL = "sqlite:///providers.db"

# create an engine (the connection to our DB)
engine = create_engine(DATABASE_URL, echo=True, future=True)

# session setup (used to talk to the DB)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# base class for all database models
Base = declarative_base()
