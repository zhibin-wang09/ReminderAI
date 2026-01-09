from pydantic import BaseModel

class Reminder(BaseModel):
    transcription: str