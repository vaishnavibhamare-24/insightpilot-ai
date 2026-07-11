SELECT
    customer_id,
    SUM(order_amount) AS total_spend
FROM orders
GROUP BY customer_id
ORDER BY total_spend DESC
LIMIT 10;