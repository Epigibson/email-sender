from models.user_model import User
from schemas.user_schema import UserCreate
from core.security import get_current_user, get_password_hash

class UserService:
    
    @staticmethod
    async def get_users():
        return await User.find_all().to_list()


    @staticmethod
    async def get_current_user_logged():
        return await get_current_user()


    @staticmethod
    async def get_user_by_username(username: str):
        return await User.find_one(User.username == username)

    
    @staticmethod
    async def get_user_by_email(email: str):
        return await User.find_one(User.email == email)


    @staticmethod
    async def get_user_by_id(id: str):
        return await User.find_one(User.id == id)

    
    @staticmethod
    async def create_user(user_data: UserCreate):
        hash_password = get_password_hash(user_data.hashed_password)
        new_user = User(**user_data.model_dump(exclude_none=True), password=hash_password)
        await new_user.insert()
        return new_user

    
    @staticmethod
    async def update_user(user: User):
        user = await UserService.get_user_by_id(user.id)
        await user.update({ "$set": user.model_dump(exclude_unset=True)})
        return user

    
    @staticmethod
    async def delete_user(user: User):
        user = await UserService.get_user_by_id(user.id)
        return await user.delete()