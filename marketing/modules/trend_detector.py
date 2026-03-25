"""
Module 1.1: Trend Detector
━━━━━━━━━━━━━━━━━━━━━━━━━━
Detecta tendencias legales en España en tiempo real.

Fuentes:
  - Google Trends España (scrape RSS/API)
  - BOE — Boletín Oficial del Estado (scrape nuevas leyes)
  - Noticias legales (El País, 20 Minutos, La Vanguardia)
  - Hashtags trending en TikTok/Twitter
  - Claude para análisis y priorización

Output: Tendencias priorizadas con ideas de vídeo.
"""

import json
import re
import time
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import URLError

from marketing.core.config_loader import get, get_category_ids
from marketing.core.database import insert_trend, query, log_operation
from marketing.core.llm import ask_json
from marketing.core.logger import get_logger

log = get_logger("trend_detector")

SYSTEM_PROMPT = """Eres un analista de tendencias especializado en temas legales en España.
Tu trabajo es analizar fuentes de noticias y detectar oportunidades de contenido viral
para TramitUp (app de asistencia legal).

REGLAS:
- Solo temas relevantes para España
- Prioriza: cambios legislativos, polémicas legales, noticias virales sobre derechos
- Cada idea debe tener un dato legal REAL y verificable
- Evalúa la ventana de oportunidad (cuánto tiempo es relevante)
- Responde SIEMPRE en JSON válido sin bloques de código markdown"""


# ─── Source scrapers ─────────────────────────────────────────────────────────

def _fetch_url(url: str, timeout: int = 10) -> str:
    """Fetch URL content with user agent."""
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    try:
        resp = urlopen(req, timeout=timeout)
        return resp.read().decode("utf-8", errors="replace")
    except (URLError, OSError) as e:
        log.warning(f"Fetch failed {url}: {e}")
        return ""


def scrape_boe() -> list[dict]:
    """Scrape BOE para nuevas disposiciones."""
    log.info("Scraping BOE...")
    html = _fetch_url("https://www.boe.es/diario_boe/")
    if not html:
        return []

    # Extract titles from BOE HTML
    items = []
    # BOE uses <h5> and <p class="titulo"> for entries
    title_matches = re.findall(
        r'<(?:h5|p\s+class="titulo")[^>]*>(.*?)</(?:h5|p)>', html, re.DOTALL
    )
    for title in title_matches[:20]:
        clean = re.sub(r'<[^>]+>', '', title).strip()
        if len(clean) > 20:
            items.append({
                "source": "boe",
                "title": clean[:200],
                "url": "https://www.boe.es/diario_boe/",
            })

    log.info(f"BOE: {len(items)} items found")
    return items


def scrape_google_trends_es() -> list[dict]:
    """Scrape Google Trends España via RSS feed."""
    log.info("Scraping Google Trends ES...")
    rss = _fetch_url("https://trends.google.es/trending/rss?geo=ES")
    if not rss:
        return []

    items = []
    titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', rss)
    traffic = re.findall(r'<ht:approx_traffic>(.*?)</ht:approx_traffic>', rss)

    for i, title in enumerate(titles[:15]):
        vol = traffic[i] if i < len(traffic) else "?"
        items.append({
            "source": "google_trends",
            "title": title,
            "volume": vol,
        })

    log.info(f"Google Trends: {len(items)} items found")
    return items


def scrape_news_legal() -> list[dict]:
    """Scrape noticias legales de periódicos españoles."""
    log.info("Scraping news sites...")
    items = []

    # El País Legal
    html = _fetch_url("https://elpais.com/noticias/legislacion/")
    if html:
        titles = re.findall(r'<h2[^>]*>.*?<a[^>]*>(.*?)</a>.*?</h2>', html, re.DOTALL)
        for t in titles[:10]:
            clean = re.sub(r'<[^>]+>', '', t).strip()
            if len(clean) > 15:
                items.append({"source": "elpais", "title": clean[:200]})

    # 20 Minutos
    html = _fetch_url("https://www.20minutos.es/minuteca/legislacion/")
    if html:
        titles = re.findall(r'<h[23][^>]*>.*?<a[^>]*>(.*?)</a>.*?</h[23]>', html, re.DOTALL)
        for t in titles[:10]:
            clean = re.sub(r'<[^>]+>', '', t).strip()
            if len(clean) > 15:
                items.append({"source": "20minutos", "title": clean[:200]})

    log.info(f"News: {len(items)} items found")
    return items


# ─── Analysis with Claude ────────────────────────────────────────────────────

def analyze_trends(raw_items: list[dict], category: str = None) -> dict:
    """Usa Claude para analizar y priorizar tendencias."""
    categories = get_category_ids()

    items_text = "\n".join(
        f"- [{it.get('source', '?')}] {it.get('title', '?')} "
        f"{'(vol: ' + it.get('volume', '') + ')' if it.get('volume') else ''}"
        for it in raw_items[:30]
    )

    prompt = f"""Analiza estas tendencias/noticias recientes de España y selecciona las 5 más
relevantes para crear contenido sobre derechos legales y trámites.

FECHA: {datetime.now().strftime('%d/%m/%Y')}
{f'FILTRO CATEGORÍA: {category}' if category else f'CATEGORÍAS DISPONIBLES: {", ".join(categories)}'}

FUENTES RECOGIDAS:
{items_text}

Si las fuentes no tienen contenido útil, genera tendencias basándote en tu conocimiento
de la actualidad legal española.

Responde SOLO con JSON válido:
{{
  "trends": [
    {{
      "title": "título corto de la tendencia",
      "category": "categoría ({', '.join(categories)})",
      "description": "qué está pasando y por qué importa",
      "source_type": "legislacion|noticia|polemica|viral|estacional",
      "urgency": "alta|media|baja",
      "viral_potential": "alto|medio|bajo",
      "window_hours": 72,
      "video_ideas": [
        {{
          "title": "título viral para TikTok",
          "hook_3s": "gancho primeros 3 segundos",
          "format": "mito_vs_realidad|pregunta_viral|revelacion|tutorial_rapido|pov_storytelling|consecuencias",
          "legal_fact": "dato legal verificable",
          "platform": "tiktok|facebook|ambas"
        }}
      ]
    }}
  ],
  "summary": "resumen de 1 frase del panorama actual"
}}"""

    return ask_json(prompt, system=SYSTEM_PROMPT, max_tokens=3000)


# ─── Main pipeline ──────────────────────────────────────────────────────────

def detect(category: str = None, save: bool = True) -> dict:
    """Pipeline completo de detección de tendencias."""
    start = time.time()
    log.info(f"Starting trend detection (category={category})")

    # 1. Scrape all sources
    raw_items = []
    raw_items.extend(scrape_google_trends_es())
    raw_items.extend(scrape_boe())
    raw_items.extend(scrape_news_legal())

    log.info(f"Total raw items: {len(raw_items)}")

    # 2. Analyze with Claude
    result = analyze_trends(raw_items, category)

    # 3. Save to DB
    if save and "trends" in result:
        for trend in result["trends"]:
            insert_trend(
                source=trend.get("source_type", "analysis"),
                title=trend["title"],
                description=trend.get("description"),
                category=trend.get("category"),
                urgency=trend.get("urgency", "media"),
                viral_potential=trend.get("viral_potential", "medio"),
                expires_at=(datetime.now() + timedelta(hours=trend.get("window_hours", 72))).isoformat(),
                metadata={"video_ideas": trend.get("video_ideas", [])},
            )

    duration = int((time.time() - start) * 1000)
    log_operation("trend_detection", "trend_detector", "success",
                  f"raw={len(raw_items)} trends={len(result.get('trends', []))}", duration)

    result["meta"] = {
        "sources_scraped": len(raw_items),
        "category_filter": category,
        "generated_at": datetime.now().isoformat(),
        "duration_ms": duration,
    }
    return result


def get_active_trends(limit: int = 10) -> list[dict]:
    """Devuelve tendencias activas (no expiradas) de la DB."""
    return query("""
        SELECT * FROM trends
        WHERE status = 'new' AND (expires_at IS NULL OR expires_at > datetime('now'))
        ORDER BY
            CASE urgency WHEN 'alta' THEN 1 WHEN 'media' THEN 2 ELSE 3 END,
            detected_at DESC
        LIMIT ?
    """, (limit,))


def format_readable(data: dict) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append(f"🔥 TREND DETECTOR — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    meta = data.get("meta", {})
    lines.append(f"   Fuentes: {meta.get('sources_scraped', '?')} | "
                 f"Duración: {meta.get('duration_ms', '?')}ms")
    if data.get("summary"):
        lines.append(f"   Resumen: {data['summary']}")
    lines.append("=" * 70)

    for i, t in enumerate(data.get("trends", []), 1):
        urg = {"alta": "🔴", "media": "🟡", "baja": "🟢"}.get(t.get("urgency"), "⚪")
        lines.append(f"\n{urg} #{i} [{t.get('category', '?')}] {t.get('title', '?')}")
        lines.append(f"   {t.get('description', '')}")
        lines.append(f"   Potencial: {t.get('viral_potential', '?')} | "
                     f"Ventana: {t.get('window_hours', '?')}h")

        for idea in t.get("video_ideas", []):
            lines.append(f"   🎬 {idea.get('title', '?')}")
            lines.append(f"      Gancho: \"{idea.get('hook_3s', '?')}\"")
            lines.append(f"      Formato: {idea.get('format', '?')} | Dato: {idea.get('legal_fact', '?')}")

    lines.append("")
    return "\n".join(lines)
