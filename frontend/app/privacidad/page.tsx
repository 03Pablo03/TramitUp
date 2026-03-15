import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Política de privacidad",
  description: "Política de privacidad y tratamiento de datos personales de Tramitup.",
};

export default function PrivacidadPage() {
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
          Política de privacidad
        </h1>
        <p className="mt-2 text-sm text-[var(--text-muted)]">
          Última actualización: 15 de marzo de 2025
        </p>

        <div className="mt-10 space-y-8 text-[var(--text-body)] prose prose-slate max-w-none">
          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              1. Responsable del tratamiento
            </h2>
            <p>
              En cumplimiento del Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016, relativo a la protección de las personas físicas en lo que respecta al tratamiento de datos personales (RGPD), y de la Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales (LOPDGDD), le informamos de que el Responsable del Tratamiento es:
            </p>
            <ul className="mt-4 list-disc pl-6 space-y-2">
              <li><strong>Denominación:</strong> Tramitup</li>
              <li><strong>Correo electrónico de contacto:</strong>{" "}
                <a href="mailto:soportetramitup@gmail.com" className="text-[var(--primary)] hover:underline">
                  soportetramitup@gmail.com
                </a>
              </li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              2. Datos personales que tratamos
            </h2>
            <p>
              En función del uso que realice del Servicio, Tramitup puede tratar las siguientes categorías de datos personales:
            </p>

            <h3 className="text-lg font-medium text-[var(--text-dark)] mt-6 mb-2">
              2.1 Datos proporcionados directamente por el Usuario
            </h3>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Datos de identificación:</strong> nombre, apellidos, dirección de correo electrónico.</li>
              <li><strong>Datos de acceso:</strong> credenciales de la cuenta (contraseña en formato cifrado).</li>
              <li><strong>Datos de comunicación:</strong> consultas y mensajes enviados a través de la plataforma o al correo de soporte.</li>
              <li><strong>Datos de pago:</strong> gestionados íntegramente por el proveedor de pagos (Stripe). Tramitup no almacena datos de tarjetas bancarias.</li>
            </ul>

            <h3 className="text-lg font-medium text-[var(--text-dark)] mt-6 mb-2">
              2.2 Datos recogidos de forma automática
            </h3>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Datos de navegación:</strong> dirección IP, tipo de navegador, sistema operativo, páginas visitadas y tiempo de sesión.</li>
              <li><strong>Datos de uso del servicio:</strong> tipo de consultas realizadas, funcionalidades utilizadas y frecuencia de uso.</li>
              <li><strong>Cookies y tecnologías similares:</strong> conforme a nuestra Política de Cookies.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              3. Finalidades y base jurídica del tratamiento
            </h2>
            <p>
              Tramitup trata sus datos personales con las siguientes finalidades y bases de legitimación:
            </p>
            <ul className="mt-4 list-disc pl-6 space-y-2">
              <li><strong>Prestación del Servicio contratado:</strong> gestión del alta, mantenimiento y cancelación de la cuenta del Usuario. Base jurídica: ejecución del contrato (Art. 6.1.b RGPD).</li>
              <li><strong>Gestión de pagos y facturación:</strong> tramitación de cobros y emisión de facturas. Base jurídica: ejecución del contrato (Art. 6.1.b RGPD) y obligación legal (Art. 6.1.c RGPD).</li>
              <li><strong>Atención al cliente:</strong> respuesta a consultas, incidencias y solicitudes de soporte. Base jurídica: ejecución del contrato (Art. 6.1.b RGPD).</li>
              <li><strong>Mejora del Servicio:</strong> análisis agregado del uso de la plataforma para mejorar funcionalidades. Base jurídica: interés legítimo (Art. 6.1.f RGPD).</li>
              <li><strong>Comunicaciones comerciales:</strong> envío de información sobre novedades, actualizaciones y ofertas, únicamente con su consentimiento previo. Base jurídica: consentimiento (Art. 6.1.a RGPD).</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              4. Conservación de los datos
            </h2>
            <p>
              Los datos personales serán conservados durante el tiempo necesario para la prestación del Servicio y, una vez finalizada la relación contractual, durante los plazos de prescripción legalmente aplicables:
            </p>
            <ul className="mt-4 list-disc pl-6 space-y-2">
              <li><strong>Datos de cuenta:</strong> hasta la cancelación de la cuenta y, posteriormente, durante 5 años por obligaciones legales.</li>
              <li><strong>Datos de facturación:</strong> durante 5 años conforme a la normativa tributaria.</li>
              <li><strong>Comunicaciones de soporte:</strong> durante 2 años desde la última interacción.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              5. Destinatarios y transferencias internacionales
            </h2>
            <p>
              Tramitup no cede datos personales a terceros con fines comerciales. No obstante, para la correcta prestación del Servicio, podemos compartir datos con los siguientes encargados del tratamiento:
            </p>
            <ul className="mt-4 list-disc pl-6 space-y-2">
              <li>Proveedores de infraestructura y alojamiento (hosting) que operan dentro del Espacio Económico Europeo (EEE) o con las garantías adecuadas conforme al RGPD.</li>
              <li>Proveedor de pagos (Stripe), con sede en la UE, que actúa como responsable independiente del tratamiento de datos de pago.</li>
              <li>Herramientas de análisis web, con las salvaguardias adecuadas en caso de transferencias fuera del EEE.</li>
            </ul>
            <p className="mt-4">
              En ningún caso se realizarán transferencias internacionales de datos sin las garantías exigidas por el RGPD (cláusulas contractuales tipo, decisiones de adecuación u otros mecanismos equivalentes).
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              6. Derechos de los interesados
            </h2>
            <p>
              El Usuario puede ejercer en cualquier momento los siguientes derechos reconocidos por el RGPD y la LOPDGDD:
            </p>
            <ul className="mt-4 list-disc pl-6 space-y-2">
              <li><strong>Derecho de acceso:</strong> conocer qué datos personales tratamos sobre usted.</li>
              <li><strong>Derecho de rectificación:</strong> solicitar la corrección de datos inexactos o incompletos.</li>
              <li><strong>Derecho de supresión (&quot;derecho al olvido&quot;):</strong> solicitar la eliminación de sus datos cuando ya no sean necesarios.</li>
              <li><strong>Derecho de limitación del tratamiento:</strong> solicitar la restricción del tratamiento en determinados supuestos.</li>
              <li><strong>Derecho a la portabilidad:</strong> recibir sus datos en formato estructurado y de uso común.</li>
              <li><strong>Derecho de oposición:</strong> oponerse al tratamiento de sus datos en determinadas circunstancias.</li>
              <li><strong>Derecho a retirar el consentimiento:</strong> en cualquier momento, sin que ello afecte a la licitud del tratamiento previo.</li>
            </ul>
            <p className="mt-4">
              Para ejercer cualquiera de estos derechos, puede dirigirse a{" "}
              <a href="mailto:soportetramitup@gmail.com" className="text-[var(--primary)] hover:underline font-medium">
                soportetramitup@gmail.com
              </a>
              , adjuntando copia de su documento de identidad o medio equivalente de acreditación.
            </p>
            <p className="mt-4">
              Asimismo, si considera que el tratamiento de sus datos no se ajusta a la normativa vigente, tiene derecho a presentar una reclamación ante la Agencia Española de Protección de Datos (AEPD), a través de su sede electrónica:{" "}
              <a href="https://www.aepd.es" target="_blank" rel="noopener noreferrer" className="text-[var(--primary)] hover:underline">
                www.aepd.es
              </a>
              .
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              7. Seguridad de los datos
            </h2>
            <p>
              Tramitup aplica las medidas técnicas y organizativas apropiadas para garantizar un nivel de seguridad adecuado al riesgo, incluyendo el cifrado de datos en tránsito y en reposo, controles de acceso, y procedimientos de revisión y actualización periódica de las medidas de seguridad, conforme al artículo 32 del RGPD.
            </p>
          </section>

          <section id="cookies">
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              8. Cookies
            </h2>
            <p>
              Tramitup utiliza cookies propias y de terceros para el funcionamiento técnico del Servicio, el análisis del uso de la plataforma y, en su caso, la personalización de la experiencia del Usuario. Para más información, puede consultar nuestra Política de Cookies disponible en el sitio web.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              9. Modificaciones de la política de privacidad
            </h2>
            <p>
              Tramitup se reserva el derecho de actualizar la presente Política de Privacidad para adaptarla a cambios legislativos o de negocio. Cualquier modificación relevante será comunicada al Usuario con antelación suficiente a través del correo electrónico registrado o mediante aviso destacado en la plataforma.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-[var(--text-dark)] mb-4">
              10. Contacto
            </h2>
            <p>
              Para cualquier consulta relativa al tratamiento de sus datos personales, puede contactar con Tramitup en:
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
