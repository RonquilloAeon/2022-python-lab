import aioredis
import ulid
from pydantic import BaseModel
from xpresso import App, Depends, Path, FromJson, FromPath
from xpresso.typing import Annotated


class CreateDocumentDto(BaseModel):
    name: str
    data: dict = None


class Document(BaseModel):
    id: str
    name: str
    data: dict = None


async def get_cache() -> aioredis.Redis:
    return await aioredis.from_url("redis://redis:6379")


async def create_document(
    document: FromJson[CreateDocumentDto],
    cache: Annotated[aioredis.Redis, Depends(get_cache)],
) -> Document:
    return Document(id=ulid.new().str.lower(), name=document.name, data=document.data)


async def read_document(document_id: FromPath[int]) -> Document:
    return Document(id=document_id, name="Something")


app = App(
    routes=[
        Path("/documents", post=create_document),
        Path(
            "/documents/{document_id}",
            get=read_document,
        ),
    ]
)
