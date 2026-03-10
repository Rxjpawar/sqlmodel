from fastapi import APIRouter , Depends, HTTPException , status
from src.auth.schemas import UserCreateModel , UserModel, UserLoginModel
from src.auth.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.utils import create_access_token , decode_token
from datetime import timedelta
from fastapi.responses import JSONResponse
from src.auth.utils import verify_password
from src.auth.dependencies import RefreshTokenBearer
from src.auth.dependencies import AccessTokenBearer
from src.db.redis import add_jti_to_blocklist
from datetime import datetime

auth_router = APIRouter()
refresh_token_bearer= RefreshTokenBearer()
access_token_bearer=AccessTokenBearer()
REFRESH_TOKEN_EXPIRY = 2

@auth_router.post("/signup",response_model=UserModel)
async def create_user_account(user_data:UserCreateModel,session:AsyncSession = Depends(get_session),):
    email = user_data.email
    user_exits = await UserService(session=session).user_exits(email=email)

    if user_exits == True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user alredy exits")
    new_user  = await UserService(session).create_user(user_data)
    return new_user 

@auth_router.post("/login")
async def login_users(login_data:UserLoginModel,session:AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await UserService(session).get_user_by_email(email)

    if user is not None:
        password_valid = verify_password(password,user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email":user.email,
                    "user_uid":str(user.uid)

                })
            refresh_token = create_access_token(
                user_data={
                    "email":user.email,
                    "user_uid":str(user.uid)

                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY))
            return JSONResponse(
                content={
                    "message":"login successsfull",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "uid":str(user.uid)

                    }
                }
            )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid email or password")
    
@auth_router.get("/refresh_token")
async def get_new_access_token(token_details:dict=Depends(refresh_token_bearer)):
    expiry_timestamp= token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp)>datetime.now():
        new_access_token = create_access_token(
            user_data=token_details["user"]
        )
        return JSONResponse(content={
            "access_token":new_access_token
        })
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid or expire token")

@auth_router.get("/logout")
async def revoke_token(token_details:dict= Depends(access_token_bearer)):
    jti=token_details["jti"]
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={"message":"logged out successfully"},status_code=status.HTTP_200_OK
    )
