SELECT
    ROW_NUMBER() OVER (ORDER BY channel_name) AS channel_key,

    channel_name,

    CASE
        WHEN LOWER(channel_name) LIKE '%lobelia%' THEN 'Cosmetics'
        WHEN LOWER(channel_name) LIKE '%pharma%' THEN 'Pharmaceutical'
        WHEN LOWER(channel_name) LIKE '%chemed%' THEN 'Medical'
        ELSE 'Medical'
    END AS channel_type,

    MIN(message_date) AS first_post_date,

    MAX(message_date) AS last_post_date,

    COUNT(*) AS total_posts,

    ROUND(AVG(view_count), 2) AS avg_views

FROM {{ ref('stg_telegram_messages') }}

GROUP BY channel_name