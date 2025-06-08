import uuid

from pydantic import BaseModel


class TagSchema(BaseModel):
    name: str


class PostSchema(BaseModel):
    id: uuid.UUID
    category: str
    content: str
    tags: list[TagSchema]


class FindCategorySchema(BaseModel):
    category: str


class FindContentSchema(BaseModel):
    content: str


class PostCreateSchema(BaseModel):
    category: str
    content: str
    tags: list[str]
