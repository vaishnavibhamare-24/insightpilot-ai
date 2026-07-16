export interface DashboardKPI {
  name: string;
  value: string | number | null;
  unit?: string | null;
}

export interface DashboardMetricsResponse {
  kpis: DashboardKPI[];
  source: string;
}