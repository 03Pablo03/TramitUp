import { NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";

/**
 * GET /api/auth/me
 *
 * Devuelve el usuario actual desde las cookies (servidor).
 * Sirve de respaldo cuando el cliente Supabase se bloquea.
 */
export async function GET() {
  try {
    const supabase = await createServerSupabaseClient();
    const { data: { user }, error: userError } = await supabase.auth.getUser();
    if (userError || !user) {
      return NextResponse.json({ error: "No autorizado" }, { status: 401 });
    }
    const { data: { session } } = await supabase.auth.getSession();
    if (!session?.access_token) {
      return NextResponse.json({ error: "No autorizado" }, { status: 401 });
    }
    return NextResponse.json({
      user: { id: user.id, email: user.email },
      access_token: session.access_token,
      refresh_token: session.refresh_token,
    });
  } catch {
    return NextResponse.json({ error: "Error" }, { status: 500 });
  }
}
