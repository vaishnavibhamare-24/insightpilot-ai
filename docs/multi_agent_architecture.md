# InsightPilot Multi-Agent Architecture

## Purpose

InsightPilot uses LangGraph to route business questions to
specialized analytics, RAG, ML, and data-quality agents.

## Architecture

User Question
→ Router Agent
→ Specialized Agent Workflow
→ Summary Agent
→ Final Response

## Agents

- Router Agent
- SQL Agent
- RAG Agent
- ML Agent
- Data Quality Agent
- Visualization Agent
- Root Cause Agent
- Recommendation Agent
- Alert Agent
- Summary Agent

## Main Endpoint

POST /api/v1/chat

## Routing Examples

- "How is churn calculated?" → RAG Agent
- "Show monthly revenue" → SQL Agent
- "Predict churn for a customer" → ML Agent
- "What is the data quality score?" → Data Quality Agent
- "Create a revenue chart" → Visualization Agent
- "Why did revenue decrease?" → Root Cause Agent
- "Recommend actions to reduce churn" → Recommendation Agent

## Root Cause Workflow

Router Agent
→ SQL Agent
→ Root Cause Agent
→ Recommendation Agent
→ Summary Agent

## Visualization Workflow

Router Agent
→ SQL Agent
→ Visualization Agent
→ Summary Agent

## Alert Workflow

Router Agent
→ Data Quality Agent
→ Alert Agent
→ Summary Agent

## Safety Controls

- Read-only Athena query validation
- Limited SQL schema context
- Input validation
- Athena query timeout
- Maximum result count
- Agent error isolation
- No automatic SNS alerts in Phase 8
- AWS credentials are not logged
- Sensitive customer records are not logged

## Evaluation

The multi-agent system is evaluated using:

- Routing accuracy
- Correct agent selection
- Agent completion rate
- SQL execution success
- Citation presence
- Average latency
- Workflow error rate

## Limitations

The system can answer only from connected AWS services,
available datasets, machine-learning services, and the
Amazon Bedrock Knowledge Base.

The Data Quality Agent must use the latest Phase 4 quality
report service for production data-quality responses.

Natural-language churn requests currently require structured
feature extraction before numerical predictions can be made.

## Technology Stack

- LangGraph
- FastAPI
- Amazon Bedrock
- Amazon Bedrock Knowledge Bases
- Amazon Athena
- AWS Glue
- Amazon S3
- Amazon SageMaker
- Pydantic
- Pytest