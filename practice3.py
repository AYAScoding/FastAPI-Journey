from fastapi import FastAPI

app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]

# TODO: Define the DELETE endpoint for removing a crew member at /delete_member/{crew_id}
# TODO: delete the crew member from the mock database and display the corresponding message 
