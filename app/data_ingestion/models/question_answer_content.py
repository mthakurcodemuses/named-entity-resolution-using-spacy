from pydantic import BaseModel

class QuestionAnswerContent(BaseModel):
    question: str
    question_participant_id: str
    answer: [str]