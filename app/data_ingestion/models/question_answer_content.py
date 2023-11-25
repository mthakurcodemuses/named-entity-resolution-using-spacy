from pydantic import BaseModel
from typing import List

class QuestionAnswerContent(BaseModel):
    question: str
    question_participant_id: str
    answer: List[str]