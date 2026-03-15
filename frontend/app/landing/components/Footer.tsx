import Link from "next/link";

const disclaimer =
  "Tramitup es un servicio de información jurídica basado en normativa pública española. No prestamos asesoramiento legal, no somos abogados y no garantizamos resultados. Los modelos de escritos generados son orientativos y deben ser revisados por el usuario antes de su presentación. Para situaciones complejas, recomendamos consultar con un profesional.";

export function Footer() {
  return (
    <footer className="relative overflow-hidden bg-gradient-to-b from-slate-900 to-slate-950 px-4 pt-20 pb-10 text-white">
      {/* Decorative elements behind content */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute -top-32 -left-32 h-96 w-96 rounded-full bg-blue-600/10 blur-3xl" />
        <div className="absolute -bottom-16 -right-16 h-72 w-72 rounded-full bg-indigo-600/10 blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-64 w-64 rounded-full bg-blue-800/5 blur-2xl" />
      </div>

      {/* Top accent line */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-blue-500/50 to-transparent" />

      <div className="mx-auto max-w-6xl">
        {/* Main footer grid */}
        <div className="flex flex-col gap-12 md:flex-row md:justify-between">
          {/* Brand */}
          <div className="max-w-xs">
            <span className="text-xl font-bold tracking-tight text-white">TramitUp</span>
            <p className="mt-3 text-sm leading-relaxed text-slate-400">
              Entiende tus derechos. Actúa con información.
            </p>
            <p className="mt-3 text-xs text-slate-500">
              Información jurídica para ciudadanos españoles. Basada en normativa pública vigente.
            </p>
          </div>

          {/* Links */}
          <div className="flex flex-wrap gap-12 md:gap-16">
            <div>
              <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-300">Producto</h4>
              <ul className="mt-4 space-y-3">
                <li>
                  <Link href="/#como-funciona" className="text-sm text-slate-400 transition-colors hover:text-white">
                    Cómo funciona
                  </Link>
                </li>
                <li>
                  <Link href="/pricing" className="text-sm text-slate-400 transition-colors hover:text-white">
                    Precios
                  </Link>
                </li>
                <li>
                  <Link href="/login" className="text-sm text-slate-400 transition-colors hover:text-white">
                    Acceder al chat
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-300">Legal</h4>
              <ul className="mt-4 space-y-3">
                <li>
                  <Link href="/aviso-legal" className="text-sm text-slate-400 transition-colors hover:text-white">
                    Aviso legal
                  </Link>
                </li>
                <li>
                  <Link href="/privacidad" className="text-sm text-slate-400 transition-colors hover:text-white">
                    Política de privacidad
                  </Link>
                </li>
                <li>
                  <Link href="/terminos" className="text-sm text-slate-400 transition-colors hover:text-white">
                    Términos de uso
                  </Link>
                </li>
                <li>
                  <Link href="/faq" className="text-sm text-slate-400 transition-colors hover:text-white">
                    Preguntas frecuentes
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-300">Contacto</h4>
              <a
                href="mailto:soportetramitup@gmail.com"
                className="mt-4 block text-sm text-slate-400 transition-colors hover:text-white"
              >
                soportetramitup@gmail.com
              </a>
            </div>
          </div>
        </div>

        {/* Bottom divider and copyright */}
        <div className="mt-16 border-t border-white/10 pt-8">
          <p className="text-center text-sm text-slate-500">
            © 2026 Tramitup. Servicio de información jurídica. No prestamos asesoramiento legal.
          </p>
          <p className="mt-3 text-center text-xs leading-relaxed text-slate-600">
            {disclaimer}
          </p>
        </div>
      </div>
    </footer>
  );
}
