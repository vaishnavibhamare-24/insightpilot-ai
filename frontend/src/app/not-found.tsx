import Link from "next/link";

import { Card } from "@/components/ui/card";

export default function NotFound() {
  return (
    <Card>
      <h1 className="text-2xl font-bold">
        Page not found
      </h1>

      <p className="mt-2 text-slate-500">
        The requested InsightPilot page does not exist.
      </p>

      <Link
        href="/"
        className="mt-5 inline-block text-sm font-medium underline"
      >
        Return to dashboard
      </Link>
    </Card>
  );
}