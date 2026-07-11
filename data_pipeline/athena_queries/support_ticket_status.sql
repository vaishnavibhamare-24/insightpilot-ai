SELECT
    status,
    COUNT(*) AS total
FROM support_tickets
GROUP BY status
ORDER BY total DESC;