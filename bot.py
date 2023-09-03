import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold


from dotenv import load_dotenv
import os
import python_weather

load_dotenv()
TOKEN = os.getenv('TOKEN')
dp = Dispatcher()

keybord=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Weather'),KeyboardButton(text='Horoscope')]])



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer_sticker('CAACAgIAAxkBAAEKNZ9k9EtDMD6d6zon0zd1w00qI6kgTgAC7BAAAsa5YEsGgHzZTAQLJDAE')
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!",reply_markup=keybord)

@dp.message(F.text=='Weather')
async def get_weather(message: Message):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get('Wroclaw')
        await message.answer(f'Current weather:\n{weather.current.kind} {round((weather.current.temperature-32)*(5/9))}°C\nWind speed:{round(weather.current.wind_speed*1.6)} km/h')

@dp.message(F.text=='Horoscope')
async def get_weather(message: Message):

@dp.message(F.document)
async def get_weather(message: Message):
    await message.forward(os.getenv('GROP_CHAT'))


@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.answer('I do not understand you.')
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())