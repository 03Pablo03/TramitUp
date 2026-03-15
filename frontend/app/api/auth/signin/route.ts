import { NextResponse } from "next/server";

/**
 * POST /api/auth/signin
 *
 * Proxy al backend para evitar CORS. El frontend llama aquí (mismo origen)
 * y Next.js reenvía al backend.
 */
export async function POST(request: Request) {
  try {
    const body = await request.json();
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

    const res = await fetch(`${apiUrl}/api/v1/auth/signin`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      return NextResponse.json(
        { detail: data.detail || "Error al iniciar sesión" },
        { status: res.status }
      );
    }

    return NextResponse.json(data);
  } catch {
    return NextResponse.json(
      {
        detail: "No se pudo conectar con el servidor. Comprueba que el backend esté corriendo (npm run dev en /backend).",
      },
      { status: 502 }
    );
  }
}
