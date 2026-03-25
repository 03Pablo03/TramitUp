"""
BOT 4: Content Calendar Bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Genera y gestiona el calendario editorial mensual para TikTok y Facebook.

Funciones:
  - Generar calendario semanal/mensual
  - Asignar formatos y temas equilibrados
  - Respetar frecuencia optima por plataforma
  - Exportar a formato legible o JSON

USO:
  python -m marketing.bots.calendar_bot --month 1
  python -m marketing.bots.calendar_bot --week 2
  python -m marketing.bots.calendar_bot --month 1 --json
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import (
    CONTENT_BANK, TIKTOK_FORMATS, FACEBOOK_FORMATS, SCHEDULE
)

# ─── Calendario maestro Mes 1 ───────────────────────────────────────────────

MASTER_CALENDAR = {
    1: {
        "week": 1,
        "dates": "Lunes a Domingo (Semana 1)",
        "theme": "Lanzamiento — posicionar derechos cotidianos",
        "tiktok": [
            {"day": "martes", "topic": "multas", "format": "mito_vs_realidad",
             "title": "¿Sabias que si te ponen una multa tienes 20 dias para pagar con 50% de descuento?"},
            {"day": "jueves", "topic": "alquiler", "format": "top_3_listicle",
             "title": "3 cosas que tu casero NO puede hacerte"},
            {"day": "sabado", "topic": "consumo", "format": "tutorial_rapido",
             "title": "¿Te han cobrado de mas en una factura? Esto es lo que tienes que hacer"},
        ],
        "facebook": [
            {"day": "lunes", "topic": "alquiler", "format": "carrusel_informativo",
             "title": "5 derechos que tienes como inquilino y probablemente no conoces"},
            {"day": "miercoles", "topic": "multas", "format": "post_de_valor",
             "title": "Te han puesto una multa. ¿Pagas o recurres? Guia rapida"},
            {"day": "viernes", "topic": "consumo", "format": "pregunta_engagement",
             "title": "¿Alguna vez te han cobrado de mas y no has reclamado?"},
        ],
        "community": [
            {"day": "miercoles", "group_type": "inquilinos", "topic": "alquiler"},
            {"day": "sabado", "group_type": "consumidores", "topic": "consumo"},
        ],
    },
    2: {
        "week": 2,
        "dates": "Lunes a Domingo (Semana 2)",
        "theme": "Engagement — historias y debate",
        "tiktok": [
            {"day": "martes", "topic": "vuelos", "format": "pov_storytelling",
             "title": "POV: Descubres que puedes reclamar un vuelo retrasado de hace 3 años"},
            {"day": "jueves", "topic": "alquiler", "format": "pregunta_gancho",
             "title": "¿Pueden echarte de tu piso si no pagas un mes?"},
            {"day": "sabado", "topic": "herencias", "format": "revelacion",
             "title": "Lo que NADIE te cuenta cuando heredas una casa"},
        ],
        "facebook": [
            {"day": "lunes", "topic": "laboral", "format": "caso_real",
             "title": "Le despidieron sin preaviso. Esto es lo que consiguio"},
            {"day": "miercoles", "topic": "tramites", "format": "infografia",
             "title": "Tramites gratuitos que la mayoria paga por hacer"},
            {"day": "viernes", "topic": "herencias", "format": "post_educativo",
             "title": "Heredar en España puede costarte mas de lo que recibes"},
        ],
        "community": [
            {"day": "martes", "group_type": "laboral", "topic": "laboral"},
            {"day": "viernes", "group_type": "tramites", "topic": "tramites"},
        ],
    },
    3: {
        "week": 3,
        "dates": "Lunes a Domingo (Semana 3)",
        "theme": "Producto — mostrar TramitUp en accion",
        "tiktok": [
            {"day": "martes", "topic": "laboral", "format": "pregunta_viral",
             "title": "¿Es legal que te graben con camaras en el trabajo?"},
            {"day": "jueves", "topic": "tramites", "format": "demo_app",
             "title": "He usado IA para entender mis derechos y esto paso"},
            {"day": "sabado", "topic": "tramites", "format": "listicle_valor",
             "title": "5 tramites que puedes hacer GRATIS y no lo sabias"},
        ],
        "facebook": [
            {"day": "lunes", "topic": "vuelos", "format": "caso_real",
             "title": "Reclamo un vuelo de hace 2 años y recibio 400€"},
            {"day": "miercoles", "topic": "tramites", "format": "demo_tutorial",
             "title": "Como usar TramitUp para resolver tu duda legal en 2 minutos"},
            {"day": "viernes", "topic": "alquiler", "format": "pregunta_engagement",
             "title": "Tu casero sube el alquiler. ¿Sabes si puede hacerlo legalmente?"},
        ],
        "community": [
            {"day": "lunes", "group_type": "inquilinos", "topic": "alquiler"},
            {"day": "jueves", "group_type": "laboral", "topic": "laboral"},
        ],
    },
    4: {
        "week": 4,
        "dates": "Lunes a Domingo (Semana 4)",
        "theme": "Conversion — testimonios y urgencia",
        "tiktok": [
            {"day": "martes", "topic": "multas", "format": "consecuencias",
             "title": "¿Que pasa si no pagas una multa?"},
            {"day": "jueves", "topic": "alquiler", "format": "storytime",
             "title": "Storytime: Mi vecino me denuncio por ruido y esto fue lo que pase"},
            {"day": "sabado", "topic": "laboral", "format": "datos_reales",
             "title": "¿Cuanto cuesta REALMENTE un divorcio en España?"},
        ],
        "facebook": [
            {"day": "lunes", "topic": "laboral", "format": "carrusel_informativo",
             "title": "Te despiden: los 5 pasos que debes seguir SI o SI"},
            {"day": "miercoles", "topic": "consumo", "format": "post_de_valor",
             "title": "14 dias para devolver cualquier compra online. La ley te protege"},
            {"day": "viernes", "topic": "multas", "format": "testimonio",
             "title": "Recurri mi multa con TramitUp y me la anularon"},
        ],
        "community": [
            {"day": "miercoles", "group_type": "consumidores", "topic": "consumo"},
            {"day": "sabado", "group_type": "inquilinos", "topic": "alquiler"},
        ],
    },
}


def get_week_calendar(week: int) -> dict:
    return MASTER_CALENDAR.get(week, {})


def get_month_calendar() -> list:
    return [MASTER_CALENDAR[w] for w in sorted(MASTER_CALENDAR.keys())]


def format_week_readable(week_data: dict) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append(f"📅 SEMANA {week_data['week']} — {week_data['theme']}")
    lines.append(f"   {week_data['dates']}")
    lines.append("=" * 70)

    lines.append("")
    lines.append("🎵 TIKTOK (3 videos)")
    for item in week_data["tiktok"]:
        lines.append(f"   📹 {item['day'].capitalize()} | {item['format'].replace('_', ' ').title()}")
        lines.append(f"      {item['title']}")
        lines.append(f"      Tema: {item['topic']}")

    lines.append("")
    lines.append("📘 FACEBOOK (3 posts)")
    for item in week_data["facebook"]:
        lines.append(f"   📝 {item['day'].capitalize()} | {item['format'].replace('_', ' ').title()}")
        lines.append(f"      {item['title']}")
        lines.append(f"      Tema: {item['topic']}")

    lines.append("")
    lines.append("💬 COMUNIDAD (participacion en grupos)")
    for item in week_data["community"]:
        lines.append(f"   🗣️ {item['day'].capitalize()} | Grupo: {item['group_type']} | Tema: {item['topic']}")

    lines.append("")

    # Stats
    tiktok_topics = [t["topic"] for t in week_data["tiktok"]]
    fb_topics = [t["topic"] for t in week_data["facebook"]]
    all_topics = tiktok_topics + fb_topics
    unique_topics = set(all_topics)

    lines.append("📊 RESUMEN SEMANAL")
    lines.append(f"   Total piezas: {len(week_data['tiktok'])} TikTok + {len(week_data['facebook'])} Facebook + {len(week_data['community'])} Comunidad")
    lines.append(f"   Temas cubiertos: {', '.join(sorted(unique_topics))}")
    lines.append("")

    return "\n".join(lines)


def format_month_readable(weeks: list) -> str:
    lines = []
    lines.append("*" * 70)
    lines.append("📆 CALENDARIO EDITORIAL — MES 1")
    lines.append(f"   Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lines.append("*" * 70)
    lines.append("")

    total_tiktok = sum(len(w["tiktok"]) for w in weeks)
    total_fb = sum(len(w["facebook"]) for w in weeks)
    total_community = sum(len(w["community"]) for w in weeks)

    lines.append(f"📊 TOTALES DEL MES:")
    lines.append(f"   🎵 TikTok: {total_tiktok} videos")
    lines.append(f"   📘 Facebook: {total_fb} posts")
    lines.append(f"   💬 Comunidad: {total_community} participaciones")
    lines.append(f"   📦 TOTAL: {total_tiktok + total_fb + total_community} piezas de contenido")
    lines.append("")

    for week in weeks:
        lines.append(format_week_readable(week))

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Content Calendar Bot")
    parser.add_argument("--month", type=int, choices=[1], help="Mes a generar (1)")
    parser.add_argument("--week", type=int, choices=[1, 2, 3, 4], help="Semana especifica")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    args = parser.parse_args()

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if args.month:
        weeks = get_month_calendar()
        if args.json:
            out_file = output_dir / f"calendar_month{args.month}_{datetime.now().strftime('%Y%m')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(weeks, f, ensure_ascii=False, indent=2)
            print(f"✅ Calendario guardado en {out_file}")
        else:
            text = format_month_readable(weeks)
            out_file = output_dir / f"calendar_month{args.month}_{datetime.now().strftime('%Y%m')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(text)
            print(f"✅ Calendario guardado en {out_file}")
    elif args.week:
        week_data = get_week_calendar(args.week)
        if not week_data:
            print(f"❌ Semana {args.week} no encontrada.")
            return
        if args.json:
            print(json.dumps(week_data, ensure_ascii=False, indent=2))
        else:
            print(format_week_readable(week_data))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
