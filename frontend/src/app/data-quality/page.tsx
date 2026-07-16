import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

export default function DataQualityPage() {
  return (
    <div className="space-y-6">
      <section>
        <div className="flex flex-wrap items-center gap-3">
          <h1 className="text-3xl font-bold text-slate-900">
            Data Quality
          </h1>

          <Badge variant="warning">
            Backend endpoint pending
          </Badge>
        </div>

        <p className="mt-2 text-slate-500">
          Review data validation results, quality scores,
          failed records, and rule violations.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <Card>
          <p className="text-sm text-slate-500">
            Quality score
          </p>

          <p className="mt-3 text-2xl font-bold text-slate-900">
            Unavailable
          </p>
        </Card>

        <Card>
          <p className="text-sm text-slate-500">
            Total rows
          </p>

          <p className="mt-3 text-2xl font-bold text-slate-900">
            Unavailable
          </p>
        </Card>

        <Card>
          <p className="text-sm text-slate-500">
            Passed rows
          </p>

          <p className="mt-3 text-2xl font-bold text-slate-900">
            Unavailable
          </p>
        </Card>

        <Card>
          <p className="text-sm text-slate-500">
            Failed rows
          </p>

          <p className="mt-3 text-2xl font-bold text-slate-900">
            Unavailable
          </p>
        </Card>
      </section>

      <Card className="border-amber-200 bg-amber-50">
        <h2 className="text-lg font-semibold text-amber-900">
          Data-quality API not connected
        </h2>

        <p className="mt-2 text-sm leading-6 text-amber-800">
          The frontend page is ready, but the FastAPI backend
          does not currently expose a data-quality report
          endpoint.
        </p>

        <p className="mt-3 text-sm leading-6 text-amber-800">
          A future endpoint can be added at:
        </p>

        <pre className="mt-3 overflow-x-auto rounded-lg bg-slate-950 p-4 text-sm text-slate-100">
          <code>
            GET /api/v1/data-quality/report
          </code>
        </pre>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold text-slate-900">
          Expected metrics
        </h2>

        <ul className="mt-4 space-y-3 text-sm text-slate-600">
          <li>Overall data-quality score</li>
          <li>Total validated rows</li>
          <li>Passed and failed row counts</li>
          <li>Failed validation rules</li>
          <li>Latest quality-check execution status</li>
        </ul>
      </Card>
    </div>
  );
}