from aiogram import executor
from config import dp

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
