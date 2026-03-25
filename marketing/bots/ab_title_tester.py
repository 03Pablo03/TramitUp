"""
BOT 10: A/B Title Tester
━━━━━━━━━━━━━━━━━━━━━━━━
Genera variantes de titulo/gancho optimizadas para viralidad.

Analiza patrones:
  - Pregunta vs afirmacion
  - Uso de numeros
  - Generacion de curiosidad
  - Negacion ("NO hagas esto")
  - Urgencia y FOMO

Output:
  - 4 variantes ordenadas por potencial viral
  - Texto en pantalla sugerido (primeros 3 segundos)
  - Explicacion de por que funciona cada variante

USO:
  python -m marketing.bots.ab_title_tester --topic multas --angle "descuento 50% en multas"
  python -m marketing.bots.ab_title_tester --topic alquiler
  python -m marketing.bots.ab_title_tester --topic laboral --angle "te despiden sin preaviso" --json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import BRAND, VOICE, CONTENT_BANK
from marketing.llm import ask

SYSTEM_PROMPT = f"""Eres un experto en copywriting viral y títulos de vídeo para {BRAND['name']},
una app de asistencia legal en España. Tu especialidad es crear títulos que maximizan
el CTR (click-through rate) y la retención en los primeros 3 segundos.

Voz de marca: {VOICE['tone']}

PATRONES VIRALES QUE DOMINAS:
1. Pregunta directa: "¿Sabías que...?" → genera curiosidad
2. Negación/Prohibición: "NO pagues esa multa" → genera urgencia
3. Números concretos: "3 cosas que tu casero NO puede hacer" → promete estructura
4. Revelación: "Lo que NADIE te cuenta sobre..." → genera intriga
5. POV/Situación: "POV: descubres que..." → genera identificación
6. Consecuencias: "¿Qué pasa si no pagas...?" → genera miedo productivo
7. Comparación: "Lo que crees vs lo que dice la ley" → genera sorpresa
8. Urgencia temporal: "Tienes 20 DÍAS para hacer esto" → genera FOMO

IMPORTANTE: Responde SIEMPRE en JSON válido sin bloques de código markdown."""


def generate_title_variants(topic: str, angle: str = None) -> dict:
    """Genera 4 variantes de titulo optimizadas para viralidad."""
    # Get topic data for context
    topic_data = None
    for item in CONTENT_BANK:
        if item["topic"] == topic:
            topic_data = item
            break

    facts = topic_data["facts"] if topic_data else []
    hooks = topic_data["hooks"] if topic_data else []

    prompt = f"""Genera 4 variantes de título/gancho para un vídeo de TikTok sobre "{topic}".
{f'Ángulo específico: {angle}' if angle else ''}

Datos legales disponibles para inspiración:
{json.dumps(facts, ensure_ascii=False)}

Hooks existentes (NO repetir, solo como referencia de estilo):
{json.dumps(hooks, ensure_ascii=False)}

Para cada variante, usa un PATRÓN DIFERENTE:
- Variante 1: Patrón de pregunta o curiosidad
- Variante 2: Patrón de negación/prohibición
- Variante 3: Patrón con números o datos
- Variante 4: Patrón de consecuencias o revelación

Responde SOLO con JSON válido:
{{
  "topic": "{topic}",
  "angle": "{angle or 'general'}",
  "variants": [
    {{
      "rank": 1,
      "title": "el título completo",
      "pattern_used": "nombre del patrón viral usado",
      "screen_text_3s": "TEXTO EXACTO que aparece en pantalla los 3 primeros segundos (MAYÚSCULAS, corto, impactante)",
      "why_it_works": "explicación breve de por qué esta variante funciona psicológicamente",
      "estimated_ctr": "alto|medio-alto|medio",
      "best_for": "tiktok|facebook|ambas",
      "opening_line": "primera frase que diría la persona en el vídeo"
    }},
    {{
      "rank": 2,
      "title": "...",
      "pattern_used": "...",
      "screen_text_3s": "...",
      "why_it_works": "...",
      "estimated_ctr": "...",
      "best_for": "...",
      "opening_line": "..."
    }},
    {{
      "rank": 3,
      "title": "...",
      "pattern_used": "...",
      "screen_text_3s": "...",
      "why_it_works": "...",
      "estimated_ctr": "...",
      "best_for": "...",
      "opening_line": "..."
    }},
    {{
      "rank": 4,
      "title": "...",
      "pattern_used": "...",
      "screen_text_3s": "...",
      "why_it_works": "...",
      "estimated_ctr": "...",
      "best_for": "...",
      "opening_line": "..."
    }}
  ],
  "recommendation": "cuál elegirías y por qué (1 frase)",
  "ab_test_plan": "cómo testear estas variantes para encontrar la ganadora"
}}"""

    raw = ask(prompt, system=SYSTEM_PROMPT, max_tokens=2500)

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
            "topic": topic,
        }

    result["generated_at"] = datetime.now().isoformat()
    return result


def format_variants_readable(data: dict) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append(f"🧪 A/B TITLE TESTER — {data.get('topic', '?').upper()}")
    lines.append(f"   Angulo: {data.get('angle', 'general')}")
    lines.append("=" * 70)

    if "error" in data:
        lines.append(f"\n❌ Error: {data['error']}")
        return "\n".join(lines)

    for v in data.get("variants", []):
        ctr_icon = {"alto": "🟢", "medio-alto": "🟡", "medio": "🟠"}.get(v.get("estimated_ctr", ""), "⚪")
        lines.append("")
        lines.append(f"   #{v.get('rank', '?')} {ctr_icon} {v.get('title', '')}")
        lines.append(f"      Patron: {v.get('pattern_used', '')}")
        lines.append(f"      Pantalla 3s: [{v.get('screen_text_3s', '')}]")
        lines.append(f"      Opening: \"{v.get('opening_line', '')}\"")
        lines.append(f"      Por que funciona: {v.get('why_it_works', '')}")
        lines.append(f"      Mejor para: {v.get('best_for', '')} | CTR estimado: {v.get('estimated_ctr', '')}")

    lines.append("")
    lines.append(f"🏆 RECOMENDACION: {data.get('recommendation', '')}")
    lines.append(f"📊 PLAN A/B: {data.get('ab_test_plan', '')}")
    lines.append("")

    return "\n".join(lines)


def main():
    import argparse
    topics = [t["topic"] for t in CONTENT_BANK]
    parser = argparse.ArgumentParser(description="A/B Title Tester Bot")
    parser.add_argument("--topic", choices=topics, required=True, help="Tema del video")
    parser.add_argument("--angle", type=str, help="Angulo especifico")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    args = parser.parse_args()

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    print(f"🧪 Generando variantes de titulo ({args.topic})...")
    result = generate_title_variants(args.topic, args.angle)

    if args.json:
        out_file = output_dir / f"titles_{args.topic}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"\n✅ Guardado en {out_file}")
    else:
        text = format_variants_readable(result)
        print(text)
        out_file = output_dir / f"titles_{args.topic}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ Guardado en {out_file}")


if __name__ == "__main__":
    main()
