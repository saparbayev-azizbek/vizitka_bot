from aiogram import Bot, Dispatcher
import logging

token = '6508279637:AAHvlYyOkjPjvVZixjIMnAjdrd3CAkGSau4'
CHANNEL_ID = '+inqZaI6qg2llNzM6'
bot = Bot(token=token)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)