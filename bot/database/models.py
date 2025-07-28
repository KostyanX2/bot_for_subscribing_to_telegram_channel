from sqlalchemy import Column, DateTime, BigInteger,Boolean,String
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username:Mapped[str] = mapped_column(String(100), nullable=True, default=None)
    user_id:Mapped[int] = mapped_column(BigInteger)
    payment = Column(Boolean, default=False)
    time:Mapped[DateTime] = mapped_column(DateTime)

    def __repr__(self):
        return f"({self.id},'{self.username}', {self.user_id}, {self.payment}, {self.time})"
