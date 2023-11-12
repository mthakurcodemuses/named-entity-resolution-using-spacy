from fastapi import FastAPI

from app.data_ingestion.api.message_sender_api import message_sender_router

app = FastAPI()
app.include_router(message_sender_router)
