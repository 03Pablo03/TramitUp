import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createServerSupabaseClient } from "@/lib/supabase/server";

/**
 * POST /api/auth/signout
 *
 * Cierra la sesión en el servidor y limpia las cookies de auth.
 */
export async function POST() {
  const response = NextResponse.json({ ok: true });
  try {
    const supabase = await createServerSupabaseClient();
    await supabase.auth.signOut();
  } catch {
    // Continuar para limpiar cookies aunque falle
  }
  // Limpiar explícitamente las cookies de Supabase en la respuesta
  const cookieStore = await cookies();
  const allCookies = cookieStore.getAll();
  for (const cookie of allCookies) {
    if (cookie.name.includes("sb-") && cookie.name.includes("auth")) {
      response.cookies.delete(cookie.name);
    }
  }
  return response;
}
