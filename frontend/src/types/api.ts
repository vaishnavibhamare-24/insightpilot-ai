export interface ApiErrorDetail {
  code?: string;
  message: string;
  details?: unknown;
}

export interface ApiErrorResponse {
  success?: false;
  error?: ApiErrorDetail;
  detail?: string;
  request_id?: string | null;
}

export interface ApiRequestError extends Error {
  status?: number;
  requestId?: string | null;
}