"use client";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <Card className="border-red-200 bg-red-50">
      <h2 className="text-lg font-semibold text-red-800">
        Something went wrong
      </h2>

      <p className="mt-2 text-sm text-red-700">
        {error.message}
      </p>

      <Button
        className="mt-4"
        onClick={() => reset()}
      >
        Try again
      </Button>
    </Card>
  );
}