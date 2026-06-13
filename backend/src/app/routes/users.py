from fastapi import APIRouter, Depends
from ..schemas import UserRegister, UserLogin, UserResponse
from ..dependencies import get_user_id
from ..crud import users as u

router = APIRouter()

# register a user
@router.post('/register')
async def register(user: UserRegister) -> dict:
  return u.register(user.username, user.email, user.password)

@router.post('/login')
async def login(user: UserLogin) -> dict:
  return u.login(user.email, user.password)

@router.get('/user/me')
async def get_current_user_details(user_id: int = Depends(get_user_id)) -> UserResponse:
  return u.get_current_user_details(user_id)

@router.get('/users/{user_id}')
async def get_user(user_id: int) -> dict:
  return u.get_user_details(user_id)