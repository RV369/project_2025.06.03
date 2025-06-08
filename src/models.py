import uuid
from typing import List

from sqlalchemy import UUID, Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
        unique=True,
    )


tags_post = Table(
    'tags_post',
    Base.metadata,
    Column('tag_id', UUID, ForeignKey('tag.id')),
    Column('posts_id', UUID, ForeignKey('posts.id')),
)


class Tag(Base):
    __tablename__ = 'tag'
    name: Mapped[str] = mapped_column(String(100), unique=True)

    def __str__(self):
        return self.name


class Post(Base):
    __tablename__ = 'posts'
    category: Mapped[str] = mapped_column(String(100), unique=False)
    content: Mapped[str] = mapped_column(Text)
    tags: Mapped[List[Tag]] = relationship(
        Tag,
        secondary=tags_post,
        lazy='joined',
    )

    def __str__(self):
        return self.category


class CountContent(Base):
    __tablename__ = 'countcontent'
    content_str: Mapped[str] = mapped_column(String(100), unique=False)
    count: Mapped[int] = mapped_column()

    def __str__(self):
        return self.content_str, self.count
