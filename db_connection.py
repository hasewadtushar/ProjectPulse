from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Update username and password
DATABASE_URL = "postgresql://postgres:tushar123@localhost:5432/youtube_db"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
