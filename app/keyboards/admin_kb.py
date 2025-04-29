from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
						ReplyKeyboardMarkup, KeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.database.requests import check_admin

async def admin_panel(tg_id: int):
	admin = InlineKeyboardMarkup(inline_keyboard=[
			[InlineKeyboardButton(text='Панель админа', callback_data='admin_panel')],
			[InlineKeyboardButton(text='Вывести токены', callback_data=f'withdraw_{tg_id}')]
		])
	return admin