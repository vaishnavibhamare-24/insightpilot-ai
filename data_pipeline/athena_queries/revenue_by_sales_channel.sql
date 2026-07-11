SELECT
    sales_channel,
    SUM(order_amount) AS revenue
FROM orders
GROUP BY sales_channel
ORDER BY revenue DESC;