
from pydantic import BaseModel

from .participant_profile import ParticipantProfile
from .question_answer_content import QuestionAnswerContent

class CallTranscript(BaseModel):
    id: str
    title: str
    company_id: str
    company_name: str
    date: str
    management_section_content: str
    management_section_tags: str
    sentiment: str
    question_and_answer_content: [QuestionAnswerContent]
    participant_profiles: [ParticipantProfile]