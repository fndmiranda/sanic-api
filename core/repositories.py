import urllib.parse
import math
from abc import ABC
from core.database import Session
import aiotask_context as context


class BaseRepository(ABC):
    """Class representing the abstract base repository."""

    _session = Session()
    _model = None

    @classmethod
    async def paginate(cls, expressions=None, options={}):
        """Retrieve all data by expressions paginated."""

        response = {
            'data': await cls._prepare(expressions=expressions, options=options, paginate=True),
            'meta': {
                'current_page': cls._page,
                'per_page': cls._limit,
                'total': cls._count,
            },
            'links': {
                'first': await cls._get_url(1),
                'last': await cls._get_url(cls._page_count),
                'prev': (
                    await cls._get_url(cls._page - 1)
                    if await cls._validate_page(cls._page - 1) else None
                ),
                'next': (
                    await cls._get_url(cls._page + 1)
                    if await cls._validate_page(cls._page + 1) else None
                ),
            },
        }

        return response

    @classmethod
    async def get(cls, expressions=None, options={}):
        """Retrieve all data by expressions."""
        return await cls._prepare(expressions=expressions, options=options)

    @classmethod
    async def find(cls, pk):
        """Retrieve one data by pk."""
        data = cls._session.query(cls.get_model()).get(pk)
        cls._session.commit()
        return data

    @classmethod
    async def count(cls, expressions=None):
        """Count the number of registers by expressions."""
        query = cls._session.query(cls.get_model())

        if expressions is not None:
            query = query.filter(expressions)

        cls._session.commit()

        return query.count()

    @classmethod
    async def update(cls, pk_or_model, payload={}):
        """Update a register by pk or model."""
        data = pk_or_model if isinstance(pk_or_model, cls.get_model()) else await cls.find(pk_or_model)

        for column, value in payload.items():
            if hasattr(data, column):
                setattr(data, column, value)

        cls._session.commit()

        return data

    @classmethod
    async def create(cls, payload):
        """Save a new register."""
        data = await cls.__populate(**payload)

        cls._session.add(data)
        cls._session.commit()

        return data

    @classmethod
    async def delete(cls, pk_or_model):
        """Delete a register by pk or model."""
        data = pk_or_model if isinstance(pk_or_model, cls.get_model()) else await cls.find(pk_or_model)

        cls._session.delete(data)
        cls._session.commit()

        print('data_delete', data)

        return data

    @classmethod
    def get_model(cls):
        """Get the model."""
        if cls._model is None:
            raise ValueError('Model is required, set _model')
        return cls._model

    @classmethod
    async def _prepare(cls, expressions=None, options={}, paginate=False):
        cls._page = await cls._get_page(options)
        cls._limit = await cls._get_limit(options)
        cls._count = await cls.count(expressions)
        cls._page_count = int(math.ceil(cls._count / cls._limit))

        query = cls._session.query(cls.get_model()).limit(cls._limit)

        if paginate:
            query = query.offset(cls._limit * (cls._page - 1))

        if expressions is not None:
            query = query.filter(expressions)

        return query.all()

    @classmethod
    async def __populate(cls, **kwargs):
        """Get the model."""
        if cls._model is None:
            raise ValueError('Model is required, set _model')
        return cls._model(**kwargs)

    @classmethod
    async def _get_page(cls, options={}):
        """Get current page."""
        request = context.get('request')

        page = options.get('page') if 'page' in options else int(request.args.get('page', 1))
        return page if page > 0 else 1

    @classmethod
    async def _get_limit(cls, options={}):
        """Get retrieve limit of registers."""
        request = context.get('request')

        limit = options.get('limit') if 'limit' in options else int(
            request.args.get('limit', cls.get_model().get_default_limit())
        )
        return limit if limit <= cls.get_model().get_max_limit() else cls.get_model().get_max_limit()

    @classmethod
    async def _validate_page(cls, page):
        if cls._count > 0:
            if page > cls._page_count or page < 1:
                return None
            return page
        return False

    @classmethod
    async def _get_url(cls, page):
        """"Get current URL with page query string."""
        request = context.get('request')
        url_parts = list(urllib.parse.urlparse(request.url))
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        query.update({'page': page})
        url_parts[4] = urllib.parse.urlencode(query)

        return urllib.parse.urlunparse(url_parts)
