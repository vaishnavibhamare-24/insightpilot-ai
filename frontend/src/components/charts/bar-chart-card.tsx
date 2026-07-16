"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Card } from "@/components/ui/card";

interface BarChartCardProps {
  title: string;
  data: Record<string, unknown>[];
  xField: string;
  yField: string;
}

export function BarChartCard({
  title,
  data,
  xField,
  yField,
}: BarChartCardProps) {
  return (
    <Card>
      <h2 className="mb-5 text-lg font-semibold">
        {title}
      </h2>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={xField} />
            <YAxis />
            <Tooltip />
            <Bar dataKey={yField} fill="currentColor" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}