import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Términos y condiciones de uso",
  description: "Términos y condiciones de uso del servicio Tramitup.",
};

export default function TerminosPage() {
  return (
    <div className="min-h-screen bg-white">
      <header className="border-b border-[var(--border)] bg-white px-4 py-4">
        <div className="mx-auto flex max-w-3xl items-center justify-between">
          <span className="font-display text-lg font-bold tracking-tight text-[var(--primary)]">
            TramitUp
          </span>
          <Link href="/" className="text-sm text-[var(--primary)] hover:underline">
            Volver
          </Link>
        </div>
      </header>
      <main className="mx-auto max-w-3xl px-4 py-16">
        <h1 className="font-display text-3xl font-bold text-[var(--text-dark)]">
          Términos y condiciones de uso
        </h1>
        <p className="mt-2 text-sm text-[var(--text-muted)]">
          Última actualización: 15 de marzo de 2025
        </p>

        <div className="mt-10 space-y-8 text-[var(--text-body)] prose prose-slate max-w-none">
          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              1. Información general
            </h2>
            <p>
              Los presentes Términos y Condiciones de Uso (en adelante, &quot;los Términos&quot;) regulan el acceso y uso de la plataforma Tramitup, accesible a través del sitio web y aplicaciones asociadas (en adelante, &quot;el Servicio&quot;), operada por Tramitup (en adelante, &quot;la Empresa&quot;).
            </p>
            <p className="mt-4">
              Al acceder o utilizar el Servicio, el usuario (en adelante, &quot;el Usuario&quot;) declara haber leído, comprendido y aceptado íntegramente los presentes Términos. Si el Usuario no está de acuerdo con alguna de las condiciones aquí establecidas, deberá abstenerse de utilizar el Servicio.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              2. Descripción del servicio
            </h2>
            <p>
              Tramitup es una plataforma digital que ofrece información jurídica y orientación sobre normativa española y europea de carácter público. El Servicio permite al Usuario:
            </p>
            <ul className="mt-4 list-disc pl-6 space-y-2">
              <li>Consultar información sobre trámites administrativos, derechos y obligaciones legales.</li>
              <li>Recibir explicaciones claras sobre normativa vigente aplicable a situaciones concretas.</li>
              <li>Obtener orientación sobre los pasos a seguir en procedimientos burocráticos o administrativos.</li>
              <li>Generar borradores de documentos orientativos basados en modelos estándar.</li>
            </ul>
            <p className="mt-4">
              El Servicio tiene carácter meramente informativo y orientativo. Tramitup <strong>NO</strong> presta servicios de asesoramiento jurídico profesional, ni actúa como despacho de abogados, gestoría o representante legal del Usuario en ningún procedimiento.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              3. Naturaleza del servicio e importante limitación de responsabilidad
            </h2>
            <p>El Usuario reconoce y acepta expresamente que:</p>
            <ul className="mt-4 list-disc pl-6 space-y-2">
              <li>La información proporcionada por Tramitup se basa en normativa de acceso público y tiene finalidad exclusivamente orientativa.</li>
              <li>Tramitup NO sustituye en ningún caso el asesoramiento legal personalizado de un abogado colegiado, gestor administrativo u otro profesional habilitado.</li>
              <li>El contenido generado por la plataforma puede contener errores, omisiones o no reflejar los cambios más recientes en la legislación.</li>
              <li>El Usuario es el único responsable de revisar, validar y adaptar cualquier documento o información proporcionada antes de presentarla ante cualquier organismo público o privado.</li>
              <li>Tramitup no se hace responsable de las decisiones tomadas por el Usuario basándose en la información obtenida a través del Servicio.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              4. Condiciones de acceso y registro
            </h2>
            <p>
              El acceso a determinadas funcionalidades del Servicio requiere el registro previo del Usuario mediante la creación de una cuenta personal. El Usuario se compromete a:
            </p>
            <ul className="mt-4 list-disc pl-6 space-y-2">
              <li>Proporcionar información veraz, completa y actualizada durante el proceso de registro.</li>
              <li>Mantener la confidencialidad de sus credenciales de acceso (usuario y contraseña).</li>
              <li>Notificar inmediatamente a Tramitup ante cualquier uso no autorizado de su cuenta.</li>
              <li>No compartir su cuenta con terceros ni permitir el acceso de personas no autorizadas.</li>
            </ul>
            <p className="mt-4">
              Tramitup se reserva el derecho de suspender o cancelar cuentas en caso de incumplimiento de los presentes Términos o uso fraudulento del Servicio.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              5. Planes y condiciones económicas
            </h2>
            <p>
              Tramitup ofrece un plan gratuito con funcionalidades limitadas y planes de pago con acceso ampliado. Las condiciones económicas aplicables son:
            </p>
            <ul className="mt-4 list-disc pl-6 space-y-2">
              <li>Los precios vigentes son los publicados en la página web en el momento de la contratación, e incluyen el IVA aplicable.</li>
              <li>El pago se realiza de forma anticipada mediante los métodos habilitados en la plataforma.</li>
              <li>Las suscripciones se renuevan automáticamente salvo cancelación expresa por parte del Usuario con al menos 24 horas de antelación al período de renovación.</li>
              <li>Tramitup se reserva el derecho de modificar sus tarifas, notificando al Usuario con al menos 30 días de antelación.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              6. Propiedad intelectual
            </h2>
            <p>
              Todos los contenidos del Servicio, incluyendo pero no limitándose a textos, diseños, logotipos, código fuente, interfaces y modelos de documentos, son propiedad de Tramitup o de sus licenciantes, y están protegidos por la normativa de propiedad intelectual e industrial vigente.
            </p>
            <p className="mt-4">
              Queda expresamente prohibida la reproducción, distribución, transformación o comunicación pública de dichos contenidos sin autorización expresa y por escrito de Tramitup.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              7. Uso aceptable
            </h2>
            <p>
              El Usuario se compromete a utilizar el Servicio de conformidad con la ley y los presentes Términos, y se abstiene expresamente de:
            </p>
            <ul className="mt-4 list-disc pl-6 space-y-2">
              <li>Utilizar el Servicio con fines ilegales, fraudulentos o contrarios a la buena fe.</li>
              <li>Intentar acceder a sistemas o datos no autorizados de la plataforma.</li>
              <li>Reproducir, vender o explotar comercialmente los contenidos del Servicio sin autorización.</li>
              <li>Introducir virus, malware o cualquier código dañino en la plataforma.</li>
              <li>Hacer un uso masivo o automatizado del Servicio sin autorización expresa de Tramitup.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              8. Modificaciones del servicio y los términos
            </h2>
            <p>
              Tramitup se reserva el derecho de modificar, suspender o interrumpir total o parcialmente el Servicio en cualquier momento, con o sin previo aviso.
            </p>
            <p className="mt-4">
              Asimismo, Tramitup podrá actualizar los presentes Términos en cualquier momento. Las modificaciones serán notificadas al Usuario mediante el correo electrónico registrado o mediante aviso en la plataforma, con al menos 15 días de antelación a su entrada en vigor. El uso continuado del Servicio tras dicho período implicará la aceptación de los nuevos Términos.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              9. Ley aplicable y jurisdicción
            </h2>
            <p>
              Los presentes Términos se rigen por la legislación española. Para la resolución de cualquier controversia derivada del uso del Servicio, las partes se someten, con renuncia expresa a cualquier otro fuero, a los Juzgados y Tribunales de la ciudad de Madrid, salvo que la normativa de protección de consumidores establezca otro fuero imperativo.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              10. Contacto
            </h2>
            <p>
              Para cualquier consulta relacionada con los presentes Términos, el Usuario puede contactar con Tramitup a través de:
            </p>
            <p className="mt-4">
              Correo electrónico:{" "}
              <a href="mailto:soportetramitup@gmail.com" className="text-[var(--primary)] hover:underline font-medium">
                soportetramitup@gmail.com
              </a>
            </p>
          </section>
        </div>
      </main>
    </div>
  );
}
