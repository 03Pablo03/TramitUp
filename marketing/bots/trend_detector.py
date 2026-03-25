"""
BOT 7: Trend Detector
━━━━━━━━━━━━━━━━━━━━━
Detecta tendencias legales en España y sugiere ideas de video oportunistas.

Fuentes:
  - Google Trends España
  - Noticias legales (BOE, periódicos)
  - Twitter/X trending topics
  - Reddit España

Output:
  - 3-5 ideas de video con gancho, ángulo y potencial viral
  - Priorizadas por oportunidad temporal

USO:
  python -m marketing.bots.trend_detector                      (búsqueda general)
  python -m marketing.bots.trend_detector --category laboral   (filtrar por tema)
  python -m marketing.bots.trend_detector --json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import BRAND, VOICE, CONTENT_BANK
from marketing.llm import ask

SYSTEM_PROMPT = f"""Eres un analista de tendencias y estratega de contenido para {BRAND['name']},
una app de asistencia legal en España. Tu trabajo es detectar temas trending relacionados
con derechos legales, leyes y trámites en España, y convertirlos en ideas de vídeo virales
para TikTok y Facebook.

Voz de marca: {VOICE['tone']}
Persona: {VOICE['persona']}

IMPORTANTE:
- Solo temas relevantes para España
- Prioriza cambios legislativos recientes, polémicas legales, noticias virales sobre derechos
- Cada idea debe tener un ángulo concreto que genere clicks
- Incluye siempre un dato legal real y verificable
- Formato de respuesta SIEMPRE en JSON válido"""

CATEGORIES = [t["topic"] for t in CONTENT_BANK]

SEARCH_QUERIES = {
    "general": [
        "nuevas leyes España 2024 2025",
        "derechos ciudadanos España noticias",
        "polémica legal España",
        "cambios legislativos BOE reciente",
        "viral derechos España TikTok",
    ],
    "laboral": [
        "reforma laboral España noticias",
        "derechos trabajadores España cambios",
        "despido ERE España reciente",
        "salario mínimo España",
    ],
    "alquiler": [
        "ley vivienda España noticias",
        "alquiler derechos inquilinos novedades",
        "regulación alquiler España",
        "desahucios España noticias",
    ],
    "multas": [
        "multas tráfico DGT novedades",
        "nuevas multas España",
        "radares DGT cambios",
    ],
    "consumo": [
        "derechos consumidor España noticias",
        "reclamaciones empresas España",
        "estafas consumo España",
    ],
    "herencias": [
        "impuesto sucesiones España cambios",
        "herencias España noticias",
        "testamento leyes España",
    ],
    "vuelos": [
        "aerolíneas reclamaciones España",
        "vuelos cancelados derechos pasajeros",
        "huelga aeropuertos España",
    ],
}


def detect_trends(category: str = None) -> dict:
    """Usa Claude para analizar tendencias y generar ideas de video."""
    cat = category or "general"
    queries = SEARCH_QUERIES.get(cat, SEARCH_QUERIES["general"])

    prompt = f"""Analiza las tendencias actuales en España sobre temas legales y derechos ciudadanos.
Fecha actual: {datetime.now().strftime('%d/%m/%Y')}

Categoría de búsqueda: {cat}
Queries de referencia: {', '.join(queries)}

Basándote en tu conocimiento de la actualidad española, genera exactamente 5 ideas de vídeo
oportunistas que podrían ser virales AHORA. Cada idea debe explotar una tendencia, noticia
reciente o tema candente.

Responde SOLO con un JSON válido (sin markdown, sin bloques de código) con esta estructura:
{{
  "trends_detected": [
    {{
      "trend": "descripción breve de la tendencia/noticia",
      "source_type": "legislación|noticia|polémica|viral|estacional",
      "urgency": "alta|media|baja"
    }}
  ],
  "video_ideas": [
    {{
      "rank": 1,
      "title": "título del vídeo (gancho)",
      "angle": "ángulo específico para abordar el tema",
      "hook_3s": "texto exacto para los 3 primeros segundos",
      "screen_text": "texto que aparece en pantalla",
      "legal_fact": "dato legal real y verificable que ancla el contenido",
      "format_suggested": "mito_vs_realidad|pregunta_viral|revelacion|consecuencias|etc",
      "viral_potential": "alto|medio",
      "why_now": "por qué este tema es oportuno ahora",
      "platform": "tiktok|facebook|ambas"
    }}
  ],
  "category": "{cat}",
  "generated_at": "{datetime.now().isoformat()}"
}}"""

    raw = ask(prompt, system=SYSTEM_PROMPT, max_tokens=3000)

    # Parse JSON from response
    try:
        # Try to extract JSON if wrapped in markdown
        if "```" in raw:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            raw = raw[start:end]
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "error": "No se pudo parsear la respuesta de Claude",
            "raw_response": raw[:500],
            "category": cat,
            "generated_at": datetime.now().isoformat(),
        }

    return result


def format_trends_readable(data: dict) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append(f"🔥 TREND DETECTOR — {data.get('category', 'general').upper()}")
    lines.append(f"   Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lines.append("=" * 70)

    if "error" in data:
        lines.append(f"\n❌ Error: {data['error']}")
        if "raw_response" in data:
            lines.append(f"   Respuesta: {data['raw_response'][:200]}...")
        return "\n".join(lines)

    lines.append("")
    lines.append("📡 TENDENCIAS DETECTADAS:")
    for t in data.get("trends_detected", []):
        urgency_icon = {"alta": "🔴", "media": "🟡", "baja": "🟢"}.get(t.get("urgency", ""), "⚪")
        lines.append(f"   {urgency_icon} [{t.get('source_type', '')}] {t.get('trend', '')}")

    lines.append("")
    lines.append("🎬 IDEAS DE VIDEO (por potencial viral):")
    for idea in data.get("video_ideas", []):
        lines.append("")
        lines.append(f"   #{idea.get('rank', '?')} — {idea.get('title', '')}")
        lines.append(f"      Angulo: {idea.get('angle', '')}")
        lines.append(f"      Gancho 3s: \"{idea.get('hook_3s', '')}\"")
        lines.append(f"      Pantalla: {idea.get('screen_text', '')}")
        lines.append(f"      Dato legal: {idea.get('legal_fact', '')}")
        lines.append(f"      Formato: {idea.get('format_suggested', '')} | Plataforma: {idea.get('platform', '')}")
        lines.append(f"      Potencial: {idea.get('viral_potential', '')} | Por que ahora: {idea.get('why_now', '')}")

    lines.append("")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Trend Detector Bot")
    parser.add_argument("--category", choices=CATEGORIES + ["general"], default="general",
                        help="Categoria de tendencias")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    args = parser.parse_args()

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    print(f"🔍 Buscando tendencias ({args.category})...")
    result = detect_trends(args.category)

    if args.json:
        out_file = output_dir / f"trends_{args.category}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"\n✅ Guardado en {out_file}")
    else:
        text = format_trends_readable(result)
        out_file = output_dir / f"trends_{args.category}_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(text)
        print(f"✅ Guardado en {out_file}")


if __name__ == "__main__":
    main()
