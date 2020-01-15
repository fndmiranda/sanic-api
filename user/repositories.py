from user.models import User
from core.repositories import BaseRepository


class UserRepository(BaseRepository):
    """Class representing the product repository."""

    _model = User
