-- Total purchase revenue
SELECT
    SUM(revenue) AS total_revenue
FROM fact_events
WHERE event_type = 'purchase';


-- Product revenue ranking
SELECT
    product_name,
    SUM(revenue) AS total_revenue
FROM fact_events
WHERE event_type = 'purchase'
GROUP BY product_name
ORDER BY total_revenue DESC;


-- Purchase conversion rate
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN event_type = 'purchase' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS conversion_rate
FROM fact_events;


-- Purchase revenue by country
SELECT
    country,
    SUM(revenue) AS total_revenue
FROM fact_events
WHERE event_type = 'purchase'
GROUP BY country
ORDER BY total_revenue DESC;


-- Peak purchasing hours
SELECT
    event_hour,
    COUNT(*) AS purchase_count
FROM fact_events
WHERE event_type = 'purchase'
GROUP BY event_hour
ORDER BY purchase_count DESC;