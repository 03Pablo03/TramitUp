import Link from "next/link";
import { LandingNav } from "./LandingNav";
import { LegalNotice } from "./LegalNotice";
import { Footer } from "./Footer";

export type SEOLandingProps = {
  title: string;
  description: string;
  h1: string;
  intro: string;
  steps?: { title: string; content: string }[];
  lawRefs?: string[];
  faqs?: { q: string; a: string }[];
  ctaText?: string;
};

export function SEOLandingTemplate({
  title,
  description,
  h1,
  intro,
  steps = [],
  lawRefs = [],
  faqs = [],
  ctaText = "Genera tu modelo de reclamación gratis →",
}: SEOLandingProps) {
  return (
    <div className="min-h-screen bg-white">
      <LandingNav />
      <main className="mx-auto max-w-3xl px-4 py-16">
        <article>
          <h1 className="font-display text-3xl font-bold text-[var(--text-dark)] sm:text-4xl">
            {h1}
          </h1>
          <p className="mt-6 text-lg leading-relaxed text-[var(--text-body)]">
            {intro}
          </p>

          {steps.length > 0 && (
            <section className="mt-12">
              <h2 className="font-display text-2xl font-semibold text-[var(--text-dark)]">
                Proceso paso a paso
              </h2>
              <ol className="mt-6 space-y-6">
                {steps.map((step, i) => (
                  <li key={i}>
                    <h3 className="font-semibold text-[var(--text-dark)]">
                      {i + 1}. {step.title}
                    </h3>
                    <p className="mt-1 text-[var(--text-body)]">{step.content}</p>
                  </li>
                ))}
              </ol>
            </section>
          )}

          {lawRefs.length > 0 && (
            <section className="mt-12">
              <h2 className="font-display text-2xl font-semibold text-[var(--text-dark)]">
                Referencias legales
              </h2>
              <ul className="mt-4 space-y-2 font-mono text-sm text-[var(--text-body)]">
                {lawRefs.map((ref, i) => (
                  <li key={i}>{ref}</li>
                ))}
              </ul>
            </section>
          )}

          <div className="mt-12 rounded-xl bg-[var(--primary-light)] p-8 text-center">
            <p className="font-display text-xl font-semibold text-[var(--text-dark)]">
              ¿Listo para reclamar?
            </p>
            <p className="mt-2 text-[var(--text-body)]">
              Tramitup genera tu modelo personalizado en segundos.
            </p>
            <Link
              href="/login"
              className="mt-6 inline-flex rounded-xl bg-[var(--primary)] px-8 py-4 font-semibold text-white hover:bg-[var(--primary-dark)]"
            >
              {ctaText}
            </Link>
          </div>

          {faqs.length > 0 && (
            <section className="mt-16">
              <h2 className="font-display text-2xl font-semibold text-[var(--text-dark)]">
                Preguntas frecuentes
              </h2>
              <dl className="mt-6 space-y-6">
                {faqs.map((faq, i) => (
                  <div key={i}>
                    <dt className="font-semibold text-[var(--text-dark)]">{faq.q}</dt>
                    <dd className="mt-2 text-[var(--text-body)]">{faq.a}</dd>
                  </div>
                ))}
              </dl>
            </section>
          )}
        </article>
      </main>
      <LegalNotice />
      <Footer />
    </div>
  );
}
