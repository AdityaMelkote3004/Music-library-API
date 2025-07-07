DATABASE_URL = "sqlite:///./music.db"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


engine = create_engine(DATABASE_URL, 
                       connect_args={"check_same_thread": False}
                       )

from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
