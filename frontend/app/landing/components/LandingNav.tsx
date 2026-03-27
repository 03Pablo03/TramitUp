import Link from "next/link";

export function LandingNav() {
  return (
    <nav className="sticky top-0 z-50 bg-stone-900/30 backdrop-blur-lg">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-3">
        <Link href="/" className="text-lg font-bold tracking-tight text-white">
          TramitUp
        </Link>
        <div className="flex items-center gap-1">
          <Link
            href="/#como-funciona"
            className="hidden rounded-lg px-3 py-2 text-sm text-white/80 hover:bg-white/10 hover:text-white sm:block transition-colors"
          >
            Cómo funciona
          </Link>
          <Link
            href="/pricing"
            className="hidden rounded-lg px-3 py-2 text-sm text-white/80 hover:bg-white/10 hover:text-white sm:block transition-colors"
          >
            Precios
          </Link>
          <div className="ml-2 h-5 w-px bg-white/20 hidden sm:block" />
          <Link
            href="/login"
            className="ml-2 rounded-lg bg-white/10 px-4 py-2 text-sm font-medium text-white backdrop-blur-sm hover:bg-white/20 transition-colors"
          >
            Acceder
          </Link>
        </div>
      </div>
    </nav>
  );
}
