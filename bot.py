import asyncio
import logging
import sys
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.methods.send_message import SendMessage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton,Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold


from dotenv import load_dotenv
import os
import python_weather

load_dotenv()
TOKEN = os.getenv('TOKEN')
zodiac_signs=['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
dp = Dispatcher()

keybord=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Weather'),KeyboardButton(text='Horoscope')]])


class Form(StatesGroup):
    city = State()
    zodiac_sign=State()
    horoscope_date=State()
    
def gen_markup(args):
    markup = InlineKeyboardBuilder()
    for i in args:
        markup.button(text=i, callback_data=i)
    markup.adjust(1,repeat=True)
    return markup.as_markup()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer_sticker('CAACAgIAAxkBAAEKNZ9k9EtDMD6d6zon0zd1w00qI6kgTgAC7BAAAsa5YEsGgHzZTAQLJDAE')
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!",reply_markup=keybord)

@dp.message(F.text=='Weather')
async def get_weather(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.city)
    await message.answer("Hi there! What's your city?",reply_markup=ReplyKeyboardRemove())

@dp.message(Form.city)
async def process_weather(message: Message, state: FSMContext):
    await state.clear()
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(message.text)
        await message.answer(f'Current weather:\n{weather.current.kind} {round((weather.current.temperature-32)*(5/9))}°C\nWind speed:{round(weather.current.wind_speed*1.6)} km/h',reply_markup=keybord)

@dp.message(F.text=='Horoscope')
async def get_zodiac_sign(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.zodiac_sign)
    await message.answer("What's your zodiac sign?\nChoose one:",reply_markup=gen_markup(zodiac_signs))

@dp.callback_query(F.data.in_(zodiac_signs))
async def process_sign(message: CallbackQuery, state: FSMContext):
    await state.update_data(zodiac_signs=message.data)
    await state.set_state(Form.horoscope_date)
    await Bot(TOKEN, parse_mode=ParseMode.HTML)(SendMessage(chat_id=message.from_user.id,text="What day do you want to know?\nChoose one: TODAY, TOMORROW, YESTERDAY, or a date in format YYYY-MM-DD."))

@dp.callback_query(Form.horoscope_date)
async def get_horoscope(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    day = str(message.text)
    print(day, type(message.text))
    sign=str(data[zodiac_signs])
    horoscope = await get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\\n*Sign:* {sign}\\n*Day:* {data["date"]}'
    await message.answer(f"Here's your horoscope!\n{horoscope_message}",reply_markup=keybord)

async def get_daily_horoscope(sign: str, day: str) -> dict:
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = await requests.get(url, params)
    return response.json()


@dp.message(F.document)
async def get_weather(message: Message):
    await message.forward(os.getenv('GROP_CHAT'))


@dp.message()
async def echo_handler(message: Message) -> None:
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