from sqlalchemy import text

from api.database import engine


def get_top_products(limit: int):
    query = text("""
        SELECT
            LOWER(message_text) AS product,
            COUNT(*) AS mentions
        FROM analytics.fct_messages
        WHERE message_text IS NOT NULL
        GROUP BY LOWER(message_text)
        ORDER BY mentions DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        return conn.execute(query, {"limit": limit}).mappings().all()


def get_channel_activity(channel_name: str):
    query = text("""
        SELECT
            dc.channel_name,
            COUNT(*) AS total_posts,
            AVG(fm.view_count) AS average_views
        FROM analytics.fct_messages fm
        JOIN analytics.dim_channels dc
            ON fm.channel_key = dc.channel_key
        WHERE dc.channel_name = :channel
        GROUP BY dc.channel_name
    """)

    with engine.connect() as conn:
        return conn.execute(
            query,
            {"channel": channel_name}
        ).mappings().all()

def search_messages(keyword: str, limit: int):
    query = text("""
        SELECT
            fm.message_id,
            dc.channel_name,
            fm.message_text
        FROM analytics.fct_messages fm
        JOIN analytics.dim_channels dc
            ON fm.channel_key = dc.channel_key
        WHERE fm.message_text ILIKE :keyword
        LIMIT :limit
    """)

    with engine.connect() as conn:
        return conn.execute(
            query,
            {
                "keyword": f"%{keyword}%",
                "limit": limit,
            },
        ).mappings().all()


def get_visual_content():
    query = text("""
        SELECT
            channel_name,
            image_category,
            COUNT(*) AS total_images
        FROM raw.image_detections
        GROUP BY channel_name, image_category
        ORDER BY channel_name
    """)

    with engine.connect() as conn:
        return conn.execute(query).mappings().all()