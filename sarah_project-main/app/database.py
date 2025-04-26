from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Database URL
# Use data directory for Fly.io persistent volume
data_dir = os.environ.get("FLY_APP") and "/app/data" or "."
os.makedirs(data_dir, exist_ok=True)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{data_dir}/flashcard_app.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database initialization function
def init_db():
    Base.metadata.create_all(bind=engine)
