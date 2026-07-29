import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cursor = conn.cursor()

df = pd.read_csv("data/processed/yolo_detections.csv")

print(f"Loading {len(df)} detection records...")

for _, row in df.iterrows():

    cursor.execute(
        """
        INSERT INTO raw.image_detections
        (
            message_id,
            channel_name,
            detected_class,
            confidence_score,
            image_category
        )
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            int(row["message_id"]),
            row["channel_name"],
            str(row["detected_class"]),
            float(row["confidence_score"]),
            row["image_category"],
        ),
    )

conn.commit()

cursor.close()
conn.close()

print("YOLO detections loaded successfully!")