from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.users import User, UserSignIn

user_router = APIRouter()
user_database = Database(User)

@user_router.post("/signup")
async def sign_new_user(data: User):

    user_exist = await User.find_one(User.email == data.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email exists"
        )
    
    await user_database.save(data)
    return {"message": "User registered successfully"}

@user_router.post("/signin")
async def sign_user_in(user: UserSignIn):
    # Find user by email
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    
    
    if user_exist.password == user.password:
        return {"message": "User signed in successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid password"
    )