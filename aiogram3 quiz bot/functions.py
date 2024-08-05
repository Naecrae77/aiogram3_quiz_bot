import aiosqlite
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from quiz_data import quiz_data


# Enable logging so you don't miss important messages
logging.basicConfig(level=logging.INFO)

# Bot object
bot = Bot(token=keys)
# Dispatcher
dp = Dispatcher()

# Database name
DB_NAME = 'quiz_bot.db'


def generate_options_keyboard(answer_options, right_answer):
    # Create an Inline keyboard collector
    builder = InlineKeyboardBuilder()

    # In a loop we create 4 Inline buttons, or rather Callback buttons
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            # The text on the buttons corresponds to the answer options
            text=option,
            # Assign data for the callback request.
            # If the answer is correct, a callback request will be generated with the data 'right_answer'
            # If the answer is incorrect, a callback request will be generated with the data 'wrong_answer'
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )

    # Display one button at a time in a column
    builder.adjust(1)
    return builder.as_markup()

@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    # edit the current message to remove the buttons (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id = callback.from_user.id,
        message_id = callback.message.message_id,
       reply_markup=None
    )

    # Get the current question for a given user
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_score = await get_user_score(callback.from_user.id)

    # Send a message to the chat that the answer is correct
    await callback.message.answer('correct!')

    # Update the current question number in the database
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    current_score += 1
    await update_user_score(callback.from_user.id, current_score)


    # Check if the end of the quiz has been reached
    if current_question_index < len(quiz_data):
        # Next question
        await get_question(callback.message, callback.from_user.id)
    else:
        # Notification about the end of the quiz
        await callback.message.answer(f"That was the last question. Quiz is over. Your score was {current_score}/{len(quiz_data)}")

@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):

    await callback.bot.edit_message_reply_markup(
        chat_id = callback.from_user.id,
        message_id = callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    current_score = await get_user_score(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    # Send an error message to the chat indicating the correct answer
    await callback.message.answer(f"Incorrect. Correct answer: {quiz_data[current_question_index]['options'][correct_option]}")

    # Update the current question number in the database
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    await update_user_score(callback.from_user.id, current_score)

    # Check if the end of the quiz has been reached
    if current_question_index < len(quiz_data):
        # Next question
        await get_question(callback.message, callback.from_user.id)
    else:
        # Notification about the end of the quiz
        await callback.message.answer(f"That was the last question. Quiz is over! Your score was {current_score}/{len(quiz_data)}")

# Handler for the /start command
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Create a keyboard collector of type Reply
    builder = ReplyKeyboardBuilder()
    # Add one button to the collector
    builder.add(types.KeyboardButton(text="Start Quiz"))
    # Attach buttons to the message
    await message.answer("Hi! I'm Naecrae quiz bot. Type /quiz to get started.\nDon't know what to do? type /help", reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True))

async def get_question(message, user_id):

    # Request the current index for the question from the database
    current_question_index = await get_quiz_index(user_id)
    # Get the index of the correct answer for the current question
    correct_index = quiz_data[current_question_index]['correct_option']
    # Get a list of answer options for the current question
    opts = quiz_data[current_question_index]['options']

    # Function for generating buttons for the current quiz question
    # As arguments we pass the answer options and the value of the correct answer (not the index!)
    kb = generate_options_keyboard(opts, opts[correct_index])
    # Send a message to the chat with a question, attach the generated buttons
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    # get the id of the user who sent the message
    user_id = message.from_user.id
    # reset the value of the current quiz question index to 0
    current_question_index = 0
    new_score = 0
    await update_quiz_index(user_id, current_question_index)
    await update_user_score(user_id, new_score)
    # request a new question for the quiz
    await get_question(message, user_id)


async def get_quiz_index(user_id):
    # Connect to the database
    async with aiosqlite.connect(DB_NAME) as db:
        # Get an entry for a given user
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Return the result
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def get_user_score(user_id):
    # Connect to the database
    async with aiosqlite.connect(DB_NAME) as db:
        # Get an entry for a given user
        async with db.execute('SELECT score FROM users WHERE user_id = (?)', (user_id,)) as cursor:
            # Return the result
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def update_quiz_index(user_id, index):
    # Create a connection to the database (if it does not exist, it will be created)
    async with aiosqlite.connect(DB_NAME) as db:
        # Insert a new entry or replace it if there is already one with the given user_id
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Save changes
        await db.commit()

async def update_user_score(user_id, new_score):
    # Create a connection to the database (if it does not exist, it will be created)
    async with aiosqlite.connect(DB_NAME) as db:
        # Insert a new entry or replace it if there is already one with the given user_id
        await db.execute('INSERT INTO users (user_id, score) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET score = excluded.score', (user_id, new_score))
        # Save changes
        await db.commit()

# Command handler /quiz
@dp.message(F.text=="Start Quiz")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Send a new message without buttons
    await message.answer(f"Let's start the quiz!")
    # Launching a new quiz
    await new_quiz(message)


async def create_table():
    # Create a connection to the database (if it does not exist, it will be created)
    async with aiosqlite.connect('quiz_bot.db') as db:
        # Execute an SQL query to the database
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, score INTEGER)''')       
        # Save changes
        await db.commit()

#help handler
@dp.message(Command('help'))
async def cmd_start(message: types.Message):
    await message.answer('Bot commands: \n/start: Start interaction with NaecraeBot \n/quiz: Start the quiz \n/help: Help options')
