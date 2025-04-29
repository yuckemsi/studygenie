from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url="sqlite+aiosqlite:///data.db")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase): ...

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(), nullable=True)
    first_name: Mapped[str] = mapped_column(String(), nullable=True)
    last_name: Mapped[str] = mapped_column(String(), nullable=True)
    tokens: Mapped[int] = mapped_column(default=0)
    level: Mapped[int] = mapped_column(default=0)  # Уровень пользователя1
    model: Mapped[str] = mapped_column(String(), nullable=True, default="openai/gpt-4.1")


    referrals = relationship("Referral", back_populates="user", foreign_keys="Referral.tg_id")
    rating = relationship("Rating", back_populates="user", uselist=False)

class Referral(Base):
    __tablename__ = "referrals"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(ForeignKey("users.tg_id"))
    refferal_id = mapped_column(ForeignKey("users.tg_id"))
    
    user = relationship("User", back_populates="referrals", foreign_keys=[tg_id])

class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(ForeignKey("users.tg_id"))
    username: Mapped[str] = mapped_column(ForeignKey("users.username"), nullable=True)
    first_name: Mapped[str] = mapped_column(ForeignKey("users.first_name"), nullable=True)
    last_name: Mapped[str] = mapped_column(ForeignKey("users.last_name"), nullable=True)

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[int] = mapped_column()  # Уровень сложности вопроса
    question: Mapped[str] = mapped_column(String(), nullable=False)  # Текст вопроса
    answer: Mapped[str] = mapped_column(String(), nullable=False)  # Ответ на вопрос
    subject: Mapped[str] = mapped_column(String(), nullable=False)  # Предмет (математика, история и т.д.)

class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(ForeignKey("users.tg_id"))
    points: Mapped[int] = mapped_column(default=0)  # Очки рейтинга

    user = relationship("User", back_populates="rating", foreign_keys=[tg_id])