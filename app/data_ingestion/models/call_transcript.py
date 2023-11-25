
from pydantic import BaseModel
from typing import List

from .participant_profile import ParticipantProfile
from .question_answer_content import QuestionAnswerContent

class CallTranscript(BaseModel):
    id: str
    title: str
    company_id: str
    company_name: str = None
    date: str
    management_section_content: str
    management_section_tags: str
    sentiment: str
    question_and_answer_content: List[QuestionAnswerContent]
    participant_profiles: List[ParticipantProfile]