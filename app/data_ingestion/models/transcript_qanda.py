from pydantic import BaseModel

class TranscriptQandA(BaseModel):
    qanda_id: str
    transcript_id: str
    content: str