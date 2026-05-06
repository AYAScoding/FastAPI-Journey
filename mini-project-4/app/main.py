from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from .database import polls
from .models import PollCreate, VoteRequest
from .manager import manager

app = FastAPI()

# --- REST API ENDPOINTS ---

@app.post("/polls")
async def create_poll(poll: PollCreate):
    poll_id = str(len(polls) + 1)
    polls[poll_id] = {
        "id": poll_id,
        "question": poll.question,
        "options": {opt: 0 for opt in poll.options}
    }
    return polls[poll_id]

@app.get("/polls")
async def list_polls():
    return list(polls.values())

@app.get("/polls/{poll_id}")
async def get_poll(poll_id: str):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found")
    return polls[poll_id]

@app.post("/polls/{poll_id}/vote")
async def vote_rest(poll_id: str, vote: VoteRequest):
    if poll_id not in polls or vote.option not in polls[poll_id]["options"]:
        raise HTTPException(status_code=400, detail="Invalid poll or option")
    
    polls[poll_id]["options"][vote.option] += 1
    
    # Crucial: Broadcast update even if vote comes via REST!
    await manager.broadcast(poll_id, {
        "event": "update",
        "poll_id": poll_id,
        "options": polls[poll_id]["options"]
    })
    return {"message": "Vote counted", "results": polls[poll_id]["options"]}

@app.delete("/polls/{poll_id}")
async def delete_poll(poll_id: str):
    if poll_id in polls:
        del polls[poll_id]
        return {"message": "Poll deleted"}
    raise HTTPException(status_code=404, detail="Poll not found")

# --- WEBSOCKET ENDPOINT ---

@app.websocket("/ws/polls/{poll_id}")
async def websocket_endpoint(websocket: WebSocket, poll_id: str):
    if poll_id not in polls:
        await websocket.close(code=1008)
        return

    await manager.connect(poll_id, websocket)
    try:
        while True:
            # Receive data from a client
            data = await websocket.receive_json()
            option = data.get("option")

            if option in polls[poll_id]["options"]:
                polls[poll_id]["options"][option] += 1
                
                # Broadcast the NEW state to ALL clients watching this poll
                await manager.broadcast(poll_id, {
                    "event": "update",
                    "poll_id": poll_id,
                    "options": polls[poll_id]["options"]
                })
    except WebSocketDisconnect:
        manager.disconnect(poll_id, websocket)