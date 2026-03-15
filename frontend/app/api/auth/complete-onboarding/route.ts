import { NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";

/**
 * POST /api/auth/complete-onboarding
 *
 * Completa el onboarding del usuario autenticado.
 * La sesión se lee de las cookies en el servidor (sin lock del cliente).
 */
export async function POST(request: Request) {
  try {
    const body = await request.json();
    const categories_interest = Array.isArray(body.categories_interest)
      ? body.categories_interest
      : [];

    const supabase = await createServerSupabaseClient();
    const { data: { user }, error: userError } = await supabase.auth.getUser();
    if (userError || !user) {
      return NextResponse.json(
        { error: "No autorizado. Inicia sesión para continuar." },
        { status: 401 }
      );
    }

    const { error: updateError } = await supabase
      .from("profiles")
      .update({
        categories_interest,
        onboarding_completed: true,
      })
      .eq("id", user.id);

    if (updateError) {
      return NextResponse.json(
        { error: updateError.message || "Error al actualizar el perfil." },
        { status: 400 }
      );
    }

    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json(
      { error: "Error inesperado. Inténtalo de nuevo." },
      { status: 500 }
    );
  }
}
