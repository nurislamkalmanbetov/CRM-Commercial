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


class Aplications:
    def __init__(self, message: types.Message):
        self.bot = bot
        self.message = message

    class AplicationsFSM(StatesGroup):
        email = State()

    async def applications(self, message: Message):
        await self.AplicationsFSM.email.set()
        await message.answer('Отправьте вашу почту для проверки')

        @dp.message_handler(state=self.AplicationsFSM.email)
        async def email_handler(message: types.Message, state: FSMContext):
            email_received = message.text
            check_manager = await user_get(email_received)
            user_id = message.from_user.id

            if not check_manager:
                await state.finish()
                return await message.answer('Вы не менеджер')

           
            data = {
                'user_id': user_id,
                'username': message.from_user.first_name
            }
            add_user = await user_post(data)
            if add_user:
                await state.finish()
                return await message.answer('Поздравляем! 🎉 Вы успешно зарегистрировались и теперь будете получать уведомления о новых заявках. 📬')
            else:
                await state.finish()
                return await message.answer('Произошла ошибка попробуйте позже')
            