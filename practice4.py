from fastapi import FastAPI, Request

# Initialize the FastAPI app
app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]


# TODO: Create a GET endpoint to retrieve a specific crew member by ID
# - The endpoint path should be "/members/{crew_id}"
# - The function should be async and named 'read_crew_member'
# - If the crew member is found, return their details in JSON format
# - If not found, return a message indicating the crew member was not found


# TODO: Create a POST endpoint to add a new crew member
# - The endpoint path should be "/members/"
# - The function should be async and named 'add_crew_member'
# - Parse the incoming request to get 'name' and 'role'
# - Create a new crew member with a unique ID and add it to the crew list
# - Return the details of the new crew member


# TODO: Create a PUT endpoint to update an existing crew member's details
# - The endpoint path should be "/members/{crew_id}"
# - The function should be async and named 'update_crew_member'
# - Parse the incoming request to get updated 'name' and 'role'
# - If the crew member is found, update their details
# - If not found, return a message indicating the crew member was not found


# TODO: Create a DELETE endpoint to remove a crew member by ID
# - The endpoint path should be "/members/{crew_id}"
# - The function should be async and named 'delete_crew_member'
# - If the crew member is found, remove them from the crew list
# - If not found, return a message indicating the crew member was not found