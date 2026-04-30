from fastapi import FastAPI
from database import engine
from routers import analytics


import models
from routers import logs

app = FastAPI(title="TraceIQ API")

app.include_router(analytics.router)

@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

app.include_router(logs.router)

@app.get("/")
def home():
    return {"message": "TraceIQ backend running with DB"}