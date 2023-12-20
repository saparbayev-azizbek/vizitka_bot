from config import dp
from aiogram import types

# 'help' buyrug'i uchun
@dp.message_handler(commands='help')
async def command_help(message: types.Message):
    await message.answer(f"Botdan foydalanish uchun ushbu\n"
                         f"ketma-ketlikka rioya qiling:\n"
                         f"1. Rasm yuboring\n"
                         f"2. Lokatsiya yoki url yuboring\n"
                         f"3. Telefon raqam kiriting (raqam '+' belgisi bilan boshlanishi kerak)"
                         )