export interface ChatCitation {
  text?: string | null;
  source_uri?: string | null;
  document_name?: string | null;
}

export interface ChatVisualization {
  chart_type?: string;
  x_field?: string | null;
  y_field?: string | null;
  title?: string;
  data?: Record<string, unknown>[];
}

export interface ChatRequest {
  message: string;
  session_id?: string | null;
}

export interface ChatResponse {
  answer: string;
  route?: string | null;
  route_reason?: string | null;
  confidence?: number | null;
  agents_used: string[];
  generated_sql?: string | null;
  data?: Record<string, unknown> | null;
  citations: ChatCitation[];
  visualization?: ChatVisualization | null;
  recommendations: string[];
  alert?: Record<string, unknown> | null;
  errors: string[];
  session_id: string;
  latency_ms: number;
}