import { NextRequest, NextResponse } from "next/server";

const backendUrl = process.env.BACKEND_API_URL;
const backendApiKey = process.env.BACKEND_API_KEY;

function buildBackendUrl(
  request: NextRequest,
  pathSegments: string[],
): string {
  if (!backendUrl) {
    throw new Error("BACKEND_API_URL is not configured.");
  }

  const path = pathSegments.join("/");
  const target = new URL(`/api/v1/${path}`, backendUrl);

  request.nextUrl.searchParams.forEach((value, key) => {
    target.searchParams.append(key, value);
  });

  return target.toString();
}

async function proxyRequest(
  request: NextRequest,
  context: {
    params: Promise<{ path: string[] }>;
  },
): Promise<NextResponse> {
  try {
    const { path } = await context.params;
    const targetUrl = buildBackendUrl(request, path);

    const headers = new Headers();

    const contentType = request.headers.get("content-type");

    if (contentType) {
      headers.set("Content-Type", contentType);
    }

    headers.set("Accept", "application/json");

    if (backendApiKey) {
      headers.set("X-API-Key", backendApiKey);
    }

    const requestId = request.headers.get("X-Request-ID");

    if (requestId) {
      headers.set("X-Request-ID", requestId);
    }

    const hasBody = !["GET", "HEAD"].includes(request.method);

    const response = await fetch(targetUrl, {
      method: request.method,
      headers,
      body: hasBody ? await request.text() : undefined,
      cache: "no-store",
    });

    const responseText = await response.text();

    return new NextResponse(responseText, {
      status: response.status,
      headers: {
        "Content-Type":
          response.headers.get("content-type") ??
          "application/json",
        "X-Request-ID":
          response.headers.get("X-Request-ID") ?? "",
      },
    });
  } catch (error) {
    const message =
      error instanceof Error
        ? error.message
        : "Backend proxy failed.";

    return NextResponse.json(
      {
        success: false,
        error: {
          code: "FRONTEND_PROXY_ERROR",
          message,
        },
      },
      {
        status: 502,
      },
    );
  }
}

export const GET = proxyRequest;
export const POST = proxyRequest;
export const PUT = proxyRequest;
export const PATCH = proxyRequest;
export const DELETE = proxyRequest;