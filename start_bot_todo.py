from aiogram.utils import executor
from admin import bot, dp
from main_bot import register

register(dp)

executor.start_polling(dp, skip_updates=True)