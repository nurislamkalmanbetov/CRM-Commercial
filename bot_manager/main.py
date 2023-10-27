
from config import bot, dp 
from aiogram import executor
from aiogram.types import Message
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from api import user_get, user_list, user_post
from applications_user import Aplications

class BotMain:
    def __init__(self):
        dp.register_message_handler(self.handle_commands, commands=['start','help',])
        # dp.register_callback_query_handler(self.callback, lambda c: c.data in [''])


    async def handle_commands(self, message: Message):
        if message.text == '/start':
            user_id = message.from_user.id
            check_user = await user_list(user_id)

            if not check_user:
                applications = Aplications(message)
                return await applications.applications(message)
            
            await message.answer('Вы уже зарегистрированы')




if __name__ == '__main__':
    BotMain()
    executor.start_polling(dp, skip_updates=True)

