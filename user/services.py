from user.repositories import UserRepository
from core.services import BaseService
import crypt


class UserService(BaseService):
    """Class representing the product service."""

    _repository = UserRepository

    async def update(self, pk, payload):
        """Update a register."""
        return await self.get_repository().update(pk, await self._prepare(payload))

    async def create(self, payload):
        """Save a new register."""
        return await self.get_repository().create(await self._prepare(payload))

    @staticmethod
    async def _prepare(payload):
        """Prepare payload to save."""
        if 'password' in payload:
            payload['password'] = crypt.crypt(payload['password'])
        return payload
