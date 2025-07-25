from sqlalchemy import Column, DateTime, BigInteger,Boolean,String
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username:Mapped[str] = mapped_column(String(100), nullable=False)
    user_id:Mapped[int] = mapped_column(BigInteger)
    payment = Column(Boolean, default=False)
    time:Mapped[DateTime] = mapped_column(DateTime)


