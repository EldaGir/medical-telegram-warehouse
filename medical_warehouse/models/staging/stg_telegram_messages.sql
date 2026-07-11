SELECT
    message_id,
    channel_name,

    message_date::timestamp AS message_date,

    text AS message_text,

    views::integer AS view_count,

    forwards::integer AS forward_count,

    has_media AS has_image,

    LENGTH(text) AS message_length

FROM raw.telegram_messages

WHERE text IS NOT NULL
  AND TRIM(text) <> ''