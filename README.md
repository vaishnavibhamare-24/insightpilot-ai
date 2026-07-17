<div align="center">

# InsightPilot AI

### End-to-End AI-Powered Customer Analytics Platform on AWS

*Data Engineering · Machine Learning · Generative AI · Real-Time Streaming*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=flat-square&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-Frontend-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=flat-square)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#)

</div>

---

## 📌 Overview

**InsightPilot AI** helps businesses analyze customer behavior, predict churn, answer natural-language business questions, and monitor real-time customer events — all in one production-style platform.

The project demonstrates a full AI system built on AWS cloud infrastructure, combining **FastAPI**, **Next.js**, **machine learning**, **Retrieval-Augmented Generation (RAG)**, and **streaming analytics** into a single cohesive pipeline.

---

## ✨ Features

| Capability | Description |
|---|---|
| 📉 **Churn Prediction** | XGBoost model forecasts customer churn risk |
| 🤖 **AI Business Assistant** | Natural-language Q&A powered by Amazon Bedrock |
| 🔍 **RAG Pipeline** | Retrieval-Augmented Generation over company documentation |
| ⚡ **Real-Time Streaming** | Live customer event ingestion via Amazon Kinesis |
| 🔄 **Automated ETL** | AWS Glue jobs handle transformation at scale |
| 🗃️ **SQL Analytics** | Serverless querying via Amazon Athena |
| 🚀 **FastAPI Backend** | High-performance REST APIs |
| 🖥️ **Next.js Dashboard** | Modern, responsive frontend |
| ✅ **Data Quality Validation** | Automated checks across the pipeline |
| 📊 **CloudWatch Monitoring** | Full observability into system health |
| 🧬 **SageMaker Integration** | Managed model training and deployment |

---

## 🏗️ Architecture

<div align="center">
<img width="800" alt="InsightPilot AI Architecture" src="https://github.com/user-attachments/assets/b65c6b9b-7a6d-4dcc-8e83-c8fd288fb7e5" />
</div>

---

## 🔄 Project Workflow

```mermaid
flowchart TD
    A[Raw Data] --> B[Amazon S3]
    B --> C[Glue Crawlers]
    C --> D[Glue ETL]
    D --> E[Processed S3]
    E --> F[Athena]
    F --> G[FastAPI APIs]
    G --> H[ML + Bedrock RAG]
    H --> I[Next.js Dashboard]
```

---

## 🧰 Tech Stack

<table>
<tr>
<td valign="top" width="33%">

**Languages**
- Python
- SQL
- TypeScript

**Backend**
- FastAPI
- Pydantic
- LangChain
- LangGraph

</td>
<td valign="top" width="33%">

**Machine Learning**
- Scikit-Learn
- XGBoost
- SageMaker

**Generative AI**
- Amazon Bedrock
- Claude
- RAG
- LangChain

</td>
<td valign="top" width="33%">

**Frontend**
- Next.js
- React
- Tailwind CSS

**AWS**
- S3 · Glue · Athena
- Bedrock · SageMaker
- Lambda · Kinesis
- CloudWatch · IAM

</td>
</tr>
</table>

---

## 🔌 APIs

| Endpoint Group | Purpose |
|---|---|
| `Analytics API` | Aggregated customer and business metrics |
| `Churn Prediction API` | Real-time churn scoring |
| `RAG Chat API` | Natural-language business Q&A |
| `Streaming API` | Live event ingestion and monitoring |
| `Health API` | Service health checks |

---

## 🤖 Machine Learning

**Model:** XGBoost
**Prediction Target:** Customer Churn

**Features used:**
- Lifetime Revenue
- Purchase Frequency
- Average Order Value
- Customer Lifetime
- Days Since Last Order

---

## 💬 AI Assistant

The AI assistant uses an **Amazon Bedrock Knowledge Base** with **Retrieval-Augmented Generation** to answer business questions grounded in company documentation — no hallucinated answers, just retrieval-backed responses.

---

## 🛣️ Roadmap

- [ ] Docker deployment
- [ ] CI/CD pipeline
- [ ] ECS deployment
- [ ] Cognito authentication
- [ ] Auto scaling

---

## 👩‍💻 Author

**Vaishnavi Bhamare**
MS Advanced Data Analytics · University of North Texas

[![Email](https://img.shields.io/badge/Email-vaishnavibhamare24%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:vaishnavibhamare24@gmail.com)
