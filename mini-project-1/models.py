from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

app = FastAPI()

class Semester(str, Enum):
    FALL = "Fall"
    SPRING = "Spring"
    SUMMER = "Summer"


class Enrolement(BaseModel):
    enrolement_id: int = Field(..., gt=0)
    course_name: str = Field(..., min_length=2, max_length=50)
    semester: Semester


class Student(BaseModel):
    student_id: int = Field(..., gt=0)
    full_name: str = Field(..., min_length=2, max_length=50)
    enrolements: list[Enrolement] = []



