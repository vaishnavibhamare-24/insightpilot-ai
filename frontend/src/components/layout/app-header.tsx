export function AppHeader() {
  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
      <div>
        <p className="font-semibold text-slate-900">
          InsightPilot AI
        </p>

        <p className="text-xs text-slate-500">
          AWS-powered business intelligence
        </p>
      </div>

      <div className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700">
        Development
      </div>
    </header>
  );
}