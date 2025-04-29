from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter, CommandObject
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from io import BytesIO

from dotenv import load_dotenv
import os

import app.database.requests as rq

from app.ai.ocr import text_recognize
from app.ai.chatbot import AIChatBot

import app.keyboards.kb as kb

from random import randint

rt = Router()

class User(StatesGroup):
    main = State()
    ai_model = State()
    is_asking = State()

class QuizGame(StatesGroup):
    waiting_for_answer = State()

load_dotenv()

openai_bot = AIChatBot(os.getenv('GITHUB_TOKEN'), "openai/gpt-4.1")
deepseek_bot = AIChatBot(os.getenv('GITHUB_TOKEN'), "deepseek/DeepSeek-V3-0324")
llama_bot = AIChatBot(os.getenv('GITHUB_TOKEN'), "meta/Llama-4-Scout-17B-16E-Instruct")


@rt.message(CommandStart()) # https://t.me/AIschool_help_bot?start=ref_1175527638
async def send_welcome(msg: Message, command: CommandObject):
    global user

    await rq.set_user(msg.from_user.id, msg.from_user.username, msg.from_user.first_name, msg.from_user.last_name)
    user = await rq.get_user(msg.from_user.id)
    await rq.add_questions()

    await msg.answer('Привет', reply_markup=await kb.main(msg.from_user.id))

    if command.args:
        option, value = command.args.split('_')
        match option:
            case 'ref':
                try:
                    inviter_id = int(value)
                except ValueError:
                    return None
                
                inviter = await rq.get_user(inviter_id)
                if not inviter:
                    return None
                
                check = await rq.validate_ref(msg.from_user.id, inviter_id)
                if check:
                    await msg.answer('Вы уже зарегистрированы в реферальной системе')
                if inviter_id == msg.from_user.id:
                    await msg.answer('Вы не можете пригласить себя')
                else:
                    await rq.add_tokens(inviter_id, 1)
                    await rq.add_ref(msg.from_user.id, inviter_id)
                    await msg.answer('Вы успешно зарегистрировались в реферальной системе')
                    await msg.bot.send_message(inviter_id, 'По вашей ссылке зарегистрировался новый пользователь!')


# ИИ ФУНКЦИИ

@rt.callback_query(F.data == 'ask_ai')
async def ask_ai(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Отправь текст или фото задания')
    await state.set_state(User.is_asking)

@rt.message(User.is_asking, F.photo)
async def img(msg: Message, bot: Bot, state: FSMContext):
    mess = await msg.answer(f'Скачиваем фото | ##........ | {randint(15, 20)}%')
    photo = msg.photo[-1]
    photo_bytes = BytesIO()
    await bot.download(photo, destination=photo_bytes)
    photo_bytes.seek(0)
    await mess.edit_text(f'Распознаем текст | ####...... | {randint(20, 40)}%')
    text = await text_recognize(photo_bytes.read())
    await mess.edit_text(f'Обрабатываем текст | ######.... | {randint(40, 60)}%')

    match user.model:
        case "openai/gpt-4.1":
            await mess.edit_text(f'Получаем ответ от ИИ | ########.. | {randint(60, 80)}%')
            try:
                oa = await openai_bot.ask(text)
                await msg.answer(oa, parse_mode="Markdown")
            except Exception as e:
                print(e)
                await msg.answer('Ошибка, попробуйте еще раз ИЛИ сделайте фото лучше', parse_mode="Markdown")
            
        case "deepseek/DeepSeek-V3-0324":
            try:
                await mess.edit_text(f'Получаем ответ от ИИ | ########.. | {randint(60, 80)}%')
                ds = await deepseek_bot.ask(text)
                await msg.answer(ds, parse_mode="Markdown")
            except Exception as e:
                print(e)
                await msg.answer('Ошибка, попробуйте еще раз ИЛИ сделайте фото лучше', parse_mode="Markdown")
        case "meta/Llama-4-Scout-17B-16E-Instruct":
            await mess.edit_text(f'Получаем ответ от ИИ | ########.. | {randint(60, 80)}%')
            try:
                ll = await llama_bot.ask(text)
                await msg.answer(ll, parse_mode="Markdown")
            except Exception as e:
                print(e)
                await msg.answer('Ошибка, попробуйте еще раз ИЛИ сделайте фото лучше', parse_mode="Markdown")
        case _:
            await msg.answer('Ошибка, попробуйте выбрать модель в настройках', parse_mode="Markdown")

    await state.clear()


@rt.message(User.is_asking, F.text)
async def img(msg: Message, bot: Bot, state: FSMContext):
    text = msg.text
    match user.model:
        case "openai/gpt-4.1":
            oa = await openai_bot.ask(text)
            await msg.answer(oa, parse_mode="Markdown")
        case "deepseek/DeepSeek-V3-0324":
            ds = await deepseek_bot.ask(text)
            await msg.answer(ds, parse_mode="Markdown")
        case _:
            await msg.answer('Ошибка, попробуйте выбрать модель в настройках', parse_mode="Markdown")
    await state.clear()

@rt.callback_query(F.data == 'main')
async def main(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Главное меню', reply_markup=await kb.main(call.from_user.id))

@rt.callback_query(F.data.startswith('profile_'))
async def profile(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Профиль', reply_markup=await kb.profile(call.from_user.id))

@rt.callback_query(F.data.startswith('settings_'))
async def settings(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Настройки', reply_markup=await kb.settings(call.from_user.id))

@rt.callback_query(F.data.startswith('choose_'))
async def choose(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Выберите модель', reply_markup=await kb.choose_model(call.from_user.id))

@rt.callback_query(F.data.startswith('openai_'))
async def openai(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await rq.change_model(call.from_user.id, "openai/gpt-4.1")
    await call.message.answer('Вы выбрали OpenAI', reply_markup=await kb.settings(call.from_user.id))

@rt.callback_query(F.data.startswith('deepseek_'))
async def deepseek(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await rq.change_model(call.from_user.id, "deepseek/DeepSeek-V3-0324")
    await call.message.answer('Вы выбрали DeepSeek', reply_markup=await kb.settings(call.from_user.id))

@rt.callback_query(F.data.startswith('llama_'))
async def deepseek(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await rq.change_model(call.from_user.id, "meta/Llama-4-Scout-17B-16E-Instruct")
    await call.message.answer('Вы выбрали Llama 4 Scout', reply_markup=await kb.settings(call.from_user.id))

@rt.callback_query(F.data == 'minigame')
async def minigame(call: CallbackQuery):
	await call.answer()
	await call.message.delete()
	await call.message.answer('Мини-игра', reply_markup=await kb.minigame(call.from_user.id))

@rt.callback_query(F.data == 'start_quiz')
async def start_quiz(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    username = call.from_user.username

    # Проверяем, есть ли пользователь в базе данных
    user = await rq.get_user(user_id)
    if not user:
        await rq.set_user(user_id, username)

    # Получаем уровень пользователя
    user_data = await rq.get_user(user_id)
    level = user_data.level

    # Получаем случайный вопрос из базы
    question = await rq.get_random_question(level)
    await state.update_data(question_id=question.id, correct_answer=question.answer)

    await call.message.answer(f"Вопрос ({question.subject}): {question.question}")
    await state.set_state(QuizGame.waiting_for_answer)

@rt.message(QuizGame.waiting_for_answer, F.text)
async def check_answer(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    data = await state.get_data()

    # Проверяем ответ
    if msg.text.strip().lower() == data['correct_answer'].lower():
        await rq.update_rating(user_id, points=10)
        await msg.answer("Правильно! Ты заработал 10 очков рейтинга.")
    else:
        await msg.answer(f"Неправильно. Правильный ответ: {data['correct_answer']}")

    # Завершаем текущий вопрос
    await state.clear()