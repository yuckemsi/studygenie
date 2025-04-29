from app.database.models import async_session
from app.database.models import User, Referral, Admin, Question, Rating
from sqlalchemy import select, insert, update, delete, or_
from sqlalchemy.sql.expression import func

async def set_user(tg_id: int, username: str = None, first_name: str = None, last_name: str = None):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, username=username, first_name=first_name, last_name=last_name))
            await session.commit()

async def validate_ref(invited_id: int, referral_id: int):
    async with async_session() as session:
        check = await session.scalar(
            select(Referral).where(
                or_(
                    Referral.tg_id == invited_id,
                    Referral.refferal_id == referral_id,
                    Referral.refferal_id == invited_id
                )
            )
        )
        return check

async def add_ref(tg_id: int, refferal_id: int):
    async with async_session() as session:
        session.add(Referral(tg_id=tg_id, refferal_id=refferal_id))
        await session.commit()

async def add_tokens(tg_id: int, tokens: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.tokens += tokens
            await session.commit()
        else:
            return False

async def get_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user

async def change_model(tg_id: int, model: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.model = model
            await session.commit()
        else:
            return False

async def check_admin(tg_id: int):
    async with async_session() as session:
        admin = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))
        if not admin:
            return False
        else:
            return True

async def add_questions():
    questions = [
        {"level": 1, "question": "Сколько будет 2 + 2?", "answer": "4", "subject": "математика"},
        {"level": 1, "question": "Как называется столица России?", "answer": "Москва", "subject": "география"},
        {"level": 2, "question": "Сколько будет 12 * 12?", "answer": "144", "subject": "математика"},
        {"level": 2, "question": "Кто написал 'Войну и мир'?", "answer": "Толстой", "subject": "литература"},
        {"level": 3, "question": "Решите уравнение: 2x + 3 = 7. Найдите x.", "answer": "2", "subject": "математика"},
        {"level": 3, "question": "В каком году началась Великая Отечественная война?", "answer": "1941", "subject": "история"}
    ]

    async with async_session() as session:
        for q in questions:
            session.add(Question(**q))
        await session.commit()

async def get_random_question(level: int):
    async with async_session() as session:
        question = await session.scalar(
            select(Question).where(Question.level == level).order_by(func.random())
        )
        return question
    
async def update_rating(tg_id: int, points: int):
    async with async_session() as session:
        rating = await session.scalar(select(Rating).where(Rating.tg_id == tg_id))
        if not rating:
            session.add(Rating(tg_id=tg_id, points=points))
        else:
            rating.points += points
        await session.commit()

async def get_top_ratings(limit=10):
    async with async_session() as session:
        results = await session.execute(
            select(User.username, Rating.points)
            .join(Rating, User.tg_id == Rating.tg_id)
            .order_by(Rating.points.desc())
            .limit(limit)
        )
        return results.all()