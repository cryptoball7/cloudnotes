from fastapi import FastAPI
from app.core.database import engine, Base

from app.models import user, note  # IMPORTANT

from app.api import auth, notes, health

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "CloudNotes API running with DB and auth"}

app.include_router(auth.router, prefix="/auth")
app.include_router(notes.router, prefix="/notes")
app.include_router(health.router, prefix="/health")

