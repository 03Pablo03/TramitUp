import { NextRequest, NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  process.env.BACKEND_URL ||
  "http://127.0.0.1:8000";

/**
 * Proxy a la API del backend. Añade el token desde la sesión (cookies).
 * Evita 401: el servidor lee la sesión y reenvía con Authorization.
 */
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path?: string[] }> }
) {
  return proxyRequest(request, await params, "GET");
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ path?: string[] }> }
) {
  return proxyRequest(request, await params, "POST");
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ path?: string[] }> }
) {
  return proxyRequest(request, await params, "PATCH");
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ path?: string[] }> }
) {
  return proxyRequest(request, await params, "DELETE");
}

async function proxyRequest(
  request: NextRequest,
  params: { path?: string[] },
  method: string
) {
  const path = params.path?.join("/") ?? "";
  if (!path) {
    return NextResponse.json({ error: "Path required" }, { status: 400 });
  }

  const supabase = await createServerSupabaseClient();
  const { data: { user }, error: userError } = await supabase.auth.getUser();
  if (userError || !user) {
    return NextResponse.json({ error: "No autorizado" }, { status: 401 });
  }
  const { data: { session } } = await supabase.auth.getSession();
  const accessToken = session?.access_token;
  if (!accessToken) {
    return NextResponse.json({ error: "No autorizado" }, { status: 401 });
  }

  const baseUrl = BACKEND_URL.replace(/\/$/, "");
  const url = `${baseUrl}/api/v1/${path}${request.nextUrl.search}`;
  const headers: Record<string, string> = {
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  };

  try {
    const init: RequestInit = {
      method,
      headers,
    };
    if (method === "POST" || method === "PUT" || method === "PATCH") {
      const contentType = request.headers.get("content-type") ?? "";
      if (contentType) headers["Content-Type"] = contentType;
      // multipart/form-data (file uploads) must be forwarded as ArrayBuffer to
      // preserve binary content — text() corrupts PDFs and images.
      // Keep the original Content-Type so the backend receives the correct boundary.
      if (contentType.startsWith("multipart/form-data")) {
        headers["Content-Type"] = contentType;
        init.body = await request.arrayBuffer();
      } else {
        init.body = await request.text();
      }
    }

    const res = await fetch(url, init);

    if (res.status >= 500) {
      let detail = "El backend devolvió un error interno.";
      try {
        const errBody = await res.clone().json();
        detail = errBody.detail || errBody.error || detail;
      } catch { /* ignorar si no es JSON */ }
      return NextResponse.json({ error: detail }, { status: 502 });
    }

    if (res.body) {
      return new NextResponse(res.body, {
        status: res.status,
        statusText: res.statusText,
        headers: res.headers,
      });
    }
    return new NextResponse(null, { status: res.status });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    return NextResponse.json(
      { error: `No se pudo conectar al backend (${baseUrl}): ${msg}` },
      { status: 502 }
    );
  }
}
