import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

const PUBLIC_ROUTES = ["/", "/login", "/pricing", "/auth/callback", "/login/forgot"];
const ONBOARDING_ROUTE = "/onboarding";

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll: (cookies: { name: string; value: string; options?: Record<string, unknown> }[]) => {
          cookies.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          response = NextResponse.next({ request });
          cookies.forEach(({ name, value, options }) =>
            response.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  const { data: { user } } = await supabase.auth.getUser();
  const path = request.nextUrl.pathname;
  const isPublic = PUBLIC_ROUTES.some((r) => r === path || path.startsWith(r + "/"));
  const isOnboarding = path === ONBOARDING_ROUTE;
  const isApiRoute = path.startsWith("/api/");

  if (!user) {
    if (!isPublic) {
      // API routes: no redirect, la ruta devuelve 401 si necesita auth
      if (isApiRoute) return response;
      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("redirect", path);
      return NextResponse.redirect(loginUrl);
    }
    return response;
  }

  // API routes: pasar sin lógica de onboarding
  if (isApiRoute) return response;

  // Usuario autenticado - comprobar onboarding
  const { data: profile } = await supabase
    .from("profiles")
    .select("onboarding_completed, plan")
    .eq("id", user.id)
    .single();

  const onboardingCompleted = profile?.onboarding_completed ?? false;
  const isPremium = profile?.plan === "pro";

  // Permitir /pricing incluso si no ha completado onboarding (para "Ver plan PRO")
  if (path === "/pricing") return response;

  if (!onboardingCompleted && !isOnboarding) {
    if (path === "/login") {
      return NextResponse.redirect(new URL(ONBOARDING_ROUTE, request.url));
    }
    return NextResponse.redirect(new URL(ONBOARDING_ROUTE, request.url));
  }

  if (onboardingCompleted && path === "/login") {
    return NextResponse.redirect(new URL("/chat", request.url));
  }

  // TODO: reactivar restricción PRO antes de producción
  // if (path === "/alerts" && !isPremium) {
  //   return NextResponse.redirect(new URL("/account", request.url));
  // }

  return response;
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
