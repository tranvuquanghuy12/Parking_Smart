from fastapi import APIRouter
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    user_dict = user.dict()
    result = await UserService.create_user(user_dict)
    return result

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: str):
    return await UserService.get_user(id)

@router.get("/", response_model=list[UserResponse])
async def get_all():
    return await UserService.get_all_users()

