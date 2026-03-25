from pydantic import BaseModel, Field
from enum import Enum

class Semester(str, Enum):
    FALL = "Fall"
    SPRING = "Spring"
    SUMMER = "Summer"

class Enrolement(BaseModel):
    enrolement_id: int | None = None
    course_name: str
    semester: Semester

class Student(BaseModel):
    student_id: int | None = None
    full_name: str
    enrolements: list[Enrolement] = []