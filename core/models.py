from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr


class ModelMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    _default_limit = 25
    _max_limit = 100

    id = Column(Integer, primary_key=True)

    @classmethod
    def get_default_limit(cls, options={}):
        """Get retrieve limit of registers."""
        limit = int(options.get('limit', cls._default_limit))
        return limit if limit <= cls._max_limit else cls._max_limit

    @classmethod
    def get_max_limit(cls):
        """Get max retrieve limit of registers."""
        return cls._max_limit
