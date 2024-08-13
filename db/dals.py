import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.models import ShowUser
from db.models import User




class UserDAL:
    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    async def create_user(
        self, name: str, surname: str, email: str
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self,users_id: uuid.UUID):
        result = await self.db_session.execute(
            select(User).filter(User.users_id == users_id)
        )
        user = result.scalars().first()
        if user:
            await self.db_session.delete(user)
            await self.db_session.commit()
        else:
            raise HTTPException(status_code=404, detail="User not found")
    async def update_user(self, users_id: uuid.UUID, new_name: str, new_surname: str) -> ShowUser:
        result = await self.db_session.execute(
            select(User).filter(User.users_id == users_id)
        )
        user = result.scalars().first()

        if user:
            user.name = new_name
            user.surname = new_surname
            await self.db_session.commit()


            return ShowUser(
                users_id=user.users_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")