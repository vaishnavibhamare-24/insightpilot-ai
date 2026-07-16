"use client";

import { FormEvent, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Textarea } from "@/components/ui/textarea";
import { apiRequest } from "@/lib/api-client";

interface SqlQueryResponse {
  status?: string;
  row_count?: number;
  data_scanned_bytes?: number;
  columns?: string[];
  rows?: Array<Record<string, unknown>>;
  error?: string | null;
  execution_time_ms?: number | null;
}

export default function SqlPage() {
  const [query, setQuery] = useState(
    "SELECT * FROM fact_orders LIMIT 10",
  );

  const [result, setResult] =
    useState<SqlQueryResponse | null>(null);

  const [error, setError] =
    useState<string | null>(null);

  const [isLoading, setIsLoading] =
    useState(false);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const trimmedQuery = query.trim();

    if (!trimmedQuery) {
      setError("Enter a SQL query before running it.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response =
        await apiRequest<SqlQueryResponse>(
          "analytics/query",
          {
            method: "POST",
            body: JSON.stringify({
              query: trimmedQuery,
              timeout_seconds: 30,
              max_results: 500,
            }),
          },
        );

      setResult(response);
    } catch (requestError) {
      const message =
        requestError instanceof Error
          ? requestError.message
          : "The SQL query failed.";

      setError(message);
    } finally {
      setIsLoading(false);
    }
  }

  const columns =
    result?.columns ??
    (
      result?.rows?.length
        ? Object.keys(result.rows[0])
        : []
    );

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-bold text-slate-900">
          SQL Explorer
        </h1>

        <p className="mt-2 text-slate-500">
          Run read-only Athena queries against the
          InsightPilot analytics layer.
        </p>
      </section>

      <Card>
        <form
          className="space-y-4"
          onSubmit={handleSubmit}
        >
          <div>
            <label
              htmlFor="sql-query"
              className="mb-2 block text-sm font-medium text-slate-700"
            >
              SQL query
            </label>

            <Textarea
              id="sql-query"
              value={query}
              onChange={(event) =>
                setQuery(event.target.value)
              }
              rows={10}
              className="font-mono"
              disabled={isLoading}
            />
          </div>

          <Button
            type="submit"
            disabled={isLoading}
          >
            {isLoading
              ? "Running query..."
              : "Run query"}
          </Button>
        </form>
      </Card>

      {isLoading ? (
        <Card>
          <div className="flex items-center gap-3">
            <LoadingSpinner />

            <p className="text-sm text-slate-600">
              Athena is executing your query.
            </p>
          </div>
        </Card>
      ) : null}

      {error ? (
        <Card className="border-red-200 bg-red-50">
          <h2 className="font-semibold text-red-800">
            Query failed
          </h2>

          <p className="mt-2 text-sm text-red-700">
            {error}
          </p>
        </Card>
      ) : null}

      {result ? (
        <>
          <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <Card>
              <p className="text-sm text-slate-500">
                Status
              </p>

              <p className="mt-2 text-xl font-semibold">
                {result.status ?? "Unknown"}
              </p>
            </Card>

            <Card>
              <p className="text-sm text-slate-500">
                Row count
              </p>

              <p className="mt-2 text-xl font-semibold">
                {result.row_count ??
                  result.rows?.length ??
                  0}
              </p>
            </Card>

            <Card>
              <p className="text-sm text-slate-500">
                Data scanned
              </p>

              <p className="mt-2 text-xl font-semibold">
                {result.data_scanned_bytes
                  ? `${(
                      result.data_scanned_bytes /
                      1024 /
                      1024
                    ).toFixed(2)} MB`
                  : "0 MB"}
              </p>
            </Card>

            <Card>
              <p className="text-sm text-slate-500">
                Execution time
              </p>

              <p className="mt-2 text-xl font-semibold">
                {result.execution_time_ms
                  ? `${Math.round(
                      result.execution_time_ms,
                    )} ms`
                  : "Unavailable"}
              </p>
            </Card>
          </section>

          {result.error ? (
            <Card className="border-red-200 bg-red-50">
              <p className="text-sm text-red-700">
                {result.error}
              </p>
            </Card>
          ) : null}

          <Card>
            <h2 className="text-lg font-semibold text-slate-900">
              Query results
            </h2>

            {result.rows?.length ? (
              <div className="mt-4 overflow-x-auto">
                <table className="min-w-full border-collapse text-left text-sm">
                  <thead>
                    <tr className="border-b border-slate-200">
                      {columns.map((column) => (
                        <th
                          key={column}
                          className="px-4 py-3 font-semibold text-slate-700"
                        >
                          {column}
                        </th>
                      ))}
                    </tr>
                  </thead>

                  <tbody>
                    {result.rows.map(
                      (row, rowIndex) => (
                        <tr
                          key={rowIndex}
                          className="border-b border-slate-100"
                        >
                          {columns.map((column) => (
                            <td
                              key={`${rowIndex}-${column}`}
                              className="whitespace-nowrap px-4 py-3 text-slate-600"
                            >
                              {String(
                                row[column] ?? "",
                              )}
                            </td>
                          ))}
                        </tr>
                      ),
                    )}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="mt-4 text-sm text-slate-500">
                The query returned no rows.
              </p>
            )}
          </Card>
        </>
      ) : null}
    </div>
  );
}