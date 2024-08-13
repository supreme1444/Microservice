import uuid

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import async_session, AsyncSession
from api.models import UserCreate,ShowUser
from db.dals import UserDAL
from db.session import get_db


user_router = APIRouter()

async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
            )
            return ShowUser(
                users_id=user.users_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )

@user_router.post("/",response_model=ShowUser)
async def create_user(body:UserCreate,db:AsyncSession=Depends(get_db))->ShowUser:
    return await _create_new_user(body,db)

async def _delete_user(user_id: uuid.UUID, db: AsyncSession) -> None:
    async with db as async_session:
        async with async_session.begin():
            user_dal = UserDAL(async_session)
            await user_dal.delete_user(user_id)
            return ("User delete")
@user_router.delete("/{user_id}")
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    await _delete_user(user_id, db)
    return {"message": "User deleted successfully"}
async def _update_user(users_id: uuid.UUID, new_name: str, new_surname: str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.update_user(
                users_id=users_id,
                new_name=new_name,
                new_surname=new_surname,
            )
            if not user:
                raise ValueError(f"User with id {users_id} not found or could not be updated")
            return ShowUser(
                users_id=user.users_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )


@user_router.put("/{user_id}", response_model=ShowUser)
async def update_user_endpoint(user_id: uuid.UUID, new_name: str, new_surname: str, db: AsyncSession = Depends(get_db)):
    user_service = UserDAL(db)
    updated_user = await user_service.update_user(user_id, new_name, new_surname)
    return updated_user

