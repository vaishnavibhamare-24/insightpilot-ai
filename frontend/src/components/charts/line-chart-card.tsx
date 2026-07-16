"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Card } from "@/components/ui/card";

interface LineChartCardProps {
  title: string;
  data: Record<string, unknown>[];
  xField: string;
  yField: string;
}

export function LineChartCard({
  title,
  data,
  xField,
  yField,
}: LineChartCardProps) {
  return (
    <Card>
      <h2 className="mb-5 text-lg font-semibold">
        {title}
      </h2>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={xField} />
            <YAxis />
            <Tooltip />

            <Line
              type="monotone"
              dataKey={yField}
              stroke="currentColor"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}