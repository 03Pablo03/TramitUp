"""
BOT 8: Comment Reply Bot
━━━━━━━━━━━━━━━━━━━━━━━━
Genera respuestas naturales y con personalidad para comentarios de TikTok y Facebook.

Funciones:
  - Clasifica comentarios: pregunta legal, testimonio, troll, positivo, solicitud
  - Genera respuestas cercanas con humor cuando toca
  - Detecta oportunidades de vídeo-respuesta
  - Sugiere si responder o ignorar trolls/negativos

USO:
  python -m marketing.bots.comment_reply --file comments.json
  python -m marketing.bots.comment_reply --comment "Me han echado del piso sin contrato"
  python -m marketing.bots.comment_reply --comment "Esto es mentira" --platform tiktok
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import BRAND, VOICE
from marketing.llm import ask

SYSTEM_PROMPT = f"""Eres el community manager de {BRAND['name']}, una app de asistencia legal en España.
Tu trabajo es responder comentarios en redes sociales (TikTok y Facebook).

PERSONALIDAD:
- Tono: {VOICE['tone']}
- Persona: {VOICE['persona']}
- Cercano, con humor sutil cuando es apropiado
- NUNCA corporativo ni robótico
- Siempre aporta valor legal real cuando hay una pregunta
- Usa emojis con moderación (1-2 máximo por respuesta)

REGLAS:
- Si es una pregunta legal: responde con dato concreto + sugiere la app sutilmente
- Si es un comentario positivo: agradece brevemente y con personalidad
- Si es un testimonio/caso personal: muestra empatía + orienta
- Si es un troll/negativo destructivo: sugiere ignorar (no alimentar)
- Si es una crítica constructiva: agradece y responde con humildad
- Las respuestas deben ser CORTAS (máx 2-3 frases para TikTok, algo más para Facebook)

IMPORTANTE: Responde SIEMPRE en JSON válido sin bloques de código markdown."""


def classify_and_reply(comment: str, platform: str = "tiktok", context: str = "") -> dict:
    """Clasifica un comentario y genera respuesta."""
    prompt = f"""Analiza este comentario de {platform} y genera una respuesta.

Comentario: "{comment}"
{f'Contexto del vídeo/post: {context}' if context else ''}
Plataforma: {platform}

Responde SOLO con JSON válido:
{{
  "comment": "{comment}",
  "platform": "{platform}",
  "classification": {{
    "type": "pregunta_legal|testimonio|positivo|troll|critica|solicitud|spam|irrelevante",
    "sentiment": "positivo|neutro|negativo",
    "has_legal_question": true/false,
    "video_reply_opportunity": true/false,
    "video_reply_reason": "razón si es buena oportunidad para vídeo-respuesta o null"
  }},
  "action": {{
    "should_reply": true/false,
    "reason": "por qué responder o no",
    "priority": "alta|media|baja"
  }},
  "reply": {{
    "text": "la respuesta (o null si no se debe responder)",
    "tone_used": "humor|empatía|informativo|agradecimiento|ninguno",
    "includes_app_mention": true/false
  }},
  "video_reply": {{
    "suggested": true/false,
    "title_if_yes": "título del vídeo-respuesta o null",
    "angle_if_yes": "ángulo del vídeo o null"
  }}
}}"""

    raw = ask(prompt, system=SYSTEM_PROMPT, max_tokens=1500)

    try:
        if "```" in raw:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            raw = raw[start:end]
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "comment": comment,
            "platform": platform,
            "error": "No se pudo parsear la respuesta",
            "raw": raw[:300],
        }

    result["generated_at"] = datetime.now().isoformat()
    return result


def process_comments_batch(comments: list, platform: str = "tiktok") -> list:
    """Procesa una lista de comentarios."""
    results = []
    for i, item in enumerate(comments, 1):
        comment_text = item if isinstance(item, str) else item.get("text", item.get("comment", ""))
        context = item.get("context", "") if isinstance(item, dict) else ""
        print(f"   Procesando comentario {i}/{len(comments)}...")
        result = classify_and_reply(comment_text, platform, context)
        results.append(result)
    return results


def format_reply_readable(data: dict) -> str:
    lines = []
    lines.append("-" * 60)

    if "error" in data:
        lines.append(f"❌ Error procesando: {data.get('comment', '')[:50]}")
        lines.append(f"   {data['error']}")
        return "\n".join(lines)

    c = data.get("classification", {})
    a = data.get("action", {})
    r = data.get("reply", {})
    v = data.get("video_reply", {})

    type_icons = {
        "pregunta_legal": "❓", "testimonio": "📖", "positivo": "👍",
        "troll": "🚫", "critica": "💬", "solicitud": "🙋",
        "spam": "🗑️", "irrelevante": "➖",
    }
    icon = type_icons.get(c.get("type", ""), "💬")

    lines.append(f"{icon} [{c.get('type', '?')}] [{c.get('sentiment', '?')}] "
                 f"Prioridad: {a.get('priority', '?')}")
    lines.append(f"   Comentario: \"{data.get('comment', '')[:80]}\"")
    lines.append(f"   Responder: {'SI' if a.get('should_reply') else 'NO'} — {a.get('reason', '')}")

    if r.get("text"):
        lines.append(f"   📝 Respuesta: \"{r['text']}\"")
        lines.append(f"      Tono: {r.get('tone_used', '')} | Mención app: {'Sí' if r.get('includes_app_mention') else 'No'}")

    if v.get("suggested"):
        lines.append(f"   🎬 VIDEO-RESPUESTA: {v.get('title_if_yes', '')}")
        lines.append(f"      Ángulo: {v.get('angle_if_yes', '')}")

    if c.get("video_reply_opportunity"):
        lines.append(f"   ⭐ Oportunidad de vídeo: {c.get('video_reply_reason', '')}")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Comment Reply Bot")
    parser.add_argument("--comment", type=str, help="Comentario individual")
    parser.add_argument("--file", type=str, help="Archivo JSON con lista de comentarios")
    parser.add_argument("--platform", choices=["tiktok", "facebook"], default="tiktok")
    parser.add_argument("--context", type=str, default="", help="Contexto del vídeo/post")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    args = parser.parse_args()

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if args.comment:
        result = classify_and_reply(args.comment, args.platform, args.context)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_reply_readable(result))
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ Archivo no encontrado: {args.file}")
            return
        with open(file_path, "r", encoding="utf-8") as f:
            comments = json.load(f)
        if not isinstance(comments, list):
            comments = [comments]

        print(f"📝 Procesando {len(comments)} comentarios ({args.platform})...")
        results = process_comments_batch(comments, args.platform)

        video_opportunities = [r for r in results if r.get("video_reply", {}).get("suggested")]
        should_reply = [r for r in results if r.get("action", {}).get("should_reply")]
        trolls = [r for r in results if r.get("classification", {}).get("type") == "troll"]

        if args.json:
            out_file = output_dir / f"replies_{args.platform}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ {len(results)} respuestas guardadas en {out_file}")
        else:
            print("\n" + "=" * 60)
            print(f"💬 RESPUESTAS — {args.platform.upper()}")
            print(f"   Total: {len(results)} | Responder: {len(should_reply)} | "
                  f"Videos: {len(video_opportunities)} | Trolls: {len(trolls)}")
            print("=" * 60)
            for r in results:
                print(format_reply_readable(r))
            print("")

            out_file = output_dir / f"replies_{args.platform}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            full_text = "\n".join(format_reply_readable(r) for r in results)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"✅ Guardado en {out_file}")
    else:
        parser.print_help()
        print("\nEjemplo rápido:")
        print('  python -m marketing.bots.comment_reply --comment "¿Me pueden echar si no pago un mes?"')
        print("\nFormato de archivo JSON para batch:")
        print('  [{"text": "comentario", "context": "vídeo sobre multas"}, ...]')


if __name__ == "__main__":
    main()
