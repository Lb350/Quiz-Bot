import asyncio
import aiosqlite

from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F

from config import *
from aiosqlitedb import *
from questions import quiz_data




def generate_options_keyboard(answer_options, right_answer):
  builder = InlineKeyboardBuilder()

  for option in answer_options:
    builder.add(types.InlineKeyboardButton(
        text=option,
        callback_data='right_answer' if option == right_answer else 'wrong_answer')
    )
  builder.adjust(1)
  return builder.as_markup()


@dp.callback_query(F.data == 'right_answer')
@dp.callback_query(F.data == "wrong_answer")
async def right_answer(callback: types.CallbackQuery):

  await callback.bot.edit_message_reply_markup(
      chat_id=callback.from_user.id,
      message_id=callback.message.message_id,
      reply_markup=None,

  )

  current_question_index = await get_quiz_index(callback.from_user.id)
  correct_option = quiz_data[current_question_index]['correct_option']
  current_score = await get_rating(callback.from_user.id)

  if callback.data == 'right_answer':

    await callback.message.answer(f"Верно!")
    current_score += 1
    await update_rating(callback.from_user.id, current_score)
  else:
      await callback.message.answer(f"Неправильно.\nПравильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

  current_question_index += 1
  await update_quiz_index(callback.from_user.id, current_question_index)

  if current_question_index < len(quiz_data):
    await get_question(callback.message, callback.from_user.id)
  else:
    await callback.message.answer(f'Это был последний вопрос. Ваш результат {current_score} правильных ответов. Квиз завершен!')

# Хэндлер на команду /start
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
  builder = ReplyKeyboardBuilder()
  builder.add(types.KeyboardButton(text='Начнём?'))
  await message.answer('Добро пожаловать в квиз!', reply_markup=builder.as_markup(resize_keyboard=True))


# Получение текущего вопроса из словаря состояний пользователя
async def get_question(message, user_id):
  current_question_index = await get_quiz_index(user_id)
  correct_index = quiz_data[current_question_index]['correct_option']
  opts = quiz_data[current_question_index]['options']
  kb = generate_options_keyboard(opts, opts[correct_index])
  await message.answer(f'{quiz_data[current_question_index]["question"]}', reply_markup=kb)


async def new_quiz(message):
  user_id = message.from_user.id
  current_question_index = 0
  new_score = 0
  await update_quiz_index(user_id, current_question_index)
  await update_rating(user_id, new_score)
  await get_question(message, user_id)


async def get_quiz_index(user_id):
  async with aiosqlite.connect('quiz350_bot.db') as db:
    async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
      results = await cursor.fetchone()
      if results is not None:
        return results[0]
      else:
        return 0


async def update_quiz_index(user_id, index):
  async with aiosqlite.connect('quiz350_bot.db') as db:
    await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
    await db.commit()


async def get_rating(user_id):
  async with aiosqlite.connect('quiz350_bot.db') as db:
    async with db.execute('SELECT rating FROM users WHERE user_id = (?)', (user_id,)) as cursor:
      results = await cursor.fetchone()
      if results is not None:
        return results[0]
      else:
        return 0

async def update_rating(user_id, new_score):
  async with aiosqlite.connect('quiz350_bot.db') as db:
    await db.execute('INSERT INTO users (user_id, rating) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET rating = excluded.rating', (user_id, new_score))
    await db.commit()


# Хэндлер на команду /quiz
@dp.message(F.text=='Начнём?')
@dp.message(Command('quiz'))
async def cmd_quiz(message: types.Message):

  await message.answer('Давайте начнем квиз!')
  await new_quiz(message)

# Хендлер на команду /help
@dp.message(Command('help'))
async def cmd_help(message: types.Message):
  await message.answer('Это квиз, где нужно выбрать правильный ответ')
  await message.answer('Команды бота:\n\start - начать взаимодействие с ботом\n\help - открыть помощь\n\quiz - начать квиз')


# Запуск процесса поллинга новых апдейтов
async def main():

  await create_table()

  await dp.start_polling(bot)


if __name__ == '__main__':
  asyncio.run(main())
