from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    message: str
    type: str

class SurveyCreate(BaseModel):
    responses: dict
