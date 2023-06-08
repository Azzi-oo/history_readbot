import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


TOKEN = "6113793608:AAH3iBMzaAvmPKi6j5d-xVUxv42Po80-aAY"
MSG = "Поделись своей историей, {}"
GROUP_LINK = '-1001522000294'



logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
reply_button_message = 'Написать еще'
welcome_message = 'Здесь можно написать вашу историю для канала Три Подруги. Публикуем всегда анонимно.'


async def start(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton
    keyboard.add(start_button)
    await message.answer(reply_markup=keyboard)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message, state: FSMContext):
    user_full_name = message.from_user.full_name
    await message.reply(welcome_message)


@dp.message_handler(commands=[reply_button_message])
async def repeat_story_handler(message: types.Message, state: FSMContext):
    user_full_name = message.from_user.full_name
    await message.reply(f'Хорошо, {user_full_name}! {MSG.format(user_full_name)}')
    await message.reply(welcome_message)


@dp.message_handler()
async def message_handler(message: types.Message, state: FSMContext):
    user_full_name = message.from_user.full_name
    if message.text == reply_button_message:
        await message.reply(welcome_message)
        return

    user_full_name = message.from_user.full_name
    user_id = message.from_user.id
    logging.info(f'{user_id} {user_full_name}')

    try:
        if message.text != reply_button_message:
            print(message.text)
            await bot.send_message(GROUP_LINK, message.text, parse_mode='Markdown')
            await message.reply(f'Спасибо, {user_full_name}. Ваша история принята и обязательно будет прочитана', reply_markup=get_repeat_keyboard())               
    except Exception as e:
        logging.exception(str(e))
        await message.reply('Произошла ошибка при отправке сообщения. Попробуйте еще раз позже.')

    await state.finish()


def get_repeat_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(reply_button_message)
    keyboard.add(button)
    return keyboard


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
