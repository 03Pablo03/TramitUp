import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  const next = searchParams.get("next") ?? "/chat";
  const error = searchParams.get("error");
  const errorDescription = searchParams.get("error_description");

  if (error) {
    // Log error only in development
    if (process.env.NODE_ENV === "development") {
      console.error("[auth/callback] Error:", error, errorDescription);
    }
    return NextResponse.redirect(`${origin}/login?error=${encodeURIComponent(errorDescription || error)}`);
  }

  const redirectUrl = `${origin}${next.startsWith("/") ? next : `/${next}`}`;

  if (!code) {
    return NextResponse.redirect(redirectUrl);
  }

  const cookieStore = await cookies();
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => cookieStore.getAll(),
        setAll: (cookiesToSet: { name: string; value: string; options?: Record<string, unknown> }[]) => {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          );
        },
      },
    }
  );

  const { error: exchangeError } = await supabase.auth.exchangeCodeForSession(code);
  if (exchangeError) {
    // Log error only in development
    if (process.env.NODE_ENV === "development") {
      console.error("[auth/callback] Exchange error:", exchangeError.message);
    }
    return NextResponse.redirect(`${origin}/login?error=${encodeURIComponent(exchangeError.message)}`);
  }

  return NextResponse.redirect(redirectUrl);
}
