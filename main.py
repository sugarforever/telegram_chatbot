from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import telegram
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
APP_URL = os.getenv("APP_URL")
bot = telegram.Bot(token=TELEGRAM_TOKEN)

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
    body = await request.json()

    chat_id = body["message"]["chat"]["id"]
    msg_id = body["message"]["message_id"]
    text = body["message"]["text"].encode('utf-8').decode()
    print("Message received: ", text)
    if text == "/start":
        bot_welcome = """
        Welcome. I can answer any question you have about LangChain framework.
        """
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
    else:
        bot.sendMessage(chat_id=chat_id, text="What a nice day!", reply_to_message_id=msg_id)
    
    return "ok"

@app.route('/set_webhook', methods=['GET', 'POST'])
async def set_webhook(request: Request):
   webhook = f"{APP_URL}/{TELEGRAM_TOKEN}"
   await bot.setWebhook(url=webhook)
   return "webhook setup ok"