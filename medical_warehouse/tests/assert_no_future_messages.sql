SELECT *
FROM {{ ref('fct_messages') }}
WHERE date_key >
    CAST(TO_CHAR(CURRENT_DATE, 'YYYYMMDD') AS INTEGER)