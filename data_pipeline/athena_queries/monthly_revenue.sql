SELECT
    date_trunc('month', CAST(order_date AS DATE)) AS month,
    SUM(order_amount) AS total_revenue
FROM orders
GROUP BY 1
ORDER BY 1;