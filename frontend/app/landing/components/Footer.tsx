import Link from "next/link";

export function Footer() {
  return (
    <footer className="overflow-hidden bg-slate-900 px-4 pt-8 pb-6 text-white">
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
          <div className="flex flex-wrap gap-6 md:gap-10">
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
        <div className="mt-6 border-t border-white/10 pt-8">
          <p className="text-center text-sm text-slate-500">
            © 2026 Tramitup. Servicio de información jurídica. No prestamos asesoramiento legal.
          </p>
        </div>
      </div>
    </footer>
  );
}
