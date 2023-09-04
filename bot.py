import asyncio
import logging
import sys
import requests
import pyqrcode
import openai

from aiogram import Bot, Dispatcher, F
from aiogram.methods.send_message import SendMessage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton,Message, CallbackQuery,FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold


from dotenv import load_dotenv
import os
import python_weather

load_dotenv()
TOKEN = os.getenv('TOKEN')
openai.api_key=os.getenv('OPEN_AI_KEY')
openai.Model.list()
zodiac_signs=['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
dp = Dispatcher()

keybord=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Weather'),KeyboardButton(text='Horoscope')],[KeyboardButton(text='Ask AI')]])

def gen_keybord(args):
    list=[]
    for i in args:
        list.append([KeyboardButton(text=i)])
    return ReplyKeyboardMarkup(keyboard=list)

class Form(StatesGroup):
    city = State()
    zodiac_sign=State()
    horoscope_date=State()
    ai_querry=State()
    
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
    await message.answer("Hi there! What's your city?",reply_markup=gen_keybord(['Wroclaw']))

@dp.message(Form.city)
async def process_weather(message: Message, state: FSMContext):
    await state.clear()
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(message.text)
        await message.answer(f'Current weather:\n{weather.current.kind} {round((weather.current.temperature-32)*(5/9))}°C\nWind speed:{round(weather.current.wind_speed*1.6)} km/h',reply_markup=keybord)

@dp.message(F.text=='Ask AI')
async def get_querry(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.ai_querry)
    await message.answer("Hi there! What's your question?",reply_markup=ReplyKeyboardRemove())

@dp.message(Form.ai_querry)
async def process_querry(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Wait for the answer')
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=message.text,
        temperature=1,
        max_tokens=2048,
        top_p=0.7,
        frequency_penalty=0
    )
    await message.answer(response['choices'][0]['text'], reply_markup=keybord)

@dp.message(F.text=='Horoscope')
async def get_zodiac_sign(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.zodiac_sign)
    await message.answer("What's your zodiac sign?\nChoose one",reply_markup=gen_keybord(zodiac_signs))

@dp.message(Form.zodiac_sign)
async def process_sign(message: Message, state: FSMContext):
    await state.update_data(zodiac_sign=message.text)
    await state.set_state(Form.horoscope_date)
    await message.answer("What day do you want to know?\nChoose one: TODAY, TOMORROW, YESTERDAY, or a date in format YYYY-MM-DD.", reply_markup=ReplyKeyboardRemove())

@dp.message(Form.horoscope_date)
async def get_horoscope(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    day = str(message.text)
    print(day, type(message.text))
    sign=str(data['zodiac_sign']).capitalize()
    horoscope = await get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f"{hbold('Horoscope')}: {data['horoscope_data']}\n{hbold('Sign')}: {sign}\n{hbold('Day')}: {data['date']}"
    await message.answer(f"Here's your horoscope!\n{horoscope_message}",reply_markup=keybord)

async def get_daily_horoscope(sign: str, day: str) -> dict:
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)
    return response.json()


@dp.message(F.document)
async def get_weather(message: Message):
    await message.forward(os.getenv('GROP_CHAT'))


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        img=pyqrcode.create(message.text)
        img.png('qrcode.png',scale=5)
        await message.answer_photo(photo=FSInputFile('qrcode.png'),caption='I do not understand you, but here is qr-code of your message',parse_mode='Markdown')
        os.remove('qrcode.png')
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())