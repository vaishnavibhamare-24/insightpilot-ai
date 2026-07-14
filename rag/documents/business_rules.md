# InsightPilot AI Business Rules

## Customer Churn

A customer is considered churned when the customer has not placed an order within the defined churn inactivity period.

The churn label must contain one of two values:

- 0 means the customer is active.
- 1 means the customer is churned.

Churn predictions are used to identify customers who may require retention campaigns.

## Orders

Every order must be associated with a valid customer.

Order amounts must be non-negative.

Cancelled orders should not be included in qualifying revenue calculations.

## Revenue

Revenue metrics must use qualifying completed orders.

Gross revenue represents the total revenue generated from qualifying orders.

Average order value is calculated using qualifying revenue and qualifying orders.

## Refunds

Every refund must reference a valid order.

An approved refund should not exceed the original order amount.

If a refund exceeds the original order amount, the refund must be flagged for review.

Refund amounts must not be negative.

## Data Quality

Customer identifiers must not be null.

The churn label must be either 0 or 1.

Critical data quality failures should be reported and investigated before downstream analytics or machine learning processes use the affected data.

## AI Response Rules

InsightPilot AI must answer business questions using information available in the enterprise knowledge base.

If the requested information is not available in the knowledge base, the system should state that the information is not available.

The system must not invent confidential, personal, or unsupported business information.