import os
import datetime
import atexit
from typing import List
from sqlalchemy import create_engine, DateTime, String, func, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

POSTGRES_USER=os.getenv("POSTGRES_USER", "app")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_DB=os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST=os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT=os.getenv("POSTGRES_PORT", "5431")

PG_DSN=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    children: Mapped[List["Ad"]] = relationship(back_populates="parent")

class Ad(Base):
    __tablename__ = "ad"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    parent: Mapped["User"] = relationship(back_populates="children")


Base.metadata.create_all(bind=engine)

atexit.register(engine.dispose)