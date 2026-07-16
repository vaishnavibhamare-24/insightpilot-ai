"use client";

import useSWR from "swr";

import { KpiCard } from "@/components/dashboard/kpi-card";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { apiRequest } from "@/lib/api-client";
import {
  formatCurrency,
  formatNumber,
} from "@/lib/formatters";
import type {
  DashboardMetricsResponse,
} from "@/types/dashboard";

const fallbackData: DashboardMetricsResponse = {
  kpis: [
    {
      name: "Total Revenue",
      value: 11874250,
      unit: "USD",
    },
    {
      name: "Total Orders",
      value: 5000,
      unit: null,
    },
    {
      name: "Average Order Value",
      value: 2374.85,
      unit: "USD",
    },
    {
      name: "Customers at Risk",
      value: 3358,
      unit: null,
    },
  ],
  source: "Development fallback data",
};

function displayKpiValue(
  name: string,
  value: string | number | null,
): string {
  if (
    name.toLowerCase().includes("revenue") ||
    name.toLowerCase().includes("order value")
  ) {
    return formatCurrency(value);
  }

  return formatNumber(value);
}

export default function DashboardPage() {
  const { data, error, isLoading, mutate } =
    useSWR<DashboardMetricsResponse>(
      "dashboard/metrics",
      apiRequest,
      {
        shouldRetryOnError: false,
        errorRetryCount: 0,
      },
    );

  if (isLoading) {
    return (
      <div className="flex min-h-80 items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  const dashboardData = data ?? fallbackData;
  const usingFallback = Boolean(error);

  return (
    <div className="space-y-8">
      <section>
        <div className="flex flex-wrap items-center gap-3">
          <h1 className="text-3xl font-bold text-slate-900">
            Executive Dashboard
          </h1>

          {usingFallback ? (
            <Badge variant="warning">
              Development fallback
            </Badge>
          ) : (
            <Badge variant="success">
              Live data
            </Badge>
          )}
        </div>

        <p className="mt-2 text-slate-500">
          A unified view of commerce, customer, and
          operational performance.
        </p>
      </section>

      {usingFallback ? (
        <Card className="border-amber-200 bg-amber-50">
          <h2 className="font-semibold text-amber-900">
            Live dashboard data is temporarily unavailable
          </h2>

          <p className="mt-2 text-sm text-amber-800">
            InsightPilot is displaying development fallback
            metrics while the AWS-backed dashboard endpoint is
            unavailable.
          </p>

          <button
            className="mt-4 rounded-lg bg-slate-900 px-4 py-2 text-sm text-white"
            onClick={() => mutate()}
          >
            Retry live data
          </button>
        </Card>
      ) : null}

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {dashboardData.kpis.map((kpi) => (
          <KpiCard
            key={kpi.name}
            name={kpi.name}
            value={displayKpiValue(
              kpi.name,
              kpi.value,
            )}
            unit={
              kpi.unit === "USD"
                ? null
                : kpi.unit
            }
          />
        ))}
      </section>

      <Card>
        <h2 className="text-lg font-semibold">
          Data source
        </h2>

        <p className="mt-2 text-sm text-slate-500">
          {dashboardData.source}
        </p>
      </Card>
    </div>
  );
}