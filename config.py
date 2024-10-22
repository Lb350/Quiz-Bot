import os
from dotenv import load_dotenv
import logging
from aiogram import Bot, Dispatcher

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()