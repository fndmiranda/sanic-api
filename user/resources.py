from core.fields import String, Integer, DateTime
from core.resources import BaseResource


class User(BaseResource):
    _fields = {
        'id': Integer,
        'name': String,
        'email': String,
        'created_at': DateTime,
        'updated_at': DateTime,
    }
