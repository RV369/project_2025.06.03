import uuid

from sqlalchemy import UUID, String, select, Text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


sqlite_database = 'sqlite+aiosqlite:///db.sqlite3'

engine = create_async_engine(sqlite_database, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


def get_session_local():
    yield SessionLocal()


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
        unique=True,
    )


class Post(Base):
    __tablename__ = 'posts'
    category: Mapped[str] = mapped_column(String(100), unique=False)
    content: Mapped[str] = mapped_column(Text)


class CountContent(Base):
    __tablename__ = 'countcontent'
    content_str: Mapped[str] = mapped_column(String(100), unique=False)
    count: Mapped[int] = mapped_column()


class Repozitory:

    @classmethod
    async def get_category(self, model, **kwargs):
        async with SessionLocal() as session:
            rez = await session.execute(select(model).filter_by(**kwargs))
            instance = rez.scalars().all()
            return instance

    @classmethod
    async def get_posts_content(self, model, **kwargs):
        async with SessionLocal() as session:
            search = '%{}%'.format(*kwargs.values())
            rez = await session.execute(
                select(model).filter(model.content.ilike(search)),
            )
            instance = rez.scalars().all()
            return instance

    @classmethod
    async def create(self, model, **kwargs):
        async with SessionLocal() as session:
            instance = model(**kwargs)
            session.add(instance)
            await session.flush()
            await session.commit()
            return instance

    @classmethod
    async def update_or_create(cls, model, **kwargs):
        async with SessionLocal() as session:
            rez = await session.execute(
                select(model).filter_by(content_str=kwargs['content_str']),
            )
            instance = rez.scalars().first()
            if instance:
                instance.count = kwargs['count']
                session.add(instance)
                await session.flush()
                await session.commit()
                return instance
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
