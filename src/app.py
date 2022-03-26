import aioredis
from xpresso import App, Depends, Path, FromPath
from xpresso import exceptions
from xpresso.typing import Annotated

from .functions import FromMsgPack
from .models import CreateDocumentDto, Document
from .responses import MsgPackResponse
from .services import find_document, save_document


async def get_cache() -> aioredis.Redis:
    return await aioredis.from_url("redis://localhost:6379")


Cache = Annotated[aioredis.Redis, Depends(get_cache)]


async def create_document(
    document: FromMsgPack[CreateDocumentDto],
    cache: Cache,
) -> MsgPackResponse:
    id = await save_document(document, cache)
    return MsgPackResponse({"status": "ok", "id": id})


async def read_document(document_id: FromPath[str], cache: Cache) -> MsgPackResponse:
    try:
        document = await find_document(document_id, cache)
        return MsgPackResponse(document.dict())
    except RuntimeError as e:
        raise exceptions.HTTPException(status_code=404, detail=str(e))


app = App(
    routes=[
        Path("/documents", post=create_document),
        Path(
            "/documents/{document_id}",
            get=read_document,
        ),
    ]
)
