from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core import count_str
from src.db import Repozitory, get_session_local
from src.models import CountContent, Post, Tag
from src.schemas import (
    FindCategorySchema,
    FindContentSchema,
    PostCreateSchema,
    PostSchema,
)


async def lifespan(app):
    await Repozitory.create_tables()
    yield


app = FastAPI(lifespan=lifespan)


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
        return [p for p in posts][skip: skip + limit]
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
    count_content = await count_str(data.content, posts)
    kwargs = {
        'content_str': data.content,
        'count': count_content,
    }
    await Repozitory.update_or_create(CountContent, **kwargs)
    if posts:
        return [p for p in posts][skip: skip + limit]
    else:
        raise HTTPException(
            status_code=404,
            detail='Искомая публикация отсутствует',
        )


@app.post('/create/', response_model=PostSchema)
async def post_create(
    data: PostCreateSchema,
    session: AsyncSession = Depends(get_session_local),
):
    kwargs = {'category': data.category, 'content': data.content, 'tags': []}
    for tag in data.tags:
        rez = await session.execute(select(Tag).filter_by(name=tag))
        instance = rez.scalars().first()
        if not instance:
            instance = Tag(name=tag)
        kwargs['tags'].append(instance)
        session.add(instance)
    post = Post(**kwargs)
    session.add(post)
    await session.flush()
    await session.commit()
    return post
