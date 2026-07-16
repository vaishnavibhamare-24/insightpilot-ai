export interface ChurnPredictionRequest {
  total_orders: number;
  lifetime_revenue: number;
  average_order_value: number;
  days_since_last_order: number;
  customer_lifetime_days: number;
  purchase_frequency: number;
  estimated_clv: number;
}

export interface ChurnPredictionResponse {
  churn_prediction: number;
  churn_probability: number;
  risk_level: string;
  endpoint_name?: string | null;
  latency_ms?: number | null;
}