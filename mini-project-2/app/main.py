from fastapi import FastAPI
from database.connection import initialize_database
from routes.events import event_router
from routes.users import user_router
import uvicorn

app = FastAPI()

# Register the routes from Phase 4
app.include_router(event_router, prefix="/event", tags=["Events"])
app.include_router(user_router, prefix="/user", tags=["Users"])

@app.on_event("startup")
async def start_db():
    """
    This is Requirement 5: initialize the database 
    connection when the application starts.
    """
    await initialize_database()

@app.get("/")
async def root():
    return {"message": "Welcome to the Event Planner API!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)