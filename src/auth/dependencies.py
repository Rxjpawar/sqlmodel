from fastapi.security import HTTPBearer
from fastapi import Request, status ,Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from src.auth.utils import decode_token
from src.db.redis import token_in_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.service import UserService
class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):

        creds: HTTPAuthorizationCredentials = await super().__call__(request)

        if creds is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authorization header missing")

        token = creds.credentials

        token_data = decode_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error":"this token is invalid or expired",
                    "resolution":"get a new token"
                })
        
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error":"this token is invalid or has been revoked",
                    "resolution":"get a new token"
                })

        
        self.verify_token_data(token_data)

        return token_data
    
    def token_valid(self,token:str)->bool:
        token_data = decode_token(token)
        return token_data is not None

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Please override this method in child classes")


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if not token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token"
            )
        
async def get_current_user(token_details:dict = Depends(AccessTokenBearer()),session:AsyncSession=Depends(get_session)):
    user_email = token_details["user"]["email"]
    user = await UserService(session).get_user_by_email(user_email)
    return user