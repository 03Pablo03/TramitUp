"""
BOT 1: TikTok Script Writer
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Genera guiones completos para videos de TikTok con estructura:
  Gancho (3s) → Desarrollo (20-30s) → CTA (5s)

Cada guion incluye:
  - Texto en pantalla sugerido
  - Formato recomendado (POV, listicle, tutorial, etc.)
  - Hashtags optimizados
  - Duracion estimada
  - Notas de grabacion

USO:
  python -m marketing.bots.tiktok_scriptwriter --topic multas
  python -m marketing.bots.tiktok_scriptwriter --topic alquiler --format top_3_listicle
  python -m marketing.bots.tiktok_scriptwriter --all  (genera el mes completo)
"""

import json
import random
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import (
    BRAND, VOICE, CTAS, HASHTAGS, CONTENT_BANK, TIKTOK_FORMATS, SCHEDULE
)


# ─── Plantillas de guion por formato ─────────────────────────────────────────

SCRIPT_TEMPLATES = {
    "mito_vs_realidad": {
        "structure": "Gancho con mito comun → Desmontar con datos reales → CTA",
        "screen_text_prefix": "MITO vs REALIDAD",
        "duration": "30-45s",
        "tips": "Empieza diciendo el mito como si fuera verdad, luego giro dramatico",
    },
    "top_3_listicle": {
        "structure": "Gancho numerico → 3 puntos con transicion rapida → CTA",
        "screen_text_prefix": "3 COSAS QUE...",
        "duration": "40-60s",
        "tips": "Transicion visual entre cada punto. Deja el mejor para el final",
    },
    "tutorial_rapido": {
        "structure": "Problema → Paso 1 → Paso 2 → Paso 3 → CTA",
        "screen_text_prefix": "PASO A PASO",
        "duration": "45-60s",
        "tips": "Incluye capturas de pantalla o ejemplos visuales en cada paso",
    },
    "pov_storytelling": {
        "structure": "POV situacion comun → Descubrimiento → Solucion → CTA",
        "screen_text_prefix": "POV:",
        "duration": "30-45s",
        "tips": "Empieza con reaccion sorprendida, luego explica",
    },
    "pregunta_gancho": {
        "structure": "Pregunta directa → Respuesta con datos → Matiz importante → CTA",
        "screen_text_prefix": "¿SABIAS QUE...?",
        "duration": "30-40s",
        "tips": "La pregunta debe ser algo que la gente se pregunte de verdad",
    },
    "revelacion": {
        "structure": "Lo que nadie te cuenta → Revelacion 1 → Revelacion 2 → CTA",
        "screen_text_prefix": "LO QUE NO TE CUENTAN",
        "duration": "40-50s",
        "tips": "Tono de 'te estan ocultando algo', genera intriga",
    },
    "pregunta_viral": {
        "structure": "Pregunta polarizante → Si/No con matices → Dato legal → CTA",
        "screen_text_prefix": "¿ES LEGAL...?",
        "duration": "30-40s",
        "tips": "Preguntas tipo si/no que generan debate en comentarios",
    },
    "demo_app": {
        "structure": "Problema comun → Abro TramitUp → Pregunto → Resultado → CTA",
        "screen_text_prefix": "PROBANDO TRAMITUP",
        "duration": "45-60s",
        "tips": "Screen recording real de la app. Reaccion genuina al resultado",
    },
    "listicle_valor": {
        "structure": "Titulo numerico → Items rapidos con texto → CTA",
        "screen_text_prefix": "X COSAS QUE NO SABIAS",
        "duration": "40-60s",
        "tips": "Texto dinamico en pantalla, ritmo rapido entre items",
    },
    "consecuencias": {
        "structure": "Accion → Consecuencia 1 → Consecuencia 2 → Final dramatico → CTA",
        "screen_text_prefix": "¿QUE PASA SI...?",
        "duration": "40-50s",
        "tips": "Escalada dramatica. Musica de tension. Datos reales en cada paso",
    },
    "storytime": {
        "structure": "Contexto → Nudo → Desenlace con leccion legal → CTA",
        "screen_text_prefix": "STORYTIME",
        "duration": "50-60s",
        "tips": "Narrativa personal o dramatizada. Empatia con la audiencia",
    },
    "datos_reales": {
        "structure": "Pregunta de dinero → Cifras reales en pantalla → Explicacion → CTA",
        "screen_text_prefix": "DATOS REALES",
        "duration": "40-50s",
        "tips": "Cifras grandes en pantalla. Comparaciones que impacten",
    },
}


# ─── Calendario del Mes 1 (12 videos) ────────────────────────────────────────

MONTH_1_PLAN = [
    {"week": 1, "topic": "multas", "format": "mito_vs_realidad",
     "title": "¿Sabias que si te ponen una multa tienes 20 dias para pagar con 50% de descuento?"},
    {"week": 1, "topic": "alquiler", "format": "top_3_listicle",
     "title": "3 cosas que tu casero NO puede hacerte"},
    {"week": 1, "topic": "consumo", "format": "tutorial_rapido",
     "title": "¿Te han cobrado de mas en una factura? Esto es lo que tienes que hacer"},
    {"week": 2, "topic": "vuelos", "format": "pov_storytelling",
     "title": "POV: Descubres que puedes reclamar un vuelo retrasado de hace 3 años"},
    {"week": 2, "topic": "alquiler", "format": "pregunta_gancho",
     "title": "¿Pueden echarte de tu piso si no pagas un mes?"},
    {"week": 2, "topic": "herencias", "format": "revelacion",
     "title": "Lo que NADIE te cuenta cuando heredas una casa"},
    {"week": 3, "topic": "laboral", "format": "pregunta_viral",
     "title": "¿Es legal que te graben con camaras en el trabajo?"},
    {"week": 3, "topic": "tramites", "format": "demo_app",
     "title": "He usado IA para entender mis derechos y esto paso"},
    {"week": 3, "topic": "tramites", "format": "listicle_valor",
     "title": "5 tramites que puedes hacer GRATIS y no lo sabias"},
    {"week": 4, "topic": "multas", "format": "consecuencias",
     "title": "¿Que pasa si no pagas una multa?"},
    {"week": 4, "topic": "alquiler", "format": "storytime",
     "title": "Storytime: Mi vecino me denuncio por ruido y esto fue lo que pase"},
    {"week": 4, "topic": "laboral", "format": "datos_reales",
     "title": "¿Cuanto cuesta REALMENTE un divorcio en España?"},
]


def get_topic_data(topic: str) -> dict:
    """Busca datos del banco de contenido por tema."""
    for item in CONTENT_BANK:
        if item["topic"] == topic:
            return item
    return {"topic": topic, "hooks": [], "facts": []}


def generate_script(topic: str, format_type: str = None, title: str = None) -> dict:
    """Genera un guion completo de TikTok."""
    topic_data = get_topic_data(topic)
    if not format_type:
        format_type = random.choice(TIKTOK_FORMATS)
    template = SCRIPT_TEMPLATES.get(format_type, SCRIPT_TEMPLATES["pregunta_gancho"])

    hook = random.choice(topic_data["hooks"]) if topic_data["hooks"] else f"Esto sobre {topic} te va a sorprender."
    facts = topic_data.get("facts", [])
    cta = random.choice(CTAS["tiktok"])

    # Build hashtags
    topic_tags = HASHTAGS["tiktok"]["topics"].get(topic, [])
    tags = HASHTAGS["tiktok"]["core"] + topic_tags + random.sample(HASHTAGS["tiktok"]["reach"], 2)

    # Build script sections
    script = {
        "metadata": {
            "topic": topic,
            "format": format_type,
            "title": title or hook,
            "duration_estimated": template["duration"],
            "generated_at": datetime.now().isoformat(),
        },
        "script": {
            "gancho_3s": {
                "texto_voz": f'"{hook}"',
                "texto_pantalla": f'{template["screen_text_prefix"]}: {(title or hook)[:50].upper()}',
                "nota": "Empieza con energia. Los 3 primeros segundos deciden si te ven.",
            },
            "desarrollo_20_30s": {
                "puntos": [],
                "nota": template["tips"],
            },
            "cta_5s": {
                "texto_voz": f'"{cta}"',
                "texto_pantalla": "Link en bio → TramitUp",
                "nota": "Tono natural, no venta agresiva.",
            },
        },
        "produccion": {
            "estructura": template["structure"],
            "formato": format_type.replace("_", " ").title(),
            "subtitulos": "OBLIGATORIOS (80% ve sin sonido)",
            "musica": "Sonido trending de fondo suave, que no tape la voz",
            "grabacion": template["tips"],
        },
        "publicacion": {
            "hashtags": " ".join(tags),
            "mejor_hora": random.choice(SCHEDULE["tiktok"]["best_hours"]),
            "mejor_dia": random.choice(SCHEDULE["tiktok"]["best_days"]),
            "caption": f'{(title or hook)} {" ".join(tags[:6])}',
        },
    }

    # Fill development points from facts
    used_facts = random.sample(facts, min(3, len(facts))) if facts else [
        f"Dato relevante sobre {topic} (investiga dato concreto)",
    ]
    for i, fact in enumerate(used_facts, 1):
        script["script"]["desarrollo_20_30s"]["puntos"].append({
            "punto": i,
            "texto": fact,
            "duracion": "8-10s",
        })

    return script


def generate_full_month() -> list:
    """Genera los 12 guiones del Mes 1."""
    scripts = []
    for plan in MONTH_1_PLAN:
        script = generate_script(plan["topic"], plan["format"], plan["title"])
        script["metadata"]["week"] = plan["week"]
        scripts.append(script)
    return scripts


def format_script_readable(script: dict) -> str:
    """Formatea un guion para lectura humana."""
    m = script["metadata"]
    s = script["script"]
    p = script["publicacion"]
    prod = script["produccion"]

    lines = []
    lines.append("=" * 70)
    lines.append(f"📹 GUION TIKTOK — Semana {m.get('week', '?')}")
    lines.append(f"   Titulo: {m['title']}")
    lines.append(f"   Formato: {prod['formato']} | Duracion: {m['duration_estimated']}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"🎯 GANCHO (3 segundos)")
    lines.append(f"   Voz: {s['gancho_3s']['texto_voz']}")
    lines.append(f"   Pantalla: {s['gancho_3s']['texto_pantalla']}")
    lines.append(f"   💡 {s['gancho_3s']['nota']}")
    lines.append("")
    lines.append(f"📝 DESARROLLO (20-30 segundos)")
    for punto in s["desarrollo_20_30s"]["puntos"]:
        lines.append(f"   [{punto['punto']}] {punto['texto']} ({punto['duracion']})")
    lines.append(f"   💡 {s['desarrollo_20_30s']['nota']}")
    lines.append("")
    lines.append(f"📣 CTA (5 segundos)")
    lines.append(f"   Voz: {s['cta_5s']['texto_voz']}")
    lines.append(f"   Pantalla: {s['cta_5s']['texto_pantalla']}")
    lines.append("")
    lines.append(f"🎬 PRODUCCION")
    lines.append(f"   Estructura: {prod['estructura']}")
    lines.append(f"   Subtitulos: {prod['subtitulos']}")
    lines.append(f"   Musica: {prod['musica']}")
    lines.append(f"   Grabacion: {prod['grabacion']}")
    lines.append("")
    lines.append(f"📱 PUBLICACION")
    lines.append(f"   Hora: {p['mejor_hora']} | Dia: {p['mejor_dia']}")
    lines.append(f"   Caption: {p['caption']}")
    lines.append(f"   Hashtags: {p['hashtags']}")
    lines.append("")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="TikTok Script Writer Bot")
    parser.add_argument("--topic", choices=[t["topic"] for t in CONTENT_BANK], help="Tema del video")
    parser.add_argument("--format", choices=TIKTOK_FORMATS, help="Formato del video")
    parser.add_argument("--all", action="store_true", help="Genera el mes completo (12 videos)")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    args = parser.parse_args()

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if args.all:
        scripts = generate_full_month()
        if args.json:
            out_file = output_dir / f"tiktok_month_{datetime.now().strftime('%Y%m')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(scripts, f, ensure_ascii=False, indent=2)
            print(f"✅ {len(scripts)} guiones guardados en {out_file}")
        else:
            full_text = ""
            for script in scripts:
                full_text += format_script_readable(script) + "\n"
            out_file = output_dir / f"tiktok_month_{datetime.now().strftime('%Y%m')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(full_text)
            print(f"✅ {len(scripts)} guiones guardados en {out_file}")
    elif args.topic:
        script = generate_script(args.topic, args.format)
        if args.json:
            print(json.dumps(script, ensure_ascii=False, indent=2))
        else:
            print(format_script_readable(script))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
