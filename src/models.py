from pydantic import BaseModel


class CreateDocumentDto(BaseModel):
    name: str
    data: dict = None


class Document(BaseModel):
    id: str
    name: str
    data: dict = None
