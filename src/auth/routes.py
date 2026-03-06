from fastapi import APIRouter , Depends, HTTPException , status
from src.auth.schemas import UserCreateModel , UserModel
from src.auth.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

auth_router = APIRouter()

@auth_router.post("/signup",response_model=UserModel)
async def create_user_account(user_data:UserCreateModel,session:AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exits = await UserService(session=session).user_exits(email=email)

    if user_exits == True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user alredy exits")
    new_user  = await UserService(session).create_user(user_data)
    return new_user 