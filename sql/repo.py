from abc import abstractmethod
from typing import Optional
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from sql.models import User


class Repo:

    @abstractmethod
    async def create(self):
        pass

    @abstractmethod
    async def get(slef):
        pass

    @abstractmethod
    async def update(self):
        pass

    @abstractmethod
    async def delete(slef):
        pass


class UserRepo(Repo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, fullname: str) -> User:
        user = User(id=user_id, fullname=fullname)
        check = await self.get(user_id=user_id)
        if not check:
            self.session.add(user)
            await self.session.commit()
        return user

    async def get(self, user_id: int) -> Optional[User]:
        return await self.session.get(User, user_id)

    async def update(self, user_id: int, chat_id: str) -> None:
        stmt = update(User).where(User.id == user_id).values(chat_id=chat_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, user_id: int) -> None:
        stmt = delete(User).where(User.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
