/** Proxy en Next.js añade el token desde cookies. Mismo origen = sin CORS ni 401 por token. */
const API_BASE = "/api/backend";

/** Token para uso directo (ej. chat streaming). Lo establece AuthContext cuando usa fallback servidor. */
let serverAccessToken: string | null = null;
export function setServerAccessToken(token: string | null) {
  serverAccessToken = token;
}

export async function getAccessToken(): Promise<string | null> {
  if (typeof window === "undefined") return null;
  if (serverAccessToken) return serverAccessToken;
  const { createClient } = await import("@/lib/supabase/client");
  const supabase = createClient();
  const { data } = await supabase.auth.getSession();
  return data.session?.access_token ?? null;
}

export async function apiFetch(path: string, options: RequestInit = {}) {
  const url = `${API_BASE}${path.startsWith("/") ? path : `/${path}`}`;
  return fetch(url, { ...options, credentials: "include" });
}

/**
 * Fetch wrapper que lanza error automáticamente si la respuesta no es ok.
 * Útil para casos donde quieres manejo de errores automático.
 */
export async function apiFetchWithError(path: string, options: RequestInit = {}): Promise<Response> {
  const response = await apiFetch(path, options);
  
  if (!response.ok) {
    let errorMessage = `Error ${response.status}`;
    try {
      const errorData = await response.json();
      errorMessage = errorData.error || errorData.detail || errorMessage;
    } catch {
      errorMessage = response.statusText || errorMessage;
    }
    throw new Error(errorMessage);
  }
  
  return response;
}
