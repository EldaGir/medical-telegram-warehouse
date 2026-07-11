import os
import json
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

def create_schema(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
    """)
    conn.commit()
    cursor.close()

    print("Schema 'raw' is ready.")

def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
       CREATE TABLE IF NOT EXISTS raw.telegram_messages (
        message_id BIGINT,
        message_date TIMESTAMP,
        text TEXT,
        views INTEGER,
        forwards INTEGER,
        has_media BOOLEAN,
        channel_name VARCHAR(100)
        PRIMARY KEY (channel_name, message_id)
        );
    """)

    conn.commit()

    print("Table 'raw.telegram_messages' is ready.")

    cursor.close()

def load_json_files(conn):
    data_folder = Path("data/raw/telegram_messages")

    cursor = conn.cursor()
    json_files = list(data_folder.rglob("*.json"))
    print(f"Found {len(json_files)} json files.")

    for json_file in json_files:
        channel_name = json_file.stem

        with open(json_file, "r", encoding="utf-8") as file:
            messages = json.load(file)
        print(f"Loading {len(messages)} messages from {channel_name}...")

        for message in messages:
            cursor.execute("""
                INSERT INTO raw.telegram_messages (
                    message_id,
                    message_date,
                    text,
                    views,
                    forwards,
                    has_media,
                    channel_name
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (channel_name, message_id) DO NOTHING
            """, (
                message["message_id"],
                message["date"],
                message["text"],
                message["views"],
                message["forwards"],
                message["has_media"],
                channel_name
            ))
    conn.commit()
    cursor.close()

    print("All JSON files loaded successfully!")

def main():
    conn = get_connection()
    print("Connected to PostgreSQL successfully!")

    create_schema(conn)
    create_table(conn)

    load_json_files(conn)

    conn.close()

if __name__ == "__main__":
    main()