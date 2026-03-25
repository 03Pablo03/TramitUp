"""
BOT 11: FAQ Scraper
━━━━━━━━━━━━━━━━━━━
Busca preguntas frecuentes reales sobre temas legales en España.

Fuentes simuladas (via Claude):
  - Grupos de Facebook (inquilinos, laborales, consumo)
  - Reddit España (r/spain, r/askspain, r/legalspain)
  - Foros legales españoles
  - Google "People Also Ask"

Output:
  - Lista priorizada de preguntas con volumen estimado
  - Categorizada por tema
  - Sugerencia de angulo para video

USO:
  python -m marketing.bots.faq_scraper --category alquiler
  python -m marketing.bots.faq_scraper --category laboral --limit 10
  python -m marketing.bots.faq_scraper --all
  python -m marketing.bots.faq_scraper --all --json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import BRAND, CONTENT_BANK
from marketing.llm import ask

SYSTEM_PROMPT = f"""Eres un investigador de mercado especializado en temas legales en España.
Tu trabajo es identificar las preguntas más frecuentes y buscadas que la gente real hace
sobre sus derechos legales, y convertirlas en oportunidades de contenido para {BRAND['name']}.

FUENTES QUE ANALIZAS:
- Grupos de Facebook: inquilinos, trabajadores, consumidores, autónomos
- Reddit España: r/spain, r/askspain, r/legalspain, r/SpainPolitics
- Foros legales: iAbogado, LegalToday, ForoJurídico
- Google People Also Ask: búsquedas relacionadas
- Yahoo Respuestas / Quora en español

CRITERIOS DE PRIORIZACIÓN:
1. Volumen de búsqueda estimado (cuánta gente se lo pregunta)
2. Potencial viral (¿la respuesta es sorprendente o poco conocida?)
3. Relevancia temporal (¿es más relevante ahora?)
4. Potencial de engagement (¿genera debate en comentarios?)

IMPORTANTE: Responde SIEMPRE en JSON válido sin bloques de código markdown."""

CATEGORIES = {
    "alquiler": "derechos inquilinos, caseros, contratos de alquiler, fianza, desahucios, subida de alquiler",
    "laboral": "despido, derechos trabajadores, vacaciones, finiquito, horas extra, baja laboral, ERE",
    "multas": "multas de tráfico, DGT, radar, recurrir multas, descuentos, puntos carnet",
    "consumo": "devoluciones, reclamaciones, garantía, compras online, factura incorrecta",
    "herencias": "herencias, testamento, impuesto sucesiones, plusvalía, renuncia herencia",
    "vuelos": "vuelos cancelados, retraso vuelo, compensación, overbooking, reclamación aerolínea",
    "tramites": "trámites gratuitos, burocracia, administración, Seguridad Social, Hacienda",
    "autonomos": "autónomos, alta autónomo, cuota, facturación, impuestos, IVA",
    "familia": "divorcio, custodia, pensión alimentos, violencia género, parejas de hecho",
}


def scrape_faqs(category: str, limit: int = 8) -> dict:
    """Busca FAQs reales sobre un tema legal."""
    description = CATEGORIES.get(category, category)

    prompt = f"""Genera las {limit} preguntas más frecuentes y buscadas en España sobre: {category}
(contexto: {description})

Piensa como si estuvieras leyendo grupos de Facebook, hilos de Reddit, y resultados de
Google "People Also Ask" sobre este tema. Las preguntas deben ser REALES, las que gente
normal (no abogados) haría.

Responde SOLO con JSON válido:
{{
  "category": "{category}",
  "total_questions": {limit},
  "questions": [
    {{
      "rank": 1,
      "question": "la pregunta tal como la haría una persona normal",
      "search_volume_estimate": "alto|medio|bajo",
      "sources_likely": ["facebook_groups", "reddit", "google_paa", "foros"],
      "surprise_factor": "alto|medio|bajo (¿la respuesta es sorprendente?)",
      "viral_potential": "alto|medio|bajo",
      "legal_answer_summary": "respuesta legal breve y precisa (1-2 frases)",
      "video_angle": {{
        "title_suggestion": "título para vídeo TikTok/Facebook",
        "format_suggestion": "mito_vs_realidad|pregunta_viral|revelacion|tutorial_rapido|etc",
        "hook_3s": "gancho para los primeros 3 segundos del vídeo"
      }},
      "engagement_potential": "por qué generaría debate en comentarios",
      "seasonality": "siempre_relevante|estacional|actualidad"
    }}
  ],
  "meta": {{
    "most_underserved_topic": "el subtema con más demanda y menos contenido disponible",
    "quick_win": "la pregunta más fácil de convertir en vídeo viral",
    "content_gap": "tema que nadie está cubriendo bien"
  }}
}}"""

    raw = ask(prompt, system=SYSTEM_PROMPT, max_tokens=3500)

    try:
        if "```" in raw:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            raw = raw[start:end]
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "error": "No se pudo parsear la respuesta",
            "raw_response": raw[:500],
            "category": category,
        }

    result["generated_at"] = datetime.now().isoformat()
    return result


def scrape_all_categories(limit_per_cat: int = 5) -> list:
    """Scrape FAQs de todas las categorías."""
    results = []
    for cat in CATEGORIES:
        print(f"   🔍 {cat}...")
        results.append(scrape_faqs(cat, limit_per_cat))
    return results


def format_faqs_readable(data: dict) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append(f"🔍 FAQ SCRAPER — {data.get('category', '?').upper()}")
    lines.append(f"   Preguntas: {data.get('total_questions', '?')}")
    lines.append("=" * 70)

    if "error" in data:
        lines.append(f"\n❌ Error: {data['error']}")
        return "\n".join(lines)

    for q in data.get("questions", []):
        vol_icon = {"alto": "🔴", "medio": "🟡", "bajo": "🟢"}.get(q.get("search_volume_estimate", ""), "⚪")
        viral_icon = {"alto": "🚀", "medio": "📈", "bajo": "📊"}.get(q.get("viral_potential", ""), "⚪")

        lines.append("")
        lines.append(f"   #{q.get('rank', '?')} {vol_icon} {q.get('question', '')}")
        lines.append(f"      Volumen: {q.get('search_volume_estimate', '?')} | "
                     f"Viral: {q.get('viral_potential', '?')} {viral_icon} | "
                     f"Sorpresa: {q.get('surprise_factor', '?')}")
        lines.append(f"      Fuentes: {', '.join(q.get('sources_likely', []))}")
        lines.append(f"      Respuesta legal: {q.get('legal_answer_summary', '')}")

        va = q.get("video_angle", {})
        lines.append(f"      🎬 Video: {va.get('title_suggestion', '')}")
        lines.append(f"         Formato: {va.get('format_suggestion', '')} | Gancho: \"{va.get('hook_3s', '')}\"")
        lines.append(f"      💬 Engagement: {q.get('engagement_potential', '')}")

    meta = data.get("meta", {})
    if meta:
        lines.append("")
        lines.append("📊 INSIGHTS:")
        lines.append(f"   Tema menos cubierto: {meta.get('most_underserved_topic', '')}")
        lines.append(f"   Quick win: {meta.get('quick_win', '')}")
        lines.append(f"   Content gap: {meta.get('content_gap', '')}")

    lines.append("")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="FAQ Scraper Bot")
    parser.add_argument("--category", choices=list(CATEGORIES.keys()), help="Categoría")
    parser.add_argument("--limit", type=int, default=8, help="Número de preguntas (default: 8)")
    parser.add_argument("--all", action="store_true", help="Todas las categorías")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    args = parser.parse_args()

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if args.all:
        print(f"🔍 Scrapeando FAQs de {len(CATEGORIES)} categorías...")
        results = scrape_all_categories(args.limit)

        total_qs = sum(len(r.get("questions", [])) for r in results if "error" not in r)
        if args.json:
            out_file = output_dir / f"faqs_all_{datetime.now().strftime('%Y%m%d')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n✅ {total_qs} preguntas de {len(CATEGORIES)} categorías guardadas en {out_file}")
        else:
            full_text = "\n".join(format_faqs_readable(r) for r in results)
            out_file = output_dir / f"faqs_all_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            for r in results:
                print(format_faqs_readable(r))
            print(f"\n✅ {total_qs} preguntas guardadas en {out_file}")

    elif args.category:
        print(f"🔍 Buscando FAQs sobre {args.category}...")
        result = scrape_faqs(args.category, args.limit)
        if args.json:
            out_file = output_dir / f"faqs_{args.category}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print(f"\n✅ Guardado en {out_file}")
        else:
            text = format_faqs_readable(result)
            print(text)
            out_file = output_dir / f"faqs_{args.category}_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ Guardado en {out_file}")
    else:
        parser.print_help()
        print(f"\nCategorías disponibles: {', '.join(CATEGORIES.keys())}")


if __name__ == "__main__":
    main()
