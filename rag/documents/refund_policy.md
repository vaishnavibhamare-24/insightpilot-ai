# InsightPilot AI Refund Policy

## Refund Requirements

Every refund must reference a valid order.

A refund amount must be zero or greater.

An approved refund must not exceed the original order amount.

## Excess Refund Amount

If a refund exceeds the original order amount, the refund must be flagged for review.

The refund should not be automatically treated as a valid approved refund.

The transaction should be investigated for a data quality issue, processing error, or potentially incorrect refund amount.

## Approved Refunds

Approved refunds are included when calculating approved refund amounts and net revenue.

Net revenue is calculated by subtracting approved refund amounts from gross revenue.

## Refund Data Quality

Refund records with missing order identifiers should be treated as invalid.

Negative refund amounts should be flagged as data quality failures.

Refunds exceeding their associated order amount should be flagged for review.

## AI Guidance

When asked what should happen when a refund exceeds the order amount, InsightPilot AI should explain that the refund must be flagged for review because an approved refund should not exceed the original order amount.