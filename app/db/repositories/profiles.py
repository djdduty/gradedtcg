from typing import Union

from asyncpg import Connection

from app.db.repositories.base import BaseRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.profiles import Profile
from app.models.domain.users import User

UsersLike = Union[User, Profile]


class ProfilesRepository(BaseRepository):
    def __init__(self, conn: Connection):
        super().__init__(conn)
        self._users_repo = UsersRepository(conn)

    async def get_profile_by_username(
        self,
        *,
        username: str,
    ) -> Profile:
        user = await self._users_repo.get_user_by_username(username=username)

        return Profile(username=user.username, bio=user.bio, image=user.image)
