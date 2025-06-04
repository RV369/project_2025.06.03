import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


from src.db import Repozitory
from src.db import Post, CountContent
from src.core import count_str


async def lifespan(app):
    await Repozitory.create_tables()
    yield


app = FastAPI(lifespan=lifespan)


class PostSchema(BaseModel):
    id: uuid.UUID
    category: str
    content: str


class FindCategorySchema(BaseModel):
    category: str


class FindContentSchema(BaseModel):
    content: str


class PostCreateSchema(BaseModel):
    category: str
    content: str


@app.post('/find_category/', response_model=list[PostSchema])
async def get_post_find_category(
    data: FindCategorySchema,
    skip: int = 0,
    limit: int = 10,
):
    kwargs = {
        'category': data.category,
    }
    posts = await Repozitory.get_category(Post, **kwargs)
    if posts:
        return [
            PostSchema(id=t.id, category=t.category, content=t.content)
            for t in posts
        ][skip: skip + limit]
    else:
        raise HTTPException(
            status_code=404,
            detail='Искомая публикация отсутствует',
        )


@app.post('/find_content/', response_model=list[PostSchema])
async def get_post_find_content(
    data: FindContentSchema,
    skip: int = 0,
    limit: int = 10,
):
    kwargs = {
        'content': data.content,
    }
    posts = await Repozitory.get_posts_content(Post, **kwargs)
    count_content = count_str(data.content, posts)
    kwargs = {
        'content_str': data.content,
        'count': count_content,
    }
    await Repozitory.create(CountContent, **kwargs)
    if posts:
        return [
            PostSchema(id=t.id, category=t.category, content=t.content)
            for t in posts
        ][skip: skip + limit]
    else:
        raise HTTPException(
            status_code=404,
            detail='Искомая публикация отсутствует',
        )


@app.post('/create/', response_model=PostSchema)
async def post_create(
    data: PostCreateSchema,
):
    kwargs = {'category': data.category, 'content': data.content}
    post = await Repozitory.create(Post, **kwargs)
    return post
