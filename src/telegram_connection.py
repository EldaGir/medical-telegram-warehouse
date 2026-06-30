import os

from dotenv import load_dotenv
from telethon import TelegramClient

# Load variables from the .env file
load_dotenv()

#Read credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# Create a Telegram client
client = TelegramClient('telegram_session', API_ID, API_HASH)

async def main():
    await client.start(phone=PHONE_NUMBER)

    me = await client.get_me()

    print("Successfully connected to Telegram!")
    print(f"Logged in as: {me.first_name}")
    print(f"Username: {me.username}")
    print(f"Phone: {me.phone}")

with client:
    client.loop.run_until_complete(main())