"""
BOT 9: Content Repurposer
━━━━━━━━━━━━━━━━━━━━━━━━━
Transforma un guion de TikTok en contenido multi-plataforma.

Input: Un guion de TikTok (JSON generado por tiktok_scriptwriter)
Output:
  - Post largo de Facebook (texto + emojis + CTA)
  - Carrusel de slides (texto por slide)
  - Story/Reel caption corto
  - Thread estilo Twitter/X
  - Descripcion YouTube Shorts

USO:
  python -m marketing.bots.content_repurposer --file output/tiktok_script.json
  python -m marketing.bots.content_repurposer --topic multas --format mito_vs_realidad
  python -m marketing.bots.content_repurposer --all-month
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import BRAND, VOICE, CTAS, HASHTAGS
from marketing.llm import ask

SYSTEM_PROMPT = f"""Eres un experto en content repurposing para {BRAND['name']}, una app de asistencia
legal en España. Tu trabajo es transformar guiones de TikTok en contenido adaptado a múltiples
plataformas, manteniendo el mensaje pero adaptando tono, formato y longitud.

Voz de marca: {VOICE['tone']}
Persona: {VOICE['persona']}

REGLAS POR PLATAFORMA:
- Facebook Post: texto largo (300-500 palabras), emojis como bullets, storytelling, CTA al final
- Carrusel: 5-7 slides, cada slide = 1 idea clara, texto corto y visual
- Story/Reel caption: máx 125 caracteres, directo y con gancho
- Twitter/X Thread: 4-6 tweets encadenados, cada uno < 280 chars, primer tweet = gancho viral
- YouTube Shorts: descripción 100-200 palabras, SEO-friendly, con timestamps si aplica

IMPORTANTE: Responde SIEMPRE en JSON válido sin bloques de código markdown."""


def repurpose_script(tiktok_script: dict) -> dict:
    """Transforma un guion de TikTok en contenido multi-plataforma."""
    meta = tiktok_script.get("metadata", {})
    script = tiktok_script.get("script", {})
    pub = tiktok_script.get("publicacion", {})

    title = meta.get("title", "")
    topic = meta.get("topic", "")
    hook = script.get("gancho_3s", {}).get("texto_voz", "")
    points = [p.get("texto", "") for p in script.get("desarrollo_20_30s", {}).get("puntos", [])]
    cta_text = script.get("cta_5s", {}).get("texto_voz", "")

    prompt = f"""Transforma este guion de TikTok en contenido para 5 plataformas diferentes.

GUION ORIGINAL (TikTok):
- Título: {title}
- Tema: {topic}
- Gancho: {hook}
- Puntos principales: {json.dumps(points, ensure_ascii=False)}
- CTA: {cta_text}
- Hashtags originales: {pub.get('hashtags', '')}

Genera contenido adaptado. Responde SOLO con JSON válido:
{{
  "source": {{
    "title": "{title}",
    "topic": "{topic}",
    "platform": "tiktok"
  }},
  "facebook_post": {{
    "text": "post completo con emojis, párrafos, CTA (300-500 palabras)",
    "hashtags": "hashtags para Facebook",
    "estimated_engagement": "alto|medio|bajo"
  }},
  "carousel": {{
    "slides": [
      {{"slide": 1, "headline": "título de slide", "body": "texto corto", "visual_note": "sugerencia visual"}},
      {{"slide": 2, "headline": "...", "body": "...", "visual_note": "..."}},
      {{"slide": 3, "headline": "...", "body": "...", "visual_note": "..."}},
      {{"slide": 4, "headline": "...", "body": "...", "visual_note": "..."}},
      {{"slide": 5, "headline": "CTA", "body": "...", "visual_note": "..."}}
    ],
    "design_notes": "notas de diseño para Canva"
  }},
  "story_reel": {{
    "caption": "máx 125 chars, directo",
    "sticker_suggestion": "sugerencia de sticker/encuesta",
    "cta": "call to action corto"
  }},
  "twitter_thread": {{
    "tweets": [
      {{"number": 1, "text": "tweet gancho (< 280 chars)"}},
      {{"number": 2, "text": "desarrollo 1"}},
      {{"number": 3, "text": "desarrollo 2"}},
      {{"number": 4, "text": "CTA final con enlace"}}
    ]
  }},
  "youtube_shorts": {{
    "title": "título SEO-friendly (< 100 chars)",
    "description": "descripción 100-200 palabras con keywords",
    "tags": ["tag1", "tag2", "tag3"]
  }}
}}"""

    raw = ask(prompt, system=SYSTEM_PROMPT, max_tokens=3000)

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
            "source": {"title": title, "topic": topic},
        }

    result["generated_at"] = datetime.now().isoformat()
    return result


def format_repurposed_readable(data: dict) -> str:
    lines = []
    src = data.get("source", {})

    lines.append("=" * 70)
    lines.append(f"♻️  CONTENT REPURPOSER — {src.get('title', '?')}")
    lines.append(f"   Tema: {src.get('topic', '?')} | Origen: TikTok")
    lines.append("=" * 70)

    if "error" in data:
        lines.append(f"\n❌ Error: {data['error']}")
        return "\n".join(lines)

    # Facebook
    fb = data.get("facebook_post", {})
    lines.append("")
    lines.append("📘 FACEBOOK POST:")
    for line in fb.get("text", "").split("\n"):
        lines.append(f"   {line}")
    lines.append(f"   Hashtags: {fb.get('hashtags', '')}")
    lines.append(f"   Engagement estimado: {fb.get('estimated_engagement', '?')}")

    # Carousel
    car = data.get("carousel", {})
    lines.append("")
    lines.append("🖼️  CARRUSEL:")
    for slide in car.get("slides", []):
        lines.append(f"   [{slide.get('slide', '?')}] {slide.get('headline', '')}")
        lines.append(f"       {slide.get('body', '')}")
        lines.append(f"       Visual: {slide.get('visual_note', '')}")
    if car.get("design_notes"):
        lines.append(f"   Diseño: {car['design_notes']}")

    # Story/Reel
    sr = data.get("story_reel", {})
    lines.append("")
    lines.append("📱 STORY/REEL:")
    lines.append(f"   Caption: {sr.get('caption', '')}")
    lines.append(f"   Sticker: {sr.get('sticker_suggestion', '')}")
    lines.append(f"   CTA: {sr.get('cta', '')}")

    # Twitter thread
    tw = data.get("twitter_thread", {})
    lines.append("")
    lines.append("🐦 TWITTER/X THREAD:")
    for tweet in tw.get("tweets", []):
        lines.append(f"   [{tweet.get('number', '?')}] {tweet.get('text', '')}")

    # YouTube Shorts
    yt = data.get("youtube_shorts", {})
    lines.append("")
    lines.append("▶️  YOUTUBE SHORTS:")
    lines.append(f"   Titulo: {yt.get('title', '')}")
    lines.append(f"   Descripcion: {yt.get('description', '')}")
    lines.append(f"   Tags: {', '.join(yt.get('tags', []))}")

    lines.append("")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Content Repurposer Bot")
    parser.add_argument("--file", type=str, help="Archivo JSON con guion de TikTok")
    parser.add_argument("--topic", type=str, help="Genera guion TikTok y lo repurposea")
    parser.add_argument("--format", type=str, help="Formato del guion TikTok")
    parser.add_argument("--all-month", action="store_true", help="Repurposea todos los guiones del mes")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    args = parser.parse_args()

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            script_data = json.load(f)
        # Handle single script or array
        scripts = script_data if isinstance(script_data, list) else [script_data]
        results = []
        for i, script in enumerate(scripts, 1):
            print(f"♻️  Repurposeando {i}/{len(scripts)}: {script.get('metadata', {}).get('title', '?')[:50]}...")
            results.append(repurpose_script(script))
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for r in results:
                print(format_repurposed_readable(r))

    elif args.topic:
        # Generate a TikTok script first, then repurpose
        from marketing.bots.tiktok_scriptwriter import generate_script
        print(f"🎵 Generando guion TikTok ({args.topic})...")
        script = generate_script(args.topic, args.format)
        print(f"♻️  Repurposeando a multi-plataforma...")
        result = repurpose_script(script)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_repurposed_readable(result))
            out_file = output_dir / f"repurposed_{args.topic}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(format_repurposed_readable(result))
            print(f"✅ Guardado en {out_file}")

    elif args.all_month:
        from marketing.bots.tiktok_scriptwriter import generate_full_month
        scripts = generate_full_month()
        results = []
        for i, script in enumerate(scripts, 1):
            title = script.get("metadata", {}).get("title", "?")
            print(f"♻️  [{i}/{len(scripts)}] {title[:50]}...")
            results.append(repurpose_script(script))

        if args.json:
            out_file = output_dir / f"repurposed_month_{datetime.now().strftime('%Y%m')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n✅ {len(results)} piezas repurposeadas en {out_file}")
        else:
            full_text = "\n".join(format_repurposed_readable(r) for r in results)
            out_file = output_dir / f"repurposed_month_{datetime.now().strftime('%Y%m')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"\n✅ {len(results)} piezas repurposeadas en {out_file}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
