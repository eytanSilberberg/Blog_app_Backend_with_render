from fastapi import FastAPI
from routes import post

app = FastAPI()

app.include_router(post.router, prefix="/api/v1")
