"""
BOT 5: Caption & Hashtag Optimizer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Optimiza captions y hashtags para maximizar alcance y engagement.

Funciones:
  - Generar captions optimizados por plataforma
  - Seleccionar hashtags por tema, alcance y trending
  - Analizar longitud optima y estructura
  - Generar variantes A/B para testing

USO:
  python -m marketing.bots.caption_optimizer --platform tiktok --topic multas --title "50% descuento en multas"
  python -m marketing.bots.caption_optimizer --platform facebook --topic alquiler --title "Derechos inquilinos"
  python -m marketing.bots.caption_optimizer --ab --platform tiktok --topic laboral
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import BRAND, HASHTAGS, CTAS, CONTENT_BANK


# ─── Patrones de caption por plataforma ──────────────────────────────────────

CAPTION_PATTERNS = {
    "tiktok": {
        "max_length": 150,
        "structure": "Hook corto + hashtags",
        "patterns": [
            "{title} 👇 {hashtags}",
            "⚠️ {title} {hashtags}",
            "ESTO no te lo cuentan 👀 {title} {hashtags}",
            "{title} (guarda este video) {hashtags}",
            "POV: {title} {hashtags}",
            "¿Sabias esto? 🤯 {title} {hashtags}",
        ],
    },
    "facebook": {
        "max_length": 500,
        "structure": "Hook → Contexto → CTA → Hashtags",
        "patterns": [
            "{hook}\n\n{body}\n\n{cta}\n\n{hashtags}",
            "⚠️ {title}\n\n{body}\n\n👉 {cta}\n\n{hashtags}",
            "¿Sabias que...?\n\n{hook}\n\n{body}\n\n{cta}\n\n{hashtags}",
        ],
    },
}

# ─── Emojis por tema ────────────────────────────────────────────────────────

TOPIC_EMOJIS = {
    "multas": ["🚗", "⚠️", "💸", "🚦"],
    "alquiler": ["🏠", "🔑", "🏘️", "📋"],
    "laboral": ["💼", "⚖️", "👷", "📄"],
    "consumo": ["🛒", "💳", "📦", "🧾"],
    "herencias": ["🏛️", "📜", "💰", "👨‍👩‍👧"],
    "vuelos": ["✈️", "🛫", "💶", "⏰"],
    "tramites": ["📝", "🏛️", "💻", "🆓"],
}


def get_topic_data(topic: str) -> dict:
    for item in CONTENT_BANK:
        if item["topic"] == topic:
            return item
    return {"topic": topic, "hooks": [], "facts": []}


def select_hashtags(platform: str, topic: str, max_tags: int = 8) -> list:
    """Selecciona hashtags optimizados."""
    platform_tags = HASHTAGS.get(platform, {})
    core = platform_tags.get("core", [])
    topic_tags = platform_tags.get("topics", {}).get(topic, [])
    reach = platform_tags.get("reach", [])

    selected = list(core)
    selected.extend(topic_tags)
    if reach:
        remaining = max_tags - len(selected)
        if remaining > 0:
            selected.extend(random.sample(reach, min(remaining, len(reach))))

    return selected[:max_tags]


def generate_caption(platform: str, topic: str, title: str = None) -> dict:
    """Genera un caption optimizado."""
    topic_data = get_topic_data(topic)
    hook = random.choice(topic_data["hooks"]) if topic_data["hooks"] else title or f"Esto sobre {topic} te interesa"
    title = title or hook

    tags = select_hashtags(platform, topic)
    hashtags_str = " ".join(tags)
    emojis = TOPIC_EMOJIS.get(topic, ["📌"])
    emoji = random.choice(emojis)

    config = CAPTION_PATTERNS[platform]
    pattern = random.choice(config["patterns"])

    if platform == "tiktok":
        caption = pattern.format(
            title=f"{emoji} {title}",
            hashtags=hashtags_str,
        )
        # Trim to max length
        if len(caption) > config["max_length"]:
            caption = caption[:config["max_length"] - 3] + "..."
    else:
        cta = random.choice(CTAS.get(platform, CTAS["facebook"]))
        facts = topic_data.get("facts", [])
        body = "\n".join(f"➡️ {f}" for f in random.sample(facts, min(3, len(facts)))) if facts else ""
        caption = pattern.format(
            hook=f"{emoji} {hook}",
            title=f"{emoji} {title}",
            body=body,
            cta=cta,
            hashtags=hashtags_str,
        )

    return {
        "metadata": {
            "platform": platform,
            "topic": topic,
            "title": title,
            "generated_at": datetime.now().isoformat(),
        },
        "caption": {
            "text": caption,
            "length": len(caption),
            "max_length": config["max_length"],
            "within_limit": len(caption) <= config["max_length"],
        },
        "hashtags": {
            "selected": tags,
            "count": len(tags),
            "core_count": len(HASHTAGS.get(platform, {}).get("core", [])),
            "topic_count": len(HASHTAGS.get(platform, {}).get("topics", {}).get(topic, [])),
        },
        "optimization_tips": [
            f"Longitud optima {platform}: {'corta y directa' if platform == 'tiktok' else 'detallada con valor'}",
            "Los 3-5 primeros hashtags son los mas importantes",
            f"Emoji principal: {emoji} (tema: {topic})",
            "Publica en horas pico para maximizar alcance inicial",
        ],
    }


def generate_ab_variants(platform: str, topic: str) -> dict:
    """Genera 2 variantes A/B para testing."""
    variant_a = generate_caption(platform, topic)
    variant_b = generate_caption(platform, topic)

    return {
        "test": {
            "platform": platform,
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
        },
        "variant_a": variant_a,
        "variant_b": variant_b,
        "testing_guide": {
            "method": "Publicar cada variante en dias similares (ej. martes vs jueves)",
            "metrics": ["alcance", "likes", "comentarios", "compartidos", "clics en bio"],
            "duration": "Minimo 1 semana por variante",
            "winner_criteria": "Mayor engagement rate (interacciones / alcance)",
        },
    }


def format_caption_readable(data: dict) -> str:
    m = data["metadata"]
    c = data["caption"]
    h = data["hashtags"]

    lines = []
    lines.append("=" * 70)
    lines.append(f"✏️ CAPTION OPTIMIZADO — {m['platform'].upper()}")
    lines.append(f"   Tema: {m['topic']} | Titulo: {m['title']}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("📝 CAPTION:")
    lines.append("")
    for line in c["text"].split("\n"):
        lines.append(f"   {line}")
    lines.append("")
    lines.append(f"   Caracteres: {c['length']}/{c['max_length']} {'✅' if c['within_limit'] else '⚠️ EXCEDE LIMITE'}")
    lines.append("")
    lines.append(f"#️⃣ HASHTAGS ({h['count']} total: {h['core_count']} core + {h['topic_count']} tema + resto alcance)")
    lines.append(f"   {' '.join(h['selected'])}")
    lines.append("")
    lines.append("💡 TIPS:")
    for tip in data["optimization_tips"]:
        lines.append(f"   • {tip}")
    lines.append("")
    return "\n".join(lines)


def main():
    import argparse
    topics = [t["topic"] for t in CONTENT_BANK]
    parser = argparse.ArgumentParser(description="Caption & Hashtag Optimizer")
    parser.add_argument("--platform", choices=["tiktok", "facebook"], required=True, help="Plataforma")
    parser.add_argument("--topic", choices=topics, help="Tema")
    parser.add_argument("--title", type=str, help="Titulo del contenido")
    parser.add_argument("--ab", action="store_true", help="Genera 2 variantes A/B")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    parser.add_argument("--all-topics", action="store_true", help="Genera captions para todos los temas")
    args = parser.parse_args()

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if args.all_topics:
        results = []
        for topic_data in CONTENT_BANK:
            results.append(generate_caption(args.platform, topic_data["topic"]))
        if args.json:
            out_file = output_dir / f"captions_{args.platform}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ {len(results)} captions guardados en {out_file}")
        else:
            for r in results:
                print(format_caption_readable(r))
    elif args.ab and args.topic:
        ab = generate_ab_variants(args.platform, args.topic)
        if args.json:
            print(json.dumps(ab, ensure_ascii=False, indent=2))
        else:
            print("🔬 TEST A/B")
            print(f"   Plataforma: {args.platform} | Tema: {args.topic}")
            print("")
            print("--- VARIANTE A ---")
            print(format_caption_readable(ab["variant_a"]))
            print("--- VARIANTE B ---")
            print(format_caption_readable(ab["variant_b"]))
            g = ab["testing_guide"]
            print("📊 GUIA DE TESTING:")
            print(f"   Metodo: {g['method']}")
            print(f"   Metricas: {', '.join(g['metrics'])}")
            print(f"   Duracion: {g['duration']}")
            print(f"   Ganador: {g['winner_criteria']}")
    elif args.topic:
        result = generate_caption(args.platform, args.topic, args.title)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_caption_readable(result))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
