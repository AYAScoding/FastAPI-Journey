from models import Enrolement, Student 
import asyncio
from fastapi import APIRouter, HTTPException, Request, Form  
from fastapi.responses import HTMLResponse, RedirectResponse 
from fastapi.templating import Jinja2Templates


enrollment_router = APIRouter()


Students_database = [
     {
        "student_id" : 1, 
        "full_name": "Ayyoub Asri",
        "enrolements": [
                {"enrolement_id": 1 ,"course_name": "Calculus 101" , "semester":"Spring"},
                {"enrolement_id": 2 ,"course_name": "Physics 101" , "semester":"Spring"},
                {"enrolement_id": 3 ,"course_name": "Programming 101" , "semester":"Spring"}
            ]
           },
    {
        "student_id" : 2, 
        "full_name": "Asiya Asri",
        "enrolements": [
            {"enrolement_id": 4 ,"course_name": "Calculus 101" , "semester":"Fall"},
            {"enrolement_id": 5 ,"course_name": "Programing 101" , "semester":"Fall"}
        ]
    }
]

templates = Jinja2Templates(directory="templates")

@enrollment_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("enrollment.html", {
        "request": request,
        "items": Students_database
    })

@enrollment_router.get("/enrollment/{id}", response_class=HTMLResponse)
async def get_item_page(request: Request, id: int):
    for item in Students_database:
        if item["student_id"] == id:
            return templates.TemplateResponse("enrollment.html", {
                "request": request,
                "enrollment": item 
            })
    raise HTTPException(status_code=404, detail=f"Enrollment with ID {id} not found")


@enrollment_router.get("/students/")
async def list_students(request: Request):
    await asyncio.sleep(1)
    return Students_database


@enrollment_router.get("/students/{student_id}")
def get_student_by_id(student_id: int): 
    for student in Students_database:
        if student["student_id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail=f"There is no student with the id = {student_id}")

@enrollment_router.post("/students/")
def add_student(student: Student):
    student_id = max((s["student_id"] for s in Students_database)) + 1 if Students_database else 1
    new_std = student.model_dump()
    new_std["student_id"] = student_id
    Students_database.append(new_std)
    raise HTTPException(status_code=201, detail="Student was added successfully")

@enrollment_router.post("/home")
async def add_student_from_form(full_name: str = Form(...)):
    student_id = max((s["student_id"] for s in Students_database)) + 1 if Students_database else 1
    new_student = {
        "student_id": student_id,
        "full_name": full_name,
        "enrolements": []
    }

    Students_database.append(new_student)
    
    return RedirectResponse(url="/home", status_code=303)

@enrollment_router.put("/students/{student_id}")
async def update_student(student_id: int, student_update: Student): 
    for std in Students_database:
        if std["student_id"] == student_id:
            std["full_name"] = student_update.full_name
            std["enrolements"] = [e.model_dump() for e in student_update.enrolements]
            raise HTTPException(status_code=204, detail="Student was Updated successfully")
    raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

@enrollment_router.delete("/students/{student_id}")
async def delete_student(student_id: int):
    for std in Students_database:
        if std["student_id"] == student_id:
            Students_database.remove(std)
            raise HTTPException(status_code=200, detail="Student is deleted successfully")
    raise HTTPException(status_code=404, detail=f"There is no student with the id = {student_id}")