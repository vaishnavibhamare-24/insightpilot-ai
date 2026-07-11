SELECT
    customer_id,
    COUNT(order_id) AS total_orders,
    SUM(order_amount) AS lifetime_value
FROM orders
GROUP BY customer_id
ORDER BY lifetime_value DESC;