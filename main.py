import os
import qrcode
from config import dp, bot, CHANNEL_ID
import logging
import asyncio
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold
from PIL import Image, ImageFont, ImageDraw
from location_to_qrcode import to_qrcode
from aiogram import Bot, Dispatcher, types, executor


# 'start' buyrug'i uchun
@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    print(message.from_user.first_name)

    await message.answer(f'👋 Assalomu alaykum {hbold(message.from_user.first_name)}!\n'
                         f"Botga xush kelibsiz. Botdan foydalanish bo'yicha\n"
                         f"qo'llanmani /help buyrug'i orqali olishingiz mumkin.",
                         parse_mode='HTML')




# Telefon raqam uchun buyruq
@dp.message_handler(lambda message: message.text.startswith('+'))
async def get_phone(message: types.Message):
    user_id = message.from_user.id
    raqam = message.text
    image = Image.open(f'rasmlar_22_{user_id}.jpg')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Montserrat-Bold.ttf', 25)
    rasm = Image.open(f'1_{user_id}.jpg')
    height = rasm.height
    pos = (20, height - 50)
    color = (0, 0, 0)
    draw.text(pos, raqam, fill=color, font=font)
    image.save(f'rasmlar_33_{user_id}.jpg')
    await bot.send_photo(
        chat_id=user_id,
        photo=InputFile(f'rasmlar_33_{user_id}.jpg')
    )


# Textni qrcodega aylantirish
@dp.message_handler()
async def send_qr_code(message: types.Message):
    try:
        user_id = message.from_user.id
        filename = f'qr_{user_id}.jpg'
        image = qrcode.make(message.text)
        image.save(filename)
        image = Image.open(f'qr_{user_id}.jpg')
        rasm = Image.open(f'1_{user_id}.jpg')
        height = rasm.height
        widht = rasm.width
        qrheight = height // 4
        new_size = (qrheight, qrheight)
        resize_img = image.resize(new_size)
        resize_img.save(f'qr_{user_id}.jpg')
        img1 = Image.open(f'1_{user_id}.jpg')
        img2 = Image.open(f'qr_{user_id}.jpg')
        img1.paste(img2, (widht - qrheight - 10, 3 * qrheight - 10))
        img1.save(f'rasmlar_22_{user_id}.jpg')
        await message.answer(f'👍 Ajoyib! Endi telefon raqamni yuboring!\n'
                             f"⚠️ Eslatma! Raqam '+' belgisi bilan boshlanishi lozim")
    except:
        await message.answer(f'Faqat matnli xabar yuboring!')


# Lokatsiyani qrcodega aylantirish
@dp.message_handler(content_types=types.ContentType.LOCATION)
async def process_location(message: types.Message):
    # Lokatsiyani olish
    try:
        location = message.location
        # to_qrcodedan foydalanish
        user_id = message.from_user.id
        to_qrcode(location, message.from_user.id)
        image = Image.open(f'qr_{user_id}.jpg')
        rasm = Image.open(f'1_{user_id}.jpg')
        height = rasm.height
        new_size = (height // 3, height // 3)
        resize_img = image.resize(new_size)
        resize_img.save(f'qr_{user_id}.jpg')
        img1 = rasm
        img2 = image
        img1.paste(img2)
        img1.save(f'rasmlar_22_{user_id}.jpg')
        await message.answer(f'👍 Ajoyib! Endi telefon raqamni yuboring!')
    except:
        await message.answer(f'Iltimos, faqat manzil yuboring!')


# Rasmni qabul qilish
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def ret_photo(message: types.Message):
    try:
        user_id = message.from_user.id
        rasm = message.photo[-1]
        file_id = rasm.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        file = await bot.download_file(file_path)

        # Rasmni 'lesson-6' papkasiga saqlash
        photo_path = os.path.join(f'1_{user_id}.jpg')
        with open(photo_path, 'wb') as new_file:
            new_file.write(file.getvalue())
        await message.answer(f'👏 Qoyil. Endi joylashuvni yuboring', parse_mode='HTML')
    except:
        await message.answer(f"Bu amalni bajarish imkoni bo'lmadi\n"
                             f"Keyinroq qaytadan urunib ko'ring!")
