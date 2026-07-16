import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

export default function MonitoringPage() {
  return (
    <div className="space-y-6">
      <section>
        <div className="flex flex-wrap items-center gap-3">
          <h1 className="text-3xl font-bold text-slate-900">
            Model Monitoring
          </h1>

          <Badge variant="warning">
            Backend endpoint pending
          </Badge>
        </div>

        <p className="mt-2 text-slate-500">
          Track model execution status, monitoring schedules,
          and the latest model-monitoring results.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <Card>
          <p className="text-sm text-slate-500">
            Schedule name
          </p>

          <p className="mt-3 text-2xl font-bold text-slate-900">
            Unavailable
          </p>
        </Card>

        <Card>
          <p className="text-sm text-slate-500">
            Schedule status
          </p>

          <p className="mt-3 text-2xl font-bold text-slate-900">
            Unavailable
          </p>
        </Card>

        <Card>
          <p className="text-sm text-slate-500">
            Latest execution
          </p>

          <p className="mt-3 text-2xl font-bold text-slate-900">
            Unavailable
          </p>
        </Card>
      </section>

      <Card className="border-amber-200 bg-amber-50">
        <h2 className="text-lg font-semibold text-amber-900">
          Monitoring API not connected
        </h2>

        <p className="mt-2 text-sm leading-6 text-amber-800">
          The monitoring page is ready, but the current
          backend monitoring file does not yet expose an API
          endpoint.
        </p>

        <p className="mt-3 text-sm leading-6 text-amber-800">
          The future endpoint can be added at:
        </p>

        <pre className="mt-3 overflow-x-auto rounded-lg bg-slate-950 p-4 text-sm text-slate-100">
          <code>
            GET /api/v1/monitoring/model
          </code>
        </pre>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold text-slate-900">
          Expected monitoring information
        </h2>

        <ul className="mt-4 space-y-3 text-sm text-slate-600">
          <li>Monitoring schedule name</li>
          <li>Schedule status</li>
          <li>Latest execution time</li>
          <li>Model drift or data-quality findings</li>
          <li>SageMaker resource availability</li>
        </ul>
      </Card>
    </div>
  );
}