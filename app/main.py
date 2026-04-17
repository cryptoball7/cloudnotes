from fastapi import FastAPI
from app.core.database import engine, Base

from app.models import user, note  # IMPORTANT

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "CloudNotes API running with DB"}
