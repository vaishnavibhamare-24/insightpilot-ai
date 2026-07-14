# InsightPilot AI Churn Model Guide

## Purpose

The churn model predicts the probability that a customer is at risk of churning.

The prediction helps the business identify customers who may require retention campaigns.

## Churn Model Features

The churn model uses the following features:

- Days since last order.
- Total spend.
- Number of orders.
- Average order value.
- Refund count.
- Refund amount.
- Support ticket count.
- Website visits.
- Purchase events.
- Customer tenure days.

These features represent customer purchasing behavior, financial activity, support interactions, website engagement, and customer history.

## Churn Probability

The model returns a churn probability between 0 and 1.

A higher probability represents a higher predicted churn risk.

## Churn Risk Thresholds

Churn risk is classified using the following thresholds:

- Low risk: churn probability below 0.40.
- Medium risk: churn probability from 0.40 through 0.69.
- High risk: churn probability of 0.70 or greater.

## Churn Label

The churn label is a binary value.

Allowed values are:

- 0 means the customer is active.
- 1 means the customer is churned.

## Business Usage

High-risk customers may be prioritized for retention campaigns.

The churn prediction should support business decisions and should not be treated as a guaranteed future outcome.

## AI Guidance

When asked which features are used by the churn model, InsightPilot AI should retrieve the churn model features from this document.

When asked about churn risk thresholds, InsightPilot AI should use the Low, Medium, and High risk thresholds defined in this guide.