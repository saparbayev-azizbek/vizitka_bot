import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '6508279637:AAHvlYyOkjPjvVZixjIMnAjdrd3CAkGSau4'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# FSM (Finite State Machine) obyekti yaratamiz
class States(StatesGroup):
    START = State()
    FIRST_QUESTION = State()
    SECOND_QUESTION = State()

# /start buyrug'i
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Salom! Men test botman. Sizga 3 savol beraman. Boshlash uchun /question buyrug'ini bering.")
    await States.START.set()

# /question buyrug'i
@dp.message_handler(Command('question'), state=States.START)
async def process_command(message: types.Message, state: FSMContext):
    await message.reply("Sizning ismingizni yuboring.")
    await States.FIRST_QUESTION.set()

# Foydalanuvchi ismini saqlash
@dp.message_handler(state=States.FIRST_QUESTION)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply(f"Rahmat! {data['name']}, yoshingizni yuboring.")

    # Keyingi holatga o'tish
    await States.next()

# Foydalanuvchi yoshini saqlash
@dp.message_handler(state=States.next)
async def process_age(message: types.Message, state: FSMContext):
    # State ichidagi ma'lumotlarga murojat qilamiz
    async with state.proxy() as data:
        data['age'] = message.text

    await message.reply(f"Sizning yoshingiz {data['age']} da. So'nggi savol uchun /done buyrug'ini bering.")

    # Keyingi holatga o'tish
    await States.NEXT.set()

# /done buyrug'i
@dp.message_handler(Command('done'), state=States.next)
async def process_done(message: types.Message, state: FSMContext):
    # State ichidagi ma'lumotlarni olish
    async with state.proxy() as data:
        name = data['name']
        age = data['age']

    await message.reply(f"Javoblar: Ismingiz - {name}, Yoshingiz - {age}. Rahmat!")

    # Holatni yakunlash
    await state.finish()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
