"use client";

import { FormEvent, useState } from "react";

import { BarChartCard } from "@/components/charts/bar-chart-card";
import { LineChartCard } from "@/components/charts/line-chart-card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Textarea } from "@/components/ui/textarea";
import { apiRequest } from "@/lib/api-client";
import type {
  ChatRequest,
  ChatResponse,
} from "@/types/chat";

export default function ChatPage() {
  const [message, setMessage] = useState("");
  const [sessionId, setSessionId] =
    useState<string | null>(null);

  const [response, setResponse] =
    useState<ChatResponse | null>(null);

  const [error, setError] =
    useState<string | null>(null);

  const [isLoading, setIsLoading] =
    useState(false);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage) {
      setError("Enter a question before submitting.");
      return;
    }

    setIsLoading(true);
    setError(null);

    const requestBody: ChatRequest = {
      message: trimmedMessage,
      session_id: sessionId,
    };

    try {
      const result = await apiRequest<ChatResponse>(
        "chat",
        {
          method: "POST",
          body: JSON.stringify(requestBody),
        },
      );

      setResponse(result);
      setSessionId(result.session_id);
    } catch (requestError) {
      const errorMessage =
        requestError instanceof Error
          ? requestError.message
          : "The AI Copilot request failed.";

      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }

  const visualization = response?.visualization;

  const canDisplayChart =
    visualization?.data &&
    visualization.data.length > 0 &&
    visualization.x_field &&
    visualization.y_field;

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-bold text-slate-900">
          AI Copilot
        </h1>

        <p className="mt-2 text-slate-500">
          Ask questions about revenue, customers, churn,
          operations, or data quality.
        </p>
      </section>

      <Card>
        <form
          className="space-y-4"
          onSubmit={handleSubmit}
        >
          <div>
            <label
              htmlFor="copilot-message"
              className="mb-2 block text-sm font-medium text-slate-700"
            >
              Business question
            </label>

            <Textarea
              id="copilot-message"
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              rows={5}
              placeholder="Example: Why did revenue decrease?"
              disabled={isLoading}
            />
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Button
              type="submit"
              disabled={isLoading}
            >
              {isLoading
                ? "Analyzing..."
                : "Ask InsightPilot"}
            </Button>

            {sessionId ? (
              <p className="text-xs text-slate-500">
                Conversation session active
              </p>
            ) : null}
          </div>
        </form>
      </Card>

      {isLoading ? (
        <Card>
          <div className="flex items-center gap-3">
            <LoadingSpinner />

            <p className="text-sm text-slate-600">
              InsightPilot agents are analyzing your
              question.
            </p>
          </div>
        </Card>
      ) : null}

      {error ? (
        <Card className="border-red-200 bg-red-50">
          <h2 className="font-semibold text-red-800">
            Copilot request failed
          </h2>

          <p className="mt-2 text-sm text-red-700">
            {error}
          </p>
        </Card>
      ) : null}

      {response ? (
        <>
          <Card>
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <h2 className="text-xl font-semibold text-slate-900">
                  Answer
                </h2>

                <p className="mt-4 whitespace-pre-wrap text-sm leading-7 text-slate-700">
                  {response.answer}
                </p>
              </div>

              {response.route ? (
                <Badge>{response.route}</Badge>
              ) : null}
            </div>

            {response.route_reason ? (
              <p className="mt-4 text-sm text-slate-500">
                Route reason: {response.route_reason}
              </p>
            ) : null}

            <div className="mt-5 flex flex-wrap gap-2">
              {response.agents_used?.map((agent) => (
                <Badge
                  key={agent}
                  variant="success"
                >
                  {agent}
                </Badge>
              ))}
            </div>

            <div className="mt-5 grid gap-3 text-sm text-slate-500 sm:grid-cols-2">
              <p>
                Latency:{" "}
                {Math.round(response.latency_ms)} ms
              </p>

              {response.confidence !== null &&
              response.confidence !== undefined ? (
                <p>
                  Confidence:{" "}
                  {(response.confidence * 100).toFixed(1)}
                  %
                </p>
              ) : null}
            </div>
          </Card>

          {response.generated_sql ? (
            <Card>
              <h2 className="text-lg font-semibold text-slate-900">
                Generated SQL
              </h2>

              <pre className="mt-4 overflow-x-auto rounded-xl bg-slate-950 p-4 text-sm text-slate-100">
                <code>{response.generated_sql}</code>
              </pre>
            </Card>
          ) : null}

          {canDisplayChart &&
          visualization?.chart_type === "bar" ? (
            <BarChartCard
              title={
                visualization.title ??
                "AI-generated visualization"
              }
              data={visualization.data ?? []}
              xField={visualization.x_field ?? ""}
              yField={visualization.y_field ?? ""}
            />
          ) : null}

          {canDisplayChart &&
          visualization?.chart_type !== "bar" ? (
            <LineChartCard
              title={
                visualization?.title ??
                "AI-generated visualization"
              }
              data={visualization?.data ?? []}
              xField={visualization?.x_field ?? ""}
              yField={visualization?.y_field ?? ""}
            />
          ) : null}

          {response.citations?.length > 0 ? (
            <Card>
              <h2 className="text-lg font-semibold text-slate-900">
                Citations
              </h2>

              <div className="mt-4 space-y-4">
                {response.citations.map(
                  (citation, index) => (
                    <div
                      key={`${citation.source_uri}-${index}`}
                      className="rounded-xl border border-slate-200 p-4"
                    >
                      <p className="text-sm font-medium text-slate-800">
                        {citation.document_name ??
                          `Source ${index + 1}`}
                      </p>

                      {citation.text ? (
                        <p className="mt-2 text-sm text-slate-600">
                          {citation.text}
                        </p>
                      ) : null}

                      {citation.source_uri ? (
                        <p className="mt-2 break-all text-xs text-slate-500">
                          {citation.source_uri}
                        </p>
                      ) : null}
                    </div>
                  ),
                )}
              </div>
            </Card>
          ) : null}

          {response.recommendations?.length > 0 ? (
            <Card>
              <h2 className="text-lg font-semibold text-slate-900">
                Recommendations
              </h2>

              <ul className="mt-4 space-y-2 text-sm text-slate-700">
                {response.recommendations.map(
                  (recommendation, index) => (
                    <li
                      key={`${recommendation}-${index}`}
                      className="rounded-lg bg-slate-50 p-3"
                    >
                      {recommendation}
                    </li>
                  ),
                )}
              </ul>
            </Card>
          ) : null}

          {response.errors?.length > 0 ? (
            <Card className="border-amber-200 bg-amber-50">
              <h2 className="font-semibold text-amber-800">
                Agent warnings
              </h2>

              <ul className="mt-3 space-y-2 text-sm text-amber-700">
                {response.errors.map(
                  (responseError, index) => (
                    <li key={`${responseError}-${index}`}>
                      {responseError}
                    </li>
                  ),
                )}
              </ul>
            </Card>
          ) : null}
        </>
      ) : null}
    </div>
  );
}