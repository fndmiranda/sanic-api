from abc import ABC
from core import marshal


class BaseResource(ABC):
    """Class representing the abstract base resource."""

    _fields = None

    def make(self, data, envelope=None):
        return marshal(data, self.get_fields(), envelope)

    def collection(self, data, envelope=None):
        if 'data' in data:
            return self.__paginate(data)

        collection = [self.make(i) for i in data]
        return {envelope: collection} if envelope else collection

    def get_fields(self):
        """Get the fields."""
        if self._fields is None:
            raise ValueError('Fields is required, set _fields')
        return self._fields

    def __paginate(self, data):
        """Prepare dict to return with paginate attributes."""
        data.update({
            'data': [self.make(i) for i in data['data']]
        })
        return data
