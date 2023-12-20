from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from telegram import Bot, Update
import os
import spark_client

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
APP_URL = os.getenv("APP_URL")
bot = Bot(token=TELEGRAM_TOKEN)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(f"/{TELEGRAM_TOKEN}")
async def respond(request: Request):
    json_string = await request.json()
    print("Message received: ", json_string)
    update = Update.de_json(json_string, bot)

    message = update.message if update.message else update.edited_message
    chat_id = message.chat.id
    msg_id = message.message_id
    text = message.text.encode('utf-8').decode()
    print("Message received: ", text)
    if text == "/start":
        bot_welcome = """
        欢迎欢迎！我是科大讯飞星火小助手，您有什么问题都可以问我哦！
        """
        await bot.sendMessage(chat_id=chat_id, text=bot_welcome)
    else:
        # await bot.sendMessage(chat_id=chat_id, text="What a nice day!", reply_to_message_id=msg_id)
        answer = spark_client.ask(text)
        if answer is None:
            answer = "抱歉，我脑子有些问题，请让我休息几秒钟。"
        await bot.sendMessage(chat_id=chat_id, text=answer)

    return "ok"


@app.post('/set_webhook')
async def set_webhook(request: Request):
    webhook = f"{APP_URL}/{TELEGRAM_TOKEN}"
    success = await bot.setWebhook(webhook)
    if success:
        return f"Webhook setup ok"
    else:
        return f"Webhook setup failed"