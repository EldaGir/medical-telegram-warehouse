import os
import json
import logging


from dotenv import load_dotenv
from telethon import TelegramClient

from pathlib import Path
from datetime import datetime


logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

logging.basicConfig(
    filename = "logs/scraper.log",
    level = logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

MESSAGE_LIMIT = 500
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

    logging.info(f"Scraping channel: {channel.username}")

    channel_folder = Path("data/raw/images") / channel.username
    channel_folder.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    json_folder = Path("data/raw/telegram_messages") / today
    json_folder.mkdir(parents=True, exist_ok=True)

    print("=" * 50)
    print(f"Channel: {channel.title}")
    print("=" * 50)

    print(f"Scraping {channel.title}...")

    messages = []

    async for message in client.iter_messages(channel, limit=MESSAGE_LIMIT):
        message_data = {
            "message_id": message.id,
            "date": message.date.isoformat() if message.date else None,
            "text": message.message,
            "views": message.views,
            "forwards": message.forwards,
            "has_media": message.media is not None,
        }

        messages.append(message_data)

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

    json_file = json_folder / f"{channel.username}.json"

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)
    print(f"Saved {len(messages)} messages to {json_file}")

    logging.info(
        f"Saved {len(messages)} messages from {channel.username}"
    )

async def main():
    await client.start(phone=PHONE_NUMBER)

    for channel_username in CHANNELS:

        try:
            await scrape_channel(channel_username)

        except Exception as error:

            logging.error(
                f"Failed to scrape {channel_username}: {error}"
            )

            print(
                f"Error scraping {channel_username}: {error}"
            )


    # print("Successfully connected!")
    # print(f"Channel Name: {channel.title}")
    # print(f"Channel ID: {channel.id}")
    # print(f"Username: @{channel.username}")

with client:
    client.loop.run_until_complete(main())