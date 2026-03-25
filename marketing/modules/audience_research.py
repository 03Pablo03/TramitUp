"""
Module 1.2: Audience Research Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Investiga preguntas reales de la audiencia sobre temas legales en España.

Fuentes:
  - Reddit España (r/spain, r/askspain, r/legalspain)
  - Google People Also Ask
  - Foros (Idealista, Forocoches sección legal)
  - Grupos de Facebook (simulado via Claude)

Output: Base de datos de FAQs categorizadas con ángulo de vídeo.
"""

import json
import re
import time
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError

from marketing.core.config_loader import get, get_categories
from marketing.core.database import insert_faq, query, log_operation, db
from marketing.core.llm import ask_json
from marketing.core.logger import get_logger

log = get_logger("audience_research")

SYSTEM_PROMPT = """Eres un investigador de mercado especializado en temas legales en España.
Analizas fuentes reales (Reddit, foros, Google) para encontrar las preguntas que la gente
REALMENTE se hace sobre sus derechos. Tu objetivo es identificar oportunidades de contenido
para TramitUp.

IMPORTANTE:
- Las preguntas deben ser REALES (como las haría una persona normal, no un abogado)
- Detecta el LENGUAJE real que usa la gente (para copiar su tono en los vídeos)
- Prioriza por: volumen + potencial viral + si la respuesta es sorprendente
- Responde SIEMPRE en JSON válido sin bloques de código markdown"""


# ─── Scrapers ────────────────────────────────────────────────────────────────

def _fetch(url: str, timeout: int = 10) -> str:
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    try:
        return urlopen(req, timeout=timeout).read().decode("utf-8", errors="replace")
    except (URLError, OSError) as e:
        log.warning(f"Fetch failed {url}: {e}")
        return ""


def scrape_reddit_es(category: str) -> list[dict]:
    """Scrape Reddit España para preguntas legales."""
    log.info(f"Scraping Reddit for '{category}'...")
    items = []

    cat_config = next((c for c in get_categories() if c["id"] == category), None)
    keywords = cat_config["keywords"] if cat_config else [category]

    subreddits = ["spain", "askspain", "SpainPolitics"]
    for sub in subreddits:
        for kw in keywords[:2]:
            url = f"https://www.reddit.com/r/{sub}/search.json?q={kw}&restrict_sr=1&sort=relevance&t=year&limit=10"
            raw = _fetch(url)
            if not raw:
                continue
            try:
                data = json.loads(raw)
                posts = data.get("data", {}).get("children", [])
                for post in posts:
                    d = post.get("data", {})
                    title = d.get("title", "")
                    if title and len(title) > 10:
                        items.append({
                            "source": f"reddit_r/{sub}",
                            "text": title,
                            "score": d.get("score", 0),
                            "comments": d.get("num_comments", 0),
                        })
            except json.JSONDecodeError:
                pass

    log.info(f"Reddit: {len(items)} posts found for '{category}'")
    return items


def scrape_google_paa(category: str) -> list[dict]:
    """Scrape Google People Also Ask (via search suggest)."""
    log.info(f"Scraping Google suggestions for '{category}'...")
    items = []

    cat_config = next((c for c in get_categories() if c["id"] == category), None)
    keywords = cat_config["keywords"] if cat_config else [category]

    for kw in keywords[:3]:
        for prefix in ["", "cómo ", "puedo ", "es legal ", "qué pasa si "]:
            query_str = f"{prefix}{kw} España"
            url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl=es&gl=es&q={query_str.replace(' ', '+')}"
            raw = _fetch(url)
            if raw:
                try:
                    data = json.loads(raw)
                    suggestions = data[1] if len(data) > 1 else []
                    for s in suggestions:
                        if s and len(s) > 10 and s != query_str:
                            items.append({
                                "source": "google_suggest",
                                "text": s,
                            })
                except (json.JSONDecodeError, IndexError):
                    pass

    log.info(f"Google: {len(items)} suggestions for '{category}'")
    return items


# ─── Analysis ────────────────────────────────────────────────────────────────

def analyze_audience(category: str, raw_items: list[dict]) -> dict:
    """Analiza preguntas reales y genera FAQs priorizadas."""
    cat_config = next((c for c in get_categories() if c["id"] == category), None)
    label = cat_config["label"] if cat_config else category

    items_text = "\n".join(
        f"- [{it.get('source', '?')}] {it.get('text', '?')} "
        f"{'(score: ' + str(it.get('score', '')) + ', comments: ' + str(it.get('comments', '')) + ')' if it.get('score') else ''}"
        for it in raw_items[:40]
    )

    prompt = f"""Analiza estas preguntas/búsquedas REALES de españoles sobre {label}.

FUENTES REALES RECOGIDAS:
{items_text if items_text.strip() else '(no se pudieron recoger fuentes, genera basándote en tu conocimiento)'}

Genera las 10 preguntas más frecuentes y útiles para crear contenido.
Para cada una, incluye el LENGUAJE REAL que usa la gente (coloquial, no formal).

Responde SOLO con JSON válido:
{{
  "category": "{category}",
  "faqs": [
    {{
      "question": "la pregunta tal como la haría una persona normal",
      "language_sample": "frase textual como la diría alguien real (ej: 'tío me quieren echar del piso')",
      "search_volume": "alto|medio|bajo",
      "surprise_factor": "alto|medio|bajo",
      "viral_potential": "alto|medio|bajo",
      "answer_summary": "respuesta legal breve (1-2 frases con datos reales)",
      "sources": ["reddit", "google", "foro"],
      "video_angle": {{
        "title": "título para TikTok",
        "hook": "gancho 3 segundos",
        "format": "pregunta_viral|mito_vs_realidad|revelacion|tutorial|consecuencias"
      }},
      "pain_point": "el dolor/frustración subyacente"
    }}
  ],
  "audience_insights": {{
    "common_emotions": ["frustración", "miedo", "confusión"],
    "language_patterns": ["palabras y expresiones que repiten"],
    "misconceptions": ["ideas erróneas más comunes"],
    "underserved_topics": ["temas que preguntan pero nadie responde bien"]
  }}
}}"""

    return ask_json(prompt, system=SYSTEM_PROMPT, max_tokens=4000)


# ─── Pipeline ────────────────────────────────────────────────────────────────

def research(category: str, save: bool = True) -> dict:
    """Pipeline completo de investigación de audiencia para una categoría."""
    start = time.time()
    log.info(f"Starting audience research for '{category}'")

    # Scrape sources
    raw_items = []
    raw_items.extend(scrape_reddit_es(category))
    raw_items.extend(scrape_google_paa(category))

    log.info(f"Total raw items for '{category}': {len(raw_items)}")

    # Analyze with Claude
    result = analyze_audience(category, raw_items)

    # Save to DB
    if save and "faqs" in result:
        for faq in result["faqs"]:
            insert_faq(
                category=category,
                question=faq["question"],
                source=", ".join(faq.get("sources", [])),
                search_volume=faq.get("search_volume", "medio"),
                viral_potential=faq.get("viral_potential", "medio"),
                answer_summary=faq.get("answer_summary"),
                video_angle=faq.get("video_angle"),
            )

        # Save audience insights
        insights = result.get("audience_insights", {})
        for pain in result["faqs"]:
            if pain.get("pain_point"):
                try:
                    with db() as conn:
                        conn.execute("""
                            INSERT INTO audience_insights (category, pain_point, language_used, source)
                            VALUES (?, ?, ?, ?)
                            ON CONFLICT(category, pain_point) DO UPDATE SET
                                language_used = excluded.language_used
                        """, (category, pain["pain_point"],
                              pain.get("language_sample", ""),
                              ", ".join(pain.get("sources", []))))
                except Exception:
                    pass

    duration = int((time.time() - start) * 1000)
    log_operation("audience_research", "audience_research", "success",
                  f"category={category} raw={len(raw_items)} faqs={len(result.get('faqs', []))}", duration)

    result["meta"] = {
        "category": category,
        "sources_scraped": len(raw_items),
        "generated_at": datetime.now().isoformat(),
        "duration_ms": duration,
    }
    return result


def research_all(save: bool = True) -> list[dict]:
    """Investiga todas las categorías."""
    results = []
    for cat in get_categories():
        log.info(f"Researching {cat['id']}...")
        results.append(research(cat["id"], save))
    return results


def get_top_faqs(category: str = None, limit: int = 10) -> list[dict]:
    """FAQs top de la DB."""
    if category:
        return query("""
            SELECT * FROM faqs WHERE category = ?
            ORDER BY
                CASE viral_potential WHEN 'alto' THEN 1 WHEN 'medio' THEN 2 ELSE 3 END,
                times_seen DESC
            LIMIT ?
        """, (category, limit))
    return query("""
        SELECT * FROM faqs
        ORDER BY
            CASE viral_potential WHEN 'alto' THEN 1 WHEN 'medio' THEN 2 ELSE 3 END,
            times_seen DESC
        LIMIT ?
    """, (limit,))


def format_readable(data: dict) -> str:
    lines = []
    cat = data.get("category", data.get("meta", {}).get("category", "?"))
    lines.append("=" * 70)
    lines.append(f"🔍 AUDIENCE RESEARCH — {cat.upper()}")
    meta = data.get("meta", {})
    lines.append(f"   Fuentes: {meta.get('sources_scraped', '?')} | "
                 f"Duración: {meta.get('duration_ms', '?')}ms")
    lines.append("=" * 70)

    for i, faq in enumerate(data.get("faqs", []), 1):
        vol = {"alto": "🔴", "medio": "🟡", "bajo": "🟢"}.get(faq.get("search_volume"), "⚪")
        viral = {"alto": "🚀", "medio": "📈", "bajo": "📊"}.get(faq.get("viral_potential"), "⚪")

        lines.append(f"\n{vol} #{i} {faq.get('question', '?')}")
        lines.append(f"   Volumen: {faq.get('search_volume', '?')} | Viral: {faq.get('viral_potential', '?')} {viral}")
        if faq.get("language_sample"):
            lines.append(f"   💬 Real: \"{faq['language_sample']}\"")
        lines.append(f"   ⚖️  Respuesta: {faq.get('answer_summary', '?')}")

        va = faq.get("video_angle", {})
        if va:
            lines.append(f"   🎬 Vídeo: {va.get('title', '?')}")
            lines.append(f"      Gancho: \"{va.get('hook', '?')}\" | Formato: {va.get('format', '?')}")

        if faq.get("pain_point"):
            lines.append(f"   😤 Pain point: {faq['pain_point']}")

    insights = data.get("audience_insights", {})
    if insights:
        lines.append("\n📊 INSIGHTS DE AUDIENCIA:")
        if insights.get("common_emotions"):
            lines.append(f"   Emociones: {', '.join(insights['common_emotions'])}")
        if insights.get("misconceptions"):
            lines.append(f"   Ideas erróneas: {', '.join(insights['misconceptions'][:3])}")
        if insights.get("underserved_topics"):
            lines.append(f"   Temas sin cubrir: {', '.join(insights['underserved_topics'][:3])}")

    lines.append("")
    return "\n".join(lines)
