from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.models import User
from src.auth.schemas import UserCreateModel
from src.auth.utils import verify_password, generate_password_hash

class UserService():
    def __init__(self,session:AsyncSession):
        self.session = session

    async def get_user_by_email(self,email:str):
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return user
    
    async def user_exits(self,email:str)->bool:
        user = await self.get_user_by_email(email)
        if user is None:
            return False
        else:
            return True
    
    async def create_user(self,user_data:UserCreateModel):
        user_data_dict  = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(user_data_dict["password"])
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user