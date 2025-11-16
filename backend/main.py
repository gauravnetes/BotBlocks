from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/")
def read_root():
    return {"Hello": "From FastAPI Backend"}

@app.get("/api/v1/health")
def get_health():
    """
    A simple health check endpoint.
    """
    return {"status": "ok", "service": "backend"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)