# InsightPilot AI

An end-to-end AI-powered customer analytics platform built on AWS that combines data engineering, machine learning, generative AI, and real-time streaming.

---

## Project Overview

InsightPilot AI helps businesses analyze customer behavior, predict churn, answer business questions using natural language, and monitor real-time customer events.

The project demonstrates a production-style AI system using AWS cloud services, FastAPI, Next.js, machine learning, Retrieval-Augmented Generation (RAG), and streaming analytics.

---

## Features

- Customer churn prediction using XGBoost
- AI-powered business assistant using Amazon Bedrock
- Retrieval-Augmented Generation (RAG)
- Real-time event streaming using Amazon Kinesis
- Automated ETL using AWS Glue
- SQL analytics using Amazon Athena
- FastAPI backend APIs
- Next.js frontend dashboard
- Data quality validation
- CloudWatch monitoring
- SageMaker model integration

---

## Tech Stack

### Languages

- Python
- SQL
- TypeScript

### Backend

- FastAPI
- Pydantic
- LangChain
- LangGraph

### Machine Learning

- Scikit-Learn
- XGBoost
- SageMaker

### Generative AI

- Amazon Bedrock
- Claude
- RAG
- LangChain

### Frontend

- Next.js
- React
- Tailwind CSS

### AWS

- Amazon S3
- AWS Glue
- Athena
- Bedrock
- SageMaker
- Lambda
- Kinesis
- CloudWatch
- IAM

---

## Architecture

(Add the architecture diagram here)

---

## Project Workflow

Raw Data

↓

Amazon S3

↓

Glue Crawlers

↓

Glue ETL

↓

Processed S3

↓

Athena

↓

FastAPI APIs

↓

Machine Learning + Bedrock RAG

↓

Next.js Dashboard

---

## APIs

- Analytics API
- Churn Prediction API
- RAG Chat API
- Streaming API
- Health API

---

## Machine Learning

Model:
XGBoost

Prediction:
Customer Churn

Features

- Lifetime Revenue
- Purchase Frequency
- Average Order Value
- Customer Lifetime
- Days Since Last Order

---

## AI Assistant

The AI assistant uses Amazon Bedrock Knowledge Base and Retrieval-Augmented Generation to answer business questions using company documentation.

---

## Future Improvements

- Docker deployment
- CI/CD pipeline
- ECS deployment
- Cognito authentication
- Auto scaling

---

## Author

Vaishnavi Bhamare

MS Advanced Data Analytics

University of North Texas
