

from fastapi import APIRouter, HTTPException, status, Security
from core.security import get_current_user
from schemas.user_schema import UserCreate
from services.user_services import UserService

router = APIRouter()


@router.post(path="/users", summary="Create a new user", description="Create a new user in the database.")
async def create_user(user: UserCreate):
    try:
        return await UserService.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    path="/", 
    summary="Get all users", 
    description="Get all users from the database.",
    dependencies=[Security(get_current_user, scopes=["users:read"])]
)
async def get_users():
    try:
        return await UserService.get_users()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    path="/current_user", 
    summary="Get current logged user", 
    description="Get current logged user from the database.",
    dependencies=[Security(get_current_user, scopes=["users:read"])]
)
async def get_current_user_logged():
    try:
        return await UserService.get_current_user_logged()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    path="/{user_id}", 
    summary="Get a user by ID", 
    description="Get a user by ID from the database.",
    dependencies=[Security(get_current_user, scopes=["users:read"])]
)
async def get_user_by_id(user_id: str):
    try:
        return await UserService.get_user_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    path="/{username}", 
    summary="Get a user by username", 
    description="Get a user by username from the database.",
    dependencies=[Security(get_current_user, scopes=["users:read"])]
)
async def get_user_by_username(username: str):
    try:
        return await UserService.get_user_by_username(username)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    path="/{email}", 
    summary="Get a user by email", 
    description="Get a user by email from the database.",
    dependencies=[Security(get_current_user, scopes=["users:read"])]
)
async def get_user_by_email(email: str):
    try:
        return await UserService.get_user_by_email(email)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    path="/{user_id}", 
    summary="Update a user by ID", 
    description="Update a user by ID in the database.",
    dependencies=[Security(get_current_user, scopes=["users:write"])]
)
async def update_user(user: UserCreate):
    try:
        return await UserService.update_user(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete( 
    path="/{user_id}", 
    summary="Delete a user by ID", 
    description="Delete a user by ID from the database.",
    dependencies=[Security(get_current_user, scopes=["users:write"])]
)
async def delete_user(user_id: str):
    try:
        return await UserService.delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
