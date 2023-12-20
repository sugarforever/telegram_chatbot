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
    print(body)
    return "ok"

@app.route('/set_webhook', methods=['GET', 'POST'])
async def set_webhook(request: Request):
   webhook = f"{APP_URL}/{TELEGRAM_TOKEN}"
   s = await bot.setWebhook(url=webhook)
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"