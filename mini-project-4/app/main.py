from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

polls: Dict[str, dict] = {}

class PollCreate(BaseModel):
    question: str
    options: List[str]

@app.post("/polls")
async def create_poll(poll: PollCreate):
    poll_id = str(len(polls) + 1)
    polls[poll_id] = {
        "question": poll.question, 
        "options": {opt: 0 for opt in poll.options}
    }
    return {"id": poll_id, **polls[poll_id]}

@app.get("/polls")
async def list_polls():
    return polls

@app.get("/polls/{poll_id}")
async def get_poll(poll_id: str):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found")
    return polls[poll_id]

@app.post("/polls/{poll_id}/vote")
async def vote_rest(poll_id: str, option: str):
    if poll_id not in polls or option not in polls[poll_id]["options"]:
        raise HTTPException(status_code=400, detail="Invalid poll or option")
    polls[poll_id]["options"][option] += 1
    # Note: In Task 2, you'll need to trigger a broadcast here too!
    return {"message": "Vote counted", "data": polls[poll_id]}