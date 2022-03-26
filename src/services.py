import aioredis
import msgpack
import ulid

from .models import CreateDocumentDto, Document


async def find_document(id: str, cache: aioredis.Redis) -> Document:
    data = await cache.get(ulid.from_str(id).bytes)

    if not data:
        raise RuntimeError(f"Document with id {id} not found.")

    return Document(id=id, **msgpack.unpackb(data))


async def save_document(
    document: CreateDocumentDto, cache: aioredis.Redis, id: str = None
) -> str:
    if not id:
        id = ulid.new()

    await cache.set(id.bytes, msgpack.packb(document.dict()))

    return str(id).lower()
