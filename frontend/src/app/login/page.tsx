import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

export default function LoginPage() {
  return (
    <div className="mx-auto max-w-xl space-y-6">
      <section className="text-center">
        <h1 className="text-3xl font-bold text-slate-900">
          Sign in to InsightPilot AI
        </h1>

        <p className="mt-2 text-slate-500">
          Secure user authentication will be added in the next
          phase.
        </p>
      </section>

      <Card>
        <div className="flex justify-center">
          <Badge variant="warning">
            Authentication placeholder
          </Badge>
        </div>

        <h2 className="mt-5 text-center text-xl font-semibold text-slate-900">
          Amazon Cognito coming in Phase 11
        </h2>

        <p className="mt-3 text-center text-sm leading-6 text-slate-600">
          This page is currently a user-interface placeholder.
          It does not accept credentials and does not perform
          authentication.
        </p>

        <div className="mt-6 space-y-4">
          <div>
            <label
              htmlFor="email"
              className="mb-2 block text-sm font-medium text-slate-700"
            >
              Email
            </label>

            <input
              id="email"
              type="email"
              disabled
              placeholder="name@example.com"
              className="w-full cursor-not-allowed rounded-lg border border-slate-300 bg-slate-100 px-3 py-2 text-sm text-slate-500"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="mb-2 block text-sm font-medium text-slate-700"
            >
              Password
            </label>

            <input
              id="password"
              type="password"
              disabled
              placeholder="Password"
              className="w-full cursor-not-allowed rounded-lg border border-slate-300 bg-slate-100 px-3 py-2 text-sm text-slate-500"
            />
          </div>

          <button
            type="button"
            disabled
            className="w-full cursor-not-allowed rounded-lg bg-slate-400 px-4 py-2 text-sm font-medium text-white"
          >
            Sign in
          </button>
        </div>
      </Card>
    </div>
  );
}