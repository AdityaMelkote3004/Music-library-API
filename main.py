from fastapi import FastAPI
from app.api import songs
from app.models import Base
from app.db import engine

app = FastAPI(title="Music Library API")

Base.metadata.create_all(bind=engine)

app.include_router(songs.router)
