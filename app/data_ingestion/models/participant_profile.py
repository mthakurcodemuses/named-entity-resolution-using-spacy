from pydantic import BaseModel
class ParticipantProfile(BaseModel):
    id: str
    type: str
    name: str
    affiliated_company: str
    affiliated_company_id: str
    designation: str