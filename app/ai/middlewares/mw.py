# from typing import Any, Callable, Awaitable

# from aiogram import BaseMiddleware
# from aiogram.types import Message, CallbackQuery

# from sqlalchemy.ext.asyncio import AsyncSession

# class DBSessionMiddleWare(BaseMiddleware):
# 	def __init__(self, session: Callable[[], Awaitable[AsyncSession]]):
# 		super().__init__()
# 		self.session = session

# 	async def on_process_message(self, message: Message, data: dict[str, Any]):
# 		data['session'] = await self.session()

# 	async def on_process_callback_query(self, call: CallbackQuery, data: dict[str, Any]):
# 		data['session'] = await self.session()