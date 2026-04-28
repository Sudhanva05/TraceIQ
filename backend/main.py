from fastapi import FastAPI

app= FastAPI(title = "TraceIQ")

@app.get("/")
def home():
    return {"message": "Welcome Backend is working" }