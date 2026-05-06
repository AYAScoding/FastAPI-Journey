from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .database import polls
from .models import PollCreate, VoteRequest
from .manager import manager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    # 1. Accept and add to manager
    await manager.connect(poll_id, websocket)
    
    # 2. Check if the poll exists
    if poll_id not in polls:
        await websocket.send_json({"error": "Poll not found"})
        await websocket.close()
        manager.disconnect(poll_id, websocket)
        return

    # 3. Send the current state immediately so buttons appear
    await websocket.send_json({
        "event": "initial_state",
        "poll_id": poll_id,
        "question": polls[poll_id]["question"],
        "options": polls[poll_id]["options"]
    })
    
    try:
        while True:
            data = await websocket.receive_json()
            option = data.get("option")

            if option in polls[poll_id]["options"]:
                polls[poll_id]["options"][option] += 1
                
                # Broadcast updates to all clients on this poll
                await manager.broadcast(poll_id, {
                    "event": "update",
                    "poll_id": poll_id,
                    "options": polls[poll_id]["options"]
                })
    except WebSocketDisconnect:
        manager.disconnect(poll_id, websocket)