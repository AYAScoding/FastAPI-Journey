from pydantic import BaseModel
from typing import List

class PollCreate(BaseModel):
    question: str
    options: List[str]

class VoteRequest(BaseModel):
    option: str