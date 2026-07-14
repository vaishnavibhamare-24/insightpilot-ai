# InsightPilot AI Data Quality Guide

## Purpose

Data quality checks ensure that business analytics and machine learning systems use valid and reliable data.

Critical data quality failures should be investigated before affected data is used by downstream systems.

## Customer Data Quality

Customer identifiers must not be null.

Each customer should have a valid customer identifier.

Duplicate or invalid customer records should be investigated.

## Churn Label Validation

The churn label must contain one of two allowed values:

- 0 means the customer is active.
- 1 means the customer is churned.

Any churn label other than 0 or 1 is invalid and should be flagged as a data quality failure.

## Order Data Quality

Every order must reference a valid customer.

Order amounts must not be negative.

Invalid or missing customer references should be investigated.

## Refund Data Quality

Every refund must reference a valid order.

Refund amounts must not be negative.

An approved refund should not exceed the original order amount.

Refunds exceeding the associated order amount must be flagged for review.

## Missing Values

Critical identifiers and required labels must not contain missing values.

Missing critical values should be reported as data quality failures.

## Data Quality Monitoring

InsightPilot AI uses data quality checks to monitor processed datasets.

Data quality results may be published to monitoring systems and used to trigger alerts when critical checks fail.

## AI Guidance

When asked what values are allowed for the churn label, InsightPilot AI should state that the churn label must be either 0 or 1.