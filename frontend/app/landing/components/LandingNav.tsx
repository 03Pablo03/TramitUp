import Link from "next/link";

export function LandingNav() {
  return (
    <nav className="sticky top-0 z-50 border-b border-white/10 bg-stone-900/20 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <span className="text-xl font-bold tracking-tight text-[var(--primary)]">TramitUp</span>
        <div className="flex items-center gap-3 sm:gap-6">
          <Link
            href="/#como-funciona"
            className="hidden text-sm font-bold text-white hover:text-blue-300 sm:block transition-colors"
          >
            Cómo funciona
          </Link>
          <Link
            href="/pricing"
            className="hidden text-sm font-bold text-white hover:text-blue-300 sm:block transition-colors"
          >
            Precios
          </Link>
          <Link
            href="/login"
            className="text-sm font-bold text-white hover:text-blue-300 transition-colors"
          >
            Iniciar sesión
          </Link>
          <Link
            href="/pricing"
            className="inline-flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-5 py-2.5 text-sm font-bold text-white shadow-lg shadow-blue-500/30 hover:from-[var(--primary-dark)] hover:to-blue-700 transition-all"
          >
            <span className="text-amber-300">★</span> Hazte PRO
          </Link>
        </div>
      </div>
    </nav>
  );
}
