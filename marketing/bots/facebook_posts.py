"""
BOT 2: Facebook Post Generator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Genera posts completos para la página de Facebook de TramitUp.

Formatos soportados:
  - Carrusel informativo (slides)
  - Post de valor (texto largo educativo)
  - Pregunta de engagement
  - Caso real (storytelling)
  - Infografía (estructura visual)
  - Demo/tutorial de la app
  - Testimonio
  - Post educativo

USO:
  python -m marketing.bots.facebook_posts --topic alquiler
  python -m marketing.bots.facebook_posts --topic laboral --format caso_real
  python -m marketing.bots.facebook_posts --all
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import (
    BRAND, VOICE, CTAS, HASHTAGS, CONTENT_BANK, FACEBOOK_FORMATS, SCHEDULE
)


# ─── Plantillas por formato ─────────────────────────────────────────────────

POST_TEMPLATES = {
    "carrusel_informativo": {
        "structure": "Slide 1 (gancho) → Slides 2-5 (contenido) → Slide final (CTA)",
        "tone": "Visual, directo, datos en cada slide",
        "optimal_slides": 5,
        "tips": "Cada slide debe ser entendible por separado. Texto grande y legible.",
    },
    "post_de_valor": {
        "structure": "Hook → Contexto → 3-5 puntos clave → CTA",
        "tone": "Educativo, cercano, con emojis moderados",
        "optimal_slides": 0,
        "tips": "Texto largo pero bien estructurado. Usa saltos de linea y emojis como bullets.",
    },
    "pregunta_engagement": {
        "structure": "Pregunta directa → Contexto breve → Invitacion a comentar",
        "tone": "Conversacional, genera debate",
        "optimal_slides": 0,
        "tips": "La pregunta debe tener respuestas variadas. Responde a los primeros comentarios.",
    },
    "caso_real": {
        "structure": "Situacion → Problema → Que dice la ley → Resolucion → CTA",
        "tone": "Narrativo, empatico, con datos legales",
        "optimal_slides": 0,
        "tips": "Anonimiza el caso. Usa comillas para frases del protagonista.",
    },
    "infografia": {
        "structure": "Titulo visual → Datos clave → Pasos/Proceso → CTA",
        "tone": "Visual, esquematico, cifras destacadas",
        "optimal_slides": 1,
        "tips": "Diseñar con Canva. Colores de marca. Datos grandes y legibles.",
    },
    "demo_tutorial": {
        "structure": "Problema → Abro TramitUp → Paso a paso → Resultado → CTA",
        "tone": "Practico, paso a paso",
        "optimal_slides": 4,
        "tips": "Capturas reales de la app. Flechas señalando donde hacer clic.",
    },
    "testimonio": {
        "structure": "Cita del usuario → Contexto → Resultado → CTA",
        "tone": "Personal, credible, emotivo",
        "optimal_slides": 1,
        "tips": "Foto del usuario (con permiso) o avatar. Cita textual entre comillas.",
    },
    "post_educativo": {
        "structure": "Dato sorprendente → Explicacion → Que hacer → CTA",
        "tone": "Informativo, autoridad, accesible",
        "optimal_slides": 0,
        "tips": "Empieza con el dato mas impactante. Lenguaje simple.",
    },
}


# ─── Calendario Mes 1 Facebook (12 posts) ───────────────────────────────────

MONTH_1_FB_PLAN = [
    {"week": 1, "topic": "alquiler", "format": "carrusel_informativo",
     "title": "5 derechos que tienes como inquilino y probablemente no conoces"},
    {"week": 1, "topic": "multas", "format": "post_de_valor",
     "title": "Te han puesto una multa. ¿Pagas o recurres? Guia rapida"},
    {"week": 1, "topic": "consumo", "format": "pregunta_engagement",
     "title": "¿Alguna vez te han cobrado de mas y no has reclamado?"},
    {"week": 2, "topic": "laboral", "format": "caso_real",
     "title": "Le despidieron sin preaviso. Esto es lo que consiguio"},
    {"week": 2, "topic": "tramites", "format": "infografia",
     "title": "Tramites gratuitos que la mayoria paga por hacer"},
    {"week": 2, "topic": "herencias", "format": "post_educativo",
     "title": "Heredar en España puede costarte mas de lo que recibes"},
    {"week": 3, "topic": "vuelos", "format": "caso_real",
     "title": "Reclamo un vuelo de hace 2 años y recibio 400€"},
    {"week": 3, "topic": "tramites", "format": "demo_tutorial",
     "title": "Como usar TramitUp para resolver tu duda legal en 2 minutos"},
    {"week": 3, "topic": "alquiler", "format": "pregunta_engagement",
     "title": "Tu casero sube el alquiler. ¿Sabes si puede hacerlo legalmente?"},
    {"week": 4, "topic": "laboral", "format": "carrusel_informativo",
     "title": "Te despiden: los 5 pasos que debes seguir SI o SI"},
    {"week": 4, "topic": "consumo", "format": "post_de_valor",
     "title": "14 dias para devolver cualquier compra online. La ley te protege"},
    {"week": 4, "topic": "multas", "format": "testimonio",
     "title": "Recurri mi multa con TramitUp y me la anularon"},
]


def get_topic_data(topic: str) -> dict:
    for item in CONTENT_BANK:
        if item["topic"] == topic:
            return item
    return {"topic": topic, "hooks": [], "facts": []}


def generate_post(topic: str, format_type: str = None, title: str = None) -> dict:
    """Genera un post completo de Facebook."""
    topic_data = get_topic_data(topic)
    if not format_type:
        format_type = random.choice(FACEBOOK_FORMATS)
    template = POST_TEMPLATES.get(format_type, POST_TEMPLATES["post_de_valor"])

    hook = random.choice(topic_data["hooks"]) if topic_data["hooks"] else f"Esto sobre {topic} te interesa."
    facts = topic_data.get("facts", [])
    cta = random.choice(CTAS["facebook"])

    # Hashtags
    topic_tags = HASHTAGS["facebook"]["topics"].get(topic, [])
    tags = HASHTAGS["facebook"]["core"] + topic_tags

    # Build body text
    used_facts = random.sample(facts, min(4, len(facts))) if facts else [
        f"Dato relevante sobre {topic} (investigar dato concreto)",
    ]

    body_lines = [hook, ""]
    for i, fact in enumerate(used_facts, 1):
        body_lines.append(f"➡️ {fact}")
    body_lines.append("")
    body_lines.append(cta)

    # Build slides for carousel/infographic formats
    slides = []
    if template["optimal_slides"] > 0:
        slides.append({"slide": 1, "content": title or hook, "type": "gancho"})
        for i, fact in enumerate(used_facts, 2):
            slides.append({"slide": i, "content": fact, "type": "contenido"})
        slides.append({"slide": len(slides) + 1, "content": cta, "type": "cta"})

    post = {
        "metadata": {
            "topic": topic,
            "format": format_type,
            "title": title or hook,
            "generated_at": datetime.now().isoformat(),
        },
        "content": {
            "headline": title or hook,
            "body": "\n".join(body_lines),
            "cta": cta,
        },
        "visual": {
            "format": format_type.replace("_", " ").title(),
            "slides": slides if slides else None,
            "tips": template["tips"],
            "brand_colors": "Azul TramitUp + blanco + acento naranja",
        },
        "publishing": {
            "hashtags": " ".join(tags),
            "best_hour": random.choice(SCHEDULE["facebook"]["best_hours"]),
            "caption": f'{(title or hook)} {" ".join(tags[:4])}',
            "cross_post": "Adaptar para grupo de Facebook si el tema aplica",
        },
        "production": {
            "structure": template["structure"],
            "tone": template["tone"],
            "tips": template["tips"],
        },
    }

    return post


def generate_full_month() -> list:
    """Genera los 12 posts del Mes 1."""
    posts = []
    for plan in MONTH_1_FB_PLAN:
        post = generate_post(plan["topic"], plan["format"], plan["title"])
        post["metadata"]["week"] = plan["week"]
        posts.append(post)
    return posts


def format_post_readable(post: dict) -> str:
    """Formatea un post para lectura humana."""
    m = post["metadata"]
    c = post["content"]
    p = post["publishing"]
    prod = post["production"]
    v = post["visual"]

    lines = []
    lines.append("=" * 70)
    lines.append(f"📘 POST FACEBOOK — Semana {m.get('week', '?')}")
    lines.append(f"   Titulo: {m['title']}")
    lines.append(f"   Formato: {v['format']}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("📝 CONTENIDO")
    lines.append(f"   Titular: {c['headline']}")
    lines.append("")
    for line in c["body"].split("\n"):
        lines.append(f"   {line}")
    lines.append("")

    if v.get("slides"):
        lines.append("🖼️ SLIDES")
        for slide in v["slides"]:
            lines.append(f"   [{slide['slide']}] ({slide['type']}) {slide['content']}")
        lines.append("")

    lines.append("🎨 VISUAL")
    lines.append(f"   Tips: {v['tips']}")
    lines.append(f"   Colores: {v['brand_colors']}")
    lines.append("")
    lines.append("📱 PUBLICACION")
    lines.append(f"   Hora: {p['best_hour']}")
    lines.append(f"   Hashtags: {p['hashtags']}")
    lines.append(f"   Cross-post: {p['cross_post']}")
    lines.append("")
    lines.append("🎯 PRODUCCION")
    lines.append(f"   Estructura: {prod['structure']}")
    lines.append(f"   Tono: {prod['tone']}")
    lines.append(f"   Tips: {prod['tips']}")
    lines.append("")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Facebook Post Generator Bot")
    parser.add_argument("--topic", choices=[t["topic"] for t in CONTENT_BANK], help="Tema del post")
    parser.add_argument("--format", choices=FACEBOOK_FORMATS, help="Formato del post")
    parser.add_argument("--all", action="store_true", help="Genera el mes completo (12 posts)")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    args = parser.parse_args()

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if args.all:
        posts = generate_full_month()
        if args.json:
            out_file = output_dir / f"facebook_month_{datetime.now().strftime('%Y%m')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)
            print(f"✅ {len(posts)} posts guardados en {out_file}")
        else:
            full_text = ""
            for post in posts:
                full_text += format_post_readable(post) + "\n"
            out_file = output_dir / f"facebook_month_{datetime.now().strftime('%Y%m')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(full_text)
            print(f"✅ {len(posts)} posts guardados en {out_file}")
    elif args.topic:
        post = generate_post(args.topic, args.format)
        if args.json:
            print(json.dumps(post, ensure_ascii=False, indent=2))
        else:
            print(format_post_readable(post))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
