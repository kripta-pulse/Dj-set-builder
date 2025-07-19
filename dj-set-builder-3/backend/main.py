# FastAPI backend
from fastapi import FastAPI
app = FastAPI()

from gpt_generator import router as gpt_router
app.include_router(gpt_router)