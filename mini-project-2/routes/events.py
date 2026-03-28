from fastapi import APIRouter, HTTPException, status
from typing import List
from beanie import PydanticObjectId
from database.connection import Database
from models.events import Event, EventUpdate

event_router = APIRouter()
event_database = Database(Event)

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events():
    return await event_database.get_all()

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId):
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

@event_router.post("/new")
async def create_event(body: Event):
    await event_database.save(body)
    return {"message": "Event created successfully"}

@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate):
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return updated_event

@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId):
    deleted = await event_database.delete(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return {"message": "Event deleted successfully"}