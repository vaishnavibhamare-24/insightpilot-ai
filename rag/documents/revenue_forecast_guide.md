# InsightPilot AI Revenue Forecast Guide

## Purpose

The revenue forecasting model predicts future revenue using historical monthly revenue patterns.

The forecast helps support business planning, trend analysis, and revenue monitoring.

## Revenue Forecasting Data

The model uses historical monthly revenue data.

Important forecasting information includes:

- Revenue month.
- Gross revenue.
- Monthly order count.
- Monthly customer count.
- Average order value.
- Units sold.

## Time-Based Train-Test Split

A random train-test split is not used for revenue forecasting.

Random splitting can leak future information into the training dataset.

Instead, older months are used for model training and newer months are used for model testing.

This preserves the chronological order of the revenue data and provides a more realistic evaluation of future forecasting performance.

## Future Information Leakage

Future information must not be available to the model during training.

Using future revenue observations to predict earlier periods would create data leakage and produce misleading evaluation results.

## Forecast Usage

Revenue forecasts may support:

- Business planning.
- Revenue trend analysis.
- Capacity planning.
- Performance monitoring.
- Dashboard reporting.

Forecast values are predictions and should not be interpreted as guaranteed future revenue.

## AI Guidance

When asked why a random train-test split is not used for revenue forecasting, InsightPilot AI should explain that random splitting can leak future information.

Older months are used for training and newer months are used for testing.