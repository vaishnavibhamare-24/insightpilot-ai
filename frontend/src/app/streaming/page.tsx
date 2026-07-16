"use client";

import useSWR from "swr";

import { Card } from "@/components/ui/card";


type EventCount = {
  event_type: string;
  event_count: string | number;
};

type StreamingResponse = {
  rows?: EventCount[];
  results?: EventCount[];
};


const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://127.0.0.1:8000/api/v1";


async function fetcher(
  endpoint: string
): Promise<StreamingResponse> {
  const response = await fetch(
    `${API_URL}/${endpoint}`
  );

  if (!response.ok) {
    throw new Error(
      "Unable to load streaming events."
    );
  }

  return response.json();
}


export default function StreamingPage() {
  const {
    data,
    error,
    isLoading,
  } = useSWR(
    "streaming/events",
    fetcher,
    {
      refreshInterval: 30_000,
    }
  );

  const rows =
    data?.rows ??
    data?.results ??
    [];

  if (isLoading) {
    return (
      <p>Loading streaming events...</p>
    );
  }

  if (error) {
    return (
      <p className="text-red-600">
        Unable to load streaming events.
      </p>
    );
  }

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-bold text-slate-900">
          Real-Time Website Events
        </h1>

        <p className="mt-2 text-slate-500">
          Event counts refresh every 30 seconds.
        </p>
      </section>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {rows.map(
          (
            event,
            index
          ) => (
            <Card
              key={`${event.event_type}-${index}`}
            >
              <p className="text-sm text-slate-500">
                {event.event_type}
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-900">
                {event.event_count}
              </p>
            </Card>
          )
        )}
      </div>
    </div>
  );
}