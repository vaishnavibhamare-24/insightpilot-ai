export interface DataQualityReport {
  status?: string;
  quality_score?: number;
  total_rows?: number;
  passed_rows?: number;
  failed_rows?: number;
  failed_rules?: Array<Record<string, unknown>>;
  [key: string]: unknown;
}