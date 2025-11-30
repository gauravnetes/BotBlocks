import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from db import models
from db.database import engine

from api import bot_routes, chat_routes

if not os.path.exists('./data'):
    os.makedirs('./data')

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BotBlocks Backend",
    description="API for building, managing, and serving chatbots."
)

origins = [
    "http://localhost",
    "http://localhost:8501",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(bot_routes.router)
app.include_router(chat_routes.router)

@app.get("/api/v1/health")
def get_health():
    return {"status": "ok", "service": "backend"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)