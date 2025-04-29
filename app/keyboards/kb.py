from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
						ReplyKeyboardMarkup, KeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.database.requests import check_admin

async def main(tg_id: int):
	main = InlineKeyboardMarkup(inline_keyboard=[
			[InlineKeyboardButton(text='Спросить нейросеть', callback_data='ask_ai')],
			[InlineKeyboardButton(text='Профиль', callback_data=f'profile_{tg_id}'), 
			InlineKeyboardButton(text='Настройки', callback_data=f'settings_{tg_id}')],
			[InlineKeyboardButton(text='Мини-игра', callback_data='minigame')],
			# [InlineKeyboardButton(text='Пожертвовать', callback_data='donate')],
			])
	if await check_admin(tg_id) == True:
		main.add(InlineKeyboardButton(text='Панель админа', callback_data='admin_panel'))
		return main
	else:
		return main
	
async def profile(tg_id: int):
	profile = InlineKeyboardMarkup(inline_keyboard=[
			[InlineKeyboardButton(text='Выбрать модель ИИ', callback_data=f'choose_{tg_id}')],
			[InlineKeyboardButton(text='Реферальная система', callback_data=f'refferal_{tg_id}')],
			[InlineKeyboardButton(text='Назад', callback_data='main')]
			])
	return profile

async def settings(tg_id: int):
	settings = InlineKeyboardMarkup(inline_keyboard=[
			[InlineKeyboardButton(text='Выбрать модель ИИ', callback_data=f'choose_{tg_id}')],
			[InlineKeyboardButton(text='Назад', callback_data='main')]
			])
	return settings

async def choose_model(tg_id: int):
	choose_model = InlineKeyboardMarkup(inline_keyboard=[
			[InlineKeyboardButton(text='OpenAI', callback_data=f'openai_{tg_id}')],
			[InlineKeyboardButton(text='DeepSeek', callback_data=f'deepseek_{tg_id}')],
			[InlineKeyboardButton(text='Llama 4 Scout', callback_data=f'llama_{tg_id}')],
			[InlineKeyboardButton(text='Назад', callback_data='profile')]
			])
	return choose_model

async def minigame(tg_id: int):
	minigame = InlineKeyboardMarkup(inline_keyboard=[
			[InlineKeyboardButton(text='Начать викторину', callback_data=f'start_quiz')],
			[InlineKeyboardButton(text='Назад', callback_data='main')]
			])
	return minigame