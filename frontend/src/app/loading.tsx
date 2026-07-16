import { LoadingSpinner } from "@/components/ui/loading-spinner";

export default function Loading() {
  return (
    <div className="flex min-h-80 items-center justify-center">
      <LoadingSpinner />
    </div>
  );
}