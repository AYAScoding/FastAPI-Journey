from fastapi import FastAPI, Request
from models import Student , Enrolement
import asyncio

app = FastAPI()

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
   
@app.get("/students/")
async def list_students(request: Request):
    await asyncio.sleep(1)
    return Students_database


@app.get("/students/{student_id}")
def get_student_by_id(request, student_id:int):
    for student in Students_database:
        if student["student_id"] == student_id:
            return student
    return {"Message": "student not Found"}

@app.post("/students/")
def add_student(student:Student):

    student_id = max((s["student_id"] for s in Students_database)) + 1 if Students_database else 1
    new_std = {"student_id":student_id,**student}
    Students_database.append(new_std)

    return {"message": "new student added successfully"}

@app.put("/students/{student_id}")
async def update_student(request:Request, student_id:int):
    data = await request.json()
    enrolements = data["enrolements"]
    for std in Students_database:
        if std["student_id"] == student_id:
            std["enrolements"] = enrolements
    return {"Message": " student updated successfully"}

@app.delete("/students/{student_id}")
async def delete_student(request:Request, student_id:int):
    for std in Students_database:
        if std["student_id"] == student_id:
            Students_database.remove(std)
            return {"Message": "Student deleted successfully"}
        return {"Message": "No student with this id"}
    









