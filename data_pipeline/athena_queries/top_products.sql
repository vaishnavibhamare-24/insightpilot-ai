SELECT
    product_id,
    COUNT(*) AS total_orders
FROM orders
GROUP BY product_id
ORDER BY total_orders DESC
LIMIT 10;