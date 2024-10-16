from bot import *

# Создаем соединение с базой данных (если она не существует, она будет создана)
async def create_table():
    async with aiosqlite.connect('quiz350_bot.db') as db:
      await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
      await db.commit()