from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.models import Base

sqlite_database = 'sqlite+aiosqlite:///db/db.sqlite3'

engine = create_async_engine(sqlite_database, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


def get_session_local():
    yield SessionLocal()


class Repozitory:
    @classmethod
    async def get_category(self, model, **kwargs):
        async with SessionLocal() as session:
            rez = await session.execute(select(model).filter_by(**kwargs))
            instance = rez.unique().scalars().all()
            return instance

    @classmethod
    async def get_posts_content(self, model, **kwargs):
        async with SessionLocal() as session:
            search = '%{}%'.format(*kwargs.values())
            rez = await session.execute(
                select(model).filter(model.content.ilike(search)),
            )
            instance = rez.unique().scalars().all()
            return instance

    @classmethod
    async def update_or_create(self, model, **kwargs):
        async with SessionLocal() as session:
            rez = await session.execute(
                select(model).filter_by(content_str=kwargs['content_str']),
            )
            instance = rez.scalars().first()
            if instance:
                instance.count = kwargs['count']
            else:
                instance = model(**kwargs)
            session.add(instance)
            await session.flush()
            await session.commit()
            return instance

    @classmethod
    async def create_tables(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
