from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from . import config


DATABASE_URL = f"postgresql://{config.settings.database_username}:{config.settings.database_password}@{config.settings.database_hostname}/{config.settings.database_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
