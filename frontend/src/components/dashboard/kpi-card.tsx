import { Card } from "@/components/ui/card";

interface KpiCardProps {
  name: string;
  value: string;
  unit?: string | null;
}

export function KpiCard({
  name,
  value,
  unit,
}: KpiCardProps) {
  return (
    <Card>
      <p className="text-sm font-medium text-slate-500">
        {name}
      </p>

      <div className="mt-3 flex items-end gap-2">
        <p className="text-3xl font-bold text-slate-900">
          {value}
        </p>

        {unit ? (
          <p className="pb-1 text-sm text-slate-500">
            {unit}
          </p>
        ) : null}
      </div>
    </Card>
  );
}