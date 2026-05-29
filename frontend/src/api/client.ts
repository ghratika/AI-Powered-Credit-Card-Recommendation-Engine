import type {
  AAConnectResponse,
  ApiErrorBody,
  RecommendationRequest,
  RecommendationResponse,
} from "../types";

/** Local dev uses Vite proxy; production (Vercel) uses VITE_API_BASE_URL. */
const API_BASE =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "/api/v1";

export class ApiClientError extends Error {
  readonly status: number;
  readonly code: string;
  readonly requestId: string;

  constructor(status: number, body: ApiErrorBody) {
    super(body.error.message);
    this.name = "ApiClientError";
    this.status = status;
    this.code = body.error.code;
    this.requestId = body.request_id;
  }
}

async function parseJson<T>(response: Response): Promise<T> {
  const text = await response.text();
  if (!text) return {} as T;
  return JSON.parse(text) as T;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init,
  });

  if (!response.ok) {
    try {
      const body = await parseJson<ApiErrorBody>(response);
      throw new ApiClientError(response.status, body);
    } catch (e) {
      if (e instanceof ApiClientError) throw e;
      throw new ApiClientError(response.status, {
        error: { code: "HTTP_ERROR", message: response.statusText || "Request failed" },
        request_id: "unknown",
      });
    }
  }

  return parseJson<T>(response);
}

export async function connectAa(): Promise<AAConnectResponse> {
  return request<AAConnectResponse>("/aa/connect", { method: "POST" });
}

export async function getRecommendations(
  body: RecommendationRequest,
): Promise<RecommendationResponse> {
  return request<RecommendationResponse>("/recommendations", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function apiErrorMessage(error: unknown): string {
  if (error instanceof ApiClientError) {
    switch (error.status) {
      case 400:
        return error.message || "Please check your profile details.";
      case 422:
        return "Connect Account Aggregator before requesting recommendations.";
      case 404:
        return error.message || "No eligible cards for your profile.";
      case 502:
        return "AI recommendation service is temporarily unavailable. Please try again.";
      case 503:
        return "Card data is unavailable. Please try again later.";
      case 500:
        return "Unable to reach the API server. Check that the Railway backend is running and VITE_API_BASE_URL is set on Vercel.";
      default:
        return error.message || "Something went wrong. Please try again.";
    }
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "Network error. Check VITE_API_BASE_URL (production) or start the local backend on port 8000.";
}
