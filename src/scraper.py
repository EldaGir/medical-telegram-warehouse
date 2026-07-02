import os

from dotenv import load_dotenv
from telethon import TelegramClient

from pathlib import Path

# Load variables from the .env file
load_dotenv()

#Read credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# Create a Telegram client
client = TelegramClient('telegram_session', API_ID, API_HASH)

CHANNELS = [
    "@CheMed123",
    "@lobelia4cosmetics",
    "@tikvahpharma",
    "@Thequorachannel",
    "@ETHIOPHARMAINFO",
]

async def scrape_channel(channel_username):
    channel = await client.get_entity(channel_username)

    channel_folder = Path("data/raw/images") / channel_username
    channel_folder.mkdir(parents=True, exist_ok=True)

    print("=" * 50)
    print(f"Channel: {channel.title}")
    print("=" * 50)

    async for message in client.iter_messages(channel, limit=5):
        message_data = {
            "message_id": message.id,
            "date": message.date.isoformat() if message.date else None,
            "text": message.message,
            "views": message.views,
            "forwards": message.forwards,
            "has_media": message.media is not None,
        }
        print(message_data)

        if message.photo:
            image_path = channel_folder / f"{message.id}.jpg"

            await client.download_media(
                message,
                file=image_path,
            )

            print(f"Downloaded image: {image_path}")


        # print(f"Message ID : {message.id}")
        # print(f"Date : {message.date}")
        # print(f"Text : {message.message}")
        # print(f"Views : {message.views}")
        # print(f"Forwards : {message.forwards}")
        # print(f"Has Media : {message.media is not None}")

        print("-" * 50)


async def main():
    await client.start(phone=PHONE_NUMBER)

    for channel_username in CHANNELS:

        channel = await scrape_channel(channel_username)

    # print("Successfully connected!")
    # print(f"Channel Name: {channel.title}")
    # print(f"Channel ID: {channel.id}")
    # print(f"Username: @{channel.username}")

with client:
    client.loop.run_until_complete(main())