import inspect
import sys
from typing import Any, NamedTuple, Type

if sys.version_info < (3, 8):
    from typing_extensions import get_args
else:
    from typing import get_args

import msgpack
from pydantic import BaseModel

from xpresso import Request
from xpresso.binders.api import SupportsExtractor
from xpresso.requests import HTTPConnection


class Extractor(NamedTuple):
    model: Type[BaseModel]

    async def extract(self, connection: HTTPConnection) -> Any:
        assert isinstance(connection, Request)
        data = await connection.body()
        deserialized_obj: Any = msgpack.unpackb(data)
        # TODO validation
        return self.model.parse_obj(deserialized_obj)


class ExtractorMarker:
    def register_parameter(self, param: inspect.Parameter) -> SupportsExtractor:
        model = next(iter(get_args(param.annotation)))
        if not issubclass(model, BaseModel):
            raise TypeError("MessagePack model must be a Pydantic model")
        return Extractor(model)
