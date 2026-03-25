from fastapi import APIRouter, HTTPException, Request, Form 
from fastapi.responses import HTMLResponse, RedirectResponse 
from fastapi.templating import Jinja2Templates
from models import Student
from database import managed_db

enrollment_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@enrollment_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    with managed_db() as db:
        data = db.get_all()
    return templates.TemplateResponse("enrollment.html", {
        "request": request,
        "items": data
    })

@enrollment_router.get("/students/")
async def list_students():
    with managed_db() as db:
        return db.get_all()

@enrollment_router.get("/students/{student_id}")
def get_student_by_id(student_id: int): 
    with managed_db() as db:
        student = db.get(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

@enrollment_router.post("/students/")
def add_student(student: Student):
    with managed_db() as db:
        new_id = db.create(student)
    return {"message": "Student added", "student_id": new_id}

@enrollment_router.post("/home")
async def add_student_from_form(full_name: str = Form(...)):
    temp_student = Student(full_name=full_name, enrolements=[])
    with managed_db() as db:
        db.create(temp_student)
    return RedirectResponse(url="/home", status_code=303)

@enrollment_router.put("/students/{student_id}")
async def update_student(student_id: int, student_update: Student): 
    with managed_db() as db:
        updated = db.update(student_id, student_update)
        if not updated:
            raise HTTPException(status_code=404, detail="Student not found")
        return updated

@enrollment_router.delete("/students/{student_id}")
async def delete_student(student_id: int):
    with managed_db() as db:
        if not db.get(student_id):
            raise HTTPException(status_code=404, detail="Student not found")
        db.delete(student_id)
    return {"detail": "Student deleted successfully"}