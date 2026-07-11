SELECT
    stm.message_id,

    dc.channel_key,

    CAST(TO_CHAR(stm.message_date, 'YYYYMMDD') AS INTEGER) AS date_key,

    stm.message_text,

    stm.message_length,

    stm.view_count,

    stm.forward_count,

    stm.has_image

FROM {{ ref('stg_telegram_messages') }} AS stm

JOIN {{ ref('dim_channels') }} AS dc
    ON stm.channel_name = dc.channel_name