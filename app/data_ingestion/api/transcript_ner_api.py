from fastapi import APIRouter, status
from app.data_ingestion.processor.text_processor import TextProcessor
from app.data_ingestion.utils.app_logger import app_logger as log

transcript_ner_router = APIRouter()

@transcript_ner_router.get("/extract/transcript/entities", status_code=status.HTTP_200_OK)
def detect_entities_in_transcript():
    text_processor = TextProcessor()
    with open("app/data_ingestion/data/transcript.xml", "r") as f:
        transcript = f.read()
        entities = text_processor.get_entities(transcript)
        log.info(f"Extract Entities from Transcript {entities}")
