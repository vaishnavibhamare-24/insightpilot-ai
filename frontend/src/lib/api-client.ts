import type {
  ApiErrorResponse,
  ApiRequestError,
} from "@/types/api";

interface ApiRequestOptions extends RequestInit {
  query?: Record<
    string,
    string | number | boolean | undefined
  >;
}

function createApiError(
  message: string,
  status?: number,
  requestId?: string | null,
): ApiRequestError {
  const error = new Error(message) as ApiRequestError;

  error.status = status;
  error.requestId = requestId;

  return error;
}

export async function apiRequest<T>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  const normalizedPath = path.replace(/^\/+/, "");

  const url = new URL(
    `/api/backend/${normalizedPath}`,
    window.location.origin,
  );

  Object.entries(options.query ?? {}).forEach(
    ([key, value]) => {
      if (value !== undefined) {
        url.searchParams.set(key, String(value));
      }
    },
  );

  const headers = new Headers(options.headers);

  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  const requestId =
    response.headers.get("X-Request-ID");

  let payload: unknown;

  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const errorPayload =
      payload as ApiErrorResponse | null;

    const message =
      errorPayload?.error?.message ??
      errorPayload?.detail ??
      `Request failed with status ${response.status}.`;

    throw createApiError(
      message,
      response.status,
      requestId,
    );
  }

  return payload as T;
}