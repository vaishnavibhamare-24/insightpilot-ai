import { Card } from "@/components/ui/card";

const layers = [
  {
    title: "Experience Layer",
    items: [
      "Next.js Dashboard",
      "AI Copilot",
      "SQL Explorer",
      "Churn Prediction",
      "Revenue Forecast",
    ],
  },
  {
    title: "API Layer",
    items: [
      "Next.js Server Proxy",
      "FastAPI REST APIs",
      "X-API-Key Authentication",
      "Request Validation",
      "Error Handling",
    ],
  },
  {
    title: "Intelligence Layer",
    items: [
      "LangGraph Router",
      "Athena SQL Agent",
      "Bedrock RAG Agent",
      "SageMaker ML Agent",
      "Data Quality Agent",
    ],
  },
  {
    title: "Data Layer",
    items: [
      "Amazon S3",
      "AWS Glue",
      "Amazon Athena",
      "Processed Analytics Tables",
      "Knowledge Base Documents",
    ],
  },
];

export default function ArchitecturePage() {
  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-3xl font-bold text-slate-900">
          Platform Architecture
        </h1>

        <p className="mt-2 text-slate-500">
          InsightPilot combines a secure web application,
          FastAPI services, agentic AI, machine learning, and
          AWS data infrastructure.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {layers.map((layer) => (
          <Card key={layer.title}>
            <h2 className="text-lg font-semibold text-slate-900">
              {layer.title}
            </h2>

            <ul className="mt-4 space-y-3 text-sm text-slate-600">
              {layer.items.map((item) => (
                <li
                  key={item}
                  className="rounded-lg bg-slate-50 px-3 py-2"
                >
                  {item}
                </li>
              ))}
            </ul>
          </Card>
        ))}
      </section>

      <Card>
        <h2 className="text-xl font-semibold text-slate-900">
          Request Flow
        </h2>

        <div className="mt-6 overflow-x-auto">
          <pre className="min-w-[700px] rounded-2xl bg-slate-950 p-6 text-sm leading-7 text-slate-100">
            <code>{`User
  ↓
Next.js Frontend
  ↓
Next.js Server-Side Proxy
  ↓
FastAPI Backend
  ↓
LangGraph Router
  ├── Athena SQL Agent
  ├── Bedrock RAG Agent
  ├── SageMaker ML Agent
  └── Data Quality Agent
  ↓
Summary, Visualization, and Recommendations`}</code>
          </pre>
        </div>
      </Card>

      <Card>
        <h2 className="text-xl font-semibold text-slate-900">
          Security Flow
        </h2>

        <div className="mt-4 space-y-3 text-sm leading-6 text-slate-600">
          <p>
            The browser sends requests only to the Next.js
            server-side proxy.
          </p>

          <p>
            The proxy reads the private backend API key from a
            server-only environment variable.
          </p>

          <p>
            The proxy adds the key as the X-API-Key header
            before forwarding the request to FastAPI.
          </p>

          <p>
            The browser never receives or stores the backend
            API key.
          </p>
        </div>
      </Card>
    </div>
  );
}