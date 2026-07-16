"use client";

import {
  ChangeEvent,
  FormEvent,
  useState,
} from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { apiRequest } from "@/lib/api-client";
import {
  formatMilliseconds,
  formatPercentage,
} from "@/lib/formatters";
import type {
  ChurnPredictionRequest,
  ChurnPredictionResponse,
} from "@/types/prediction";

const initialForm: ChurnPredictionRequest = {
  total_orders: 5,
  lifetime_revenue: 2500,
  average_order_value: 500,
  days_since_last_order: 90,
  customer_lifetime_days: 365,
  purchase_frequency: 0.02,
  estimated_clv: 3000,
};

export default function ChurnPage() {
  const [form, setForm] =
    useState<ChurnPredictionRequest>(initialForm);

  const [result, setResult] =
    useState<ChurnPredictionResponse | null>(null);

  const [error, setError] =
    useState<string | null>(null);

  const [isLoading, setIsLoading] =
    useState(false);

  function handleChange(
    event: ChangeEvent<HTMLInputElement>,
  ) {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: Number(value),
    }));
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response =
        await apiRequest<ChurnPredictionResponse>(
          "predictions/churn",
          {
            method: "POST",
            body: JSON.stringify(form),
          },
        );

      setResult(response);
    } catch (requestError) {
      const message =
        requestError instanceof Error
          ? requestError.message
          : "The churn prediction request failed.";

      setError(message);
    } finally {
      setIsLoading(false);
    }
  }

  const riskVariant =
    result?.risk_level?.toLowerCase() === "high"
      ? "danger"
      : result?.risk_level?.toLowerCase() ===
          "medium"
        ? "warning"
        : "success";

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-bold text-slate-900">
          Churn Prediction
        </h1>

        <p className="mt-2 text-slate-500">
          Estimate customer churn risk using the trained
          InsightPilot machine-learning model.
        </p>
      </section>

      <Card>
        <form
          className="grid gap-5 md:grid-cols-2"
          onSubmit={handleSubmit}
        >
          {Object.entries(form).map(
            ([field, value]) => (
              <div key={field}>
                <label
                  htmlFor={field}
                  className="mb-2 block text-sm font-medium text-slate-700"
                >
                  {field
                    .replaceAll("_", " ")
                    .replace(/\b\w/g, (letter) =>
                      letter.toUpperCase(),
                    )}
                </label>

                <Input
                  id={field}
                  name={field}
                  type="number"
                  step="any"
                  value={value}
                  onChange={handleChange}
                  disabled={isLoading}
                  required
                />
              </div>
            ),
          )}

          <div className="md:col-span-2">
            <Button
              type="submit"
              disabled={isLoading}
            >
              {isLoading
                ? "Predicting..."
                : "Predict churn"}
            </Button>
          </div>
        </form>
      </Card>

      {isLoading ? (
        <Card>
          <div className="flex items-center gap-3">
            <LoadingSpinner />

            <p className="text-sm text-slate-600">
              Running churn inference.
            </p>
          </div>
        </Card>
      ) : null}

      {error ? (
        <Card className="border-red-200 bg-red-50">
          <h2 className="font-semibold text-red-800">
            Prediction failed
          </h2>

          <p className="mt-2 text-sm text-red-700">
            {error}
          </p>
        </Card>
      ) : null}

      {result ? (
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <Card>
            <p className="text-sm text-slate-500">
              Prediction
            </p>

            <p className="mt-3 text-2xl font-bold">
              {result.churn_prediction === 1
                ? "Likely to churn"
                : "Likely to stay"}
            </p>
          </Card>

          <Card>
            <p className="text-sm text-slate-500">
              Churn probability
            </p>

            <p className="mt-3 text-2xl font-bold">
              {formatPercentage(
                result.churn_probability * 100,
              )}
            </p>
          </Card>

          <Card>
            <p className="text-sm text-slate-500">
              Risk level
            </p>

            <div className="mt-3">
              <Badge variant={riskVariant}>
                {result.risk_level}
              </Badge>
            </div>
          </Card>

          <Card>
            <p className="text-sm text-slate-500">
              Latency
            </p>

            <p className="mt-3 text-2xl font-bold">
              {formatMilliseconds(
                result.latency_ms,
              )}
            </p>
          </Card>
        </section>
      ) : null}
    </div>
  );
}