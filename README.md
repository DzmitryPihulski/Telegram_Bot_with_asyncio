# Telegram bot with AI

## Introduction
This bot was created in self-studing proposes.<br>
Everything was written in 1 file bot.py<br>
There is file .env with BOT TOKEN and other passwords. It was not included in this repositori.

## Bot commands
1. Start command: basic command where bot will send sticker and greatings.

2. Weather checker: You can check current weather in any city.<br> Bot will ask you to give him city's name. After that, with the help of FSM content and python_weather library, it will reply.

3. Ask AI: This feature uses openAI API to ask AI questions. It not free program, so the number of questions is limited, because I have free trial.

4. Horoscope check: This time bot will ask you about your zodiac sign and date. With the help of requests library and API, it will send you horoscope for this zodiac sign and date.

5. Sending documents: If you will send any document to bot, it will forward your document to certain group.

6. Generating qr-codes: If you will send anything that is not in above commands, it will make a qr-code of your message and reply with it.

## Used libraryies
* asyncio 3.4.3
* logging 0.4.9.6
* requests 2.31.0
* pyqrcode 1.2.1
* openai 0.28.0
* aiogram 3.0.0
* dotenv 1.0.0
* python_weather 1.0.3
## Instalation process
First of all make your own .env file in the same folder with my bot.py.
Add to you .env file this:<br>
    <b>TOKEN</b> = your bot token<br>
    <b>GROP_CHAT</b> = your group id<br>
    <b>OPEN_AI_KEY</b> = your key<br>
Second. Add bot to the group and give him admin status.<br>
You are done.