SELECT
    event_type,
    COUNT(*) AS total_events
FROM website_events
GROUP BY event_type
ORDER BY total_events DESC;