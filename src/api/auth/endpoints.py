from fastapi import APIRouter, Body
from fastapi.params import Depends

from schemas.pydantic.user import UserCreate
from database.session import get_async_session
from utils.password import hash_password, verify_password
from repositories.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User

auth_routers = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_routers.post("/register")
async def register(user: UserCreate = Body(), session: AsyncSession=Depends(get_async_session)):
    user.password = hash_password(user.password)
    user_session = UserRepository(session)
    result = await user_session.create(user)
    print(result)
# ^Test