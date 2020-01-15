from abc import ABC
from sanic.exceptions import abort


class BaseService(ABC):
    """Class representing the abstract base service."""

    _repository = None

    async def paginate(self, expressions=None, options={}):
        """Retrieve all data by filters paginated."""
        return await self.get_repository().paginate(expressions, options)

    async def find(self, pk):
        """Get one data by pk."""
        return await self.get_repository().find(pk)

    async def find_or_404(self, pk):
        """Get one data by pk or abort with http status code 404."""
        return await self.find(pk) or abort(404)

    async def get(self, expressions=None):
        """Retrieve all data by filters."""
        return await self.get_repository().get(expressions)

    async def create(self, payload):
        """Save a new register."""
        return await self.get_repository().create(payload)

    async def update(self, pk, payload):
        """Update a register."""
        return await self.get_repository().update(pk, payload)

    async def update_or_404(self, pk, payload):
        """Get one data to update by pk or abort with http status code 404."""
        model = await self.find_or_404(pk)
        return await self.get_repository().update(model, payload)

    async def delete(self, pk):
        """Delete one data by pk."""
        return await self.get_repository().delete(pk)

    async def delete_or_404(self, pk):
        """Get one data to delete by pk or abort with http status code 404."""
        model = await self.find_or_404(pk)
        return await self.get_repository().delete(model)

    def get_repository(self):
        """Get repository."""
        if self._repository is None:
            raise ValueError('Repository is required, set _repository')
        return self._repository

    def get_model(self):
        """Get the model."""
        return self.get_repository().get_model()
