import typing

import msgpack
from starlette.background import BackgroundTask
from xpresso.responses import Response


class MsgPackResponse(Response):
    media_type = "application/x-msgpack"

    def __init__(
        self,
        content: typing.Any,
        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: typing.Any) -> bytes:
        return msgpack.packb(content)
