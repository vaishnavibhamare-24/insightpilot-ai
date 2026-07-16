"use client";

import { useState } from "react";
import useSWR from "swr";

import { LineChartCard } from "@/components/charts/line-chart-card";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { apiRequest } from "@/lib/api-client";
import { formatCurrency } from "@/lib/formatters";

interface RevenueForecastPoint {
  month: string;
  predicted_revenue: number;
}

interface RevenueForecastResponse {
  model_name?: string;
  forecast_horizon?: number;
  forecast?: RevenueForecastPoint[];
  predictions?: RevenueForecastPoint[];
  latency_ms?: number | null;
}

export default function ForecastPage() {
  const [months, setMonths] = useState(6);

  const { data, error, isLoading, mutate } =
    useSWR<RevenueForecastResponse>(
      `forecast/revenue?months=${months}`,
      apiRequest,
    );

  const forecastData: RevenueForecastPoint[] =
    data?.forecast ??
    data?.predictions ??
    [];

  const chartData: Record<string, unknown>[] =
    forecastData.map((item) => ({
      month: item.month,
      predicted_revenue: item.predicted_revenue,
    }));

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-bold text-slate-900">
          Revenue Forecast
        </h1>

        <p className="mt-2 text-slate-500">
          View projected monthly revenue for the selected
          forecast horizon.
        </p>
      </section>

      <Card>
        <div className="max-w-xs">
          <label
            htmlFor="forecast-months"
            className="mb-2 block text-sm font-medium text-slate-700"
          >
            Forecast months
          </label>

          <Input
            id="forecast-months"
            type="number"
            min={1}
            max={24}
            value={months}
            onChange={(event) => {
              const value = Number(event.target.value);

              if (value >= 1 && value <= 24) {
                setMonths(value);
              }
            }}
          />
        </div>
      </Card>

      {isLoading ? (
        <Card>
          <div className="flex items-center gap-3">
            <LoadingSpinner />

            <p className="text-sm text-slate-600">
              Loading revenue forecast.
            </p>
          </div>
        </Card>
      ) : null}

      {error ? (
        <Card className="border-red-200 bg-red-50">
          <h2 className="font-semibold text-red-800">
            Forecast unavailable
          </h2>

          <p className="mt-2 text-sm text-red-700">
            {error.message}
          </p>

          <button
            className="mt-4 rounded-lg bg-slate-900 px-4 py-2 text-sm text-white"
            onClick={() => mutate()}
          >
            Try again
          </button>
        </Card>
      ) : null}

      {data ? (
        <>
          <section className="grid gap-4 md:grid-cols-2">
            <Card>
              <p className="text-sm text-slate-500">
                Model name
              </p>

              <p className="mt-3 text-xl font-semibold">
                {data.model_name ?? "Unavailable"}
              </p>
            </Card>

            <Card>
              <p className="text-sm text-slate-500">
                Forecast horizon
              </p>

              <p className="mt-3 text-xl font-semibold">
                {data.forecast_horizon ?? months} months
              </p>
            </Card>
          </section>

          {forecastData.length > 0 ? (
            <>
              <LineChartCard
                title="Monthly Revenue Forecast"
                data={chartData}
                xField="month"
                yField="predicted_revenue"
              />

              <Card>
                <h2 className="text-lg font-semibold text-slate-900">
                  Forecast details
                </h2>

                <div className="mt-4 overflow-x-auto">
                  <table className="min-w-full border-collapse text-left text-sm">
                    <thead>
                      <tr className="border-b border-slate-200">
                        <th className="px-4 py-3 font-semibold text-slate-700">
                          Month
                        </th>

                        <th className="px-4 py-3 font-semibold text-slate-700">
                          Predicted revenue
                        </th>
                      </tr>
                    </thead>

                    <tbody>
                      {forecastData.map((item) => (
                        <tr
                          key={item.month}
                          className="border-b border-slate-100"
                        >
                          <td className="px-4 py-3 text-slate-600">
                            {item.month}
                          </td>

                          <td className="px-4 py-3 text-slate-600">
                            {formatCurrency(
                              item.predicted_revenue,
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>
            </>
          ) : (
            <Card>
              <p className="text-sm text-slate-500">
                No forecast data was returned.
              </p>
            </Card>
          )}
        </>
      ) : null}
    </div>
  );
}