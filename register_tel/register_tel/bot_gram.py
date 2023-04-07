import asyncio
import sys
import os
import logging
import dotenv
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import State, StatesGroup

from django.conf import settings
from settings import MEDIA_ROOT
from key_bot import KEY_TOKEN

sys.path.append(os.path.dirname(os.path.abspath('bot.py')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_registration.settings')
settings.configure()

dotenv.load_dotenv()

API_TOKEN = KEY_TOKEN


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logger = logging.getLogger()
new_user = {}


class Registration(StatesGroup):
    username = State()
    first_name = State()
    last_name = State()
    password = State()
    password2 = State()
    photo = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    new_user['telegram_id'] = message.from_id
    new_user['nick_name'] = f'@{message.from_user.username}'
    await message.answer('Please enter your username:')
    await Registration.username.set()


@dp.message_handler(state=Registration.username)
async def process_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
        new_user['username'] = data['username']
    await message.answer('Please enter your first name:')
    await Registration.first_name.set()


@dp.message_handler(state=Registration.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
        new_user['first_name'] = data['first_name']
    await message.answer('Please enter your last name:')
    await Registration.last_name.set()


@dp.message_handler(state=Registration.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text
        new_user['last_name'] = data['last_name']
    await message.answer('Please enter your password:')
    await Registration.password.set()


@dp.message_handler(state=Registration.password)
async def process_password(message: types.Message, state: FSMContext):
    # save the user's nickname and end the registration process
    async with state.proxy() as data:
        data['password'] = message.text
    await message.answer('Please enter your password again:')
    await Registration.password2.set()


@dp.message_handler(state=Registration.password2)
async def process_password2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password2'] = message.text
        new_user['password'] = data['password2']
        if data['password2'] == data['password']:
            await message.answer('Do you agree to receive your photo? (yes/no)')
            await Registration.photo.set()
        else:
            await message.reply('Passwords do not match. Try again: ')
            await Registration.password2.set()


@dp.message_handler(state=Registration.photo)
async def get_user_photo(message: types.Message, state: FSMContext):
    if message.text in ['y', 'Y', 'ok', 'Ok', 'OK', 'yes', 'YES', 'Yes', '+']:
        user_profile_photo = await bot.get_user_profile_photos(message.from_id)
        if user_profile_photo.photos and len(user_profile_photo.photos[0]) > 0:
            file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
            photo = f'{MEDIA_ROOT}/user_{message.from_id}_photo.png'
            await bot.download_file(file.file_path, f'{MEDIA_ROOT}/user_{message.from_id}_photo.png')
            async with state.proxy() as data:
                data['photo'] = photo
                new_user['photo'] = data['photo']
        else:
            await message.answer("You have no photos to save.")
    else:
        await message.answer("Your photos were not saved!!!")
    print(new_user)
    response = requests.post('http://127.0.0.1:8000/save-user/', json=new_user)
    logger.info(new_user)
    if response.status_code == 200:
        await message.answer('User saved to database!')
    else:
        await message.answer('Error saving user to database.')
    await state.finish()
    await message.answer("You have been registered, please follow the link below to validate your account.")
    await message.answer("http://127.0.0.1:8000/accounts/login /")



# start the bot
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()
