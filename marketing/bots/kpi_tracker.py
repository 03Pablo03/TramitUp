"""
BOT 6: KPI Tracker
━━━━━━━━━━━━━━━━━━
Registra, analiza y reporta las metricas clave del marketing.

Funciones:
  - Registrar metricas diarias/semanales
  - Comparar contra objetivos del mes
  - Generar reportes de rendimiento
  - Identificar contenido top performer
  - Sugerir ajustes de estrategia

USO:
  python -m marketing.bots.kpi_tracker --report month1
  python -m marketing.bots.kpi_tracker --log --platform tiktok --metric views --value 2500
  python -m marketing.bots.kpi_tracker --status
  python -m marketing.bots.kpi_tracker --init
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import KPIS


# ─── Estructura de datos KPI ────────────────────────────────────────────────

KPI_DEFINITIONS = {
    "tiktok": {
        "seguidores": {"label": "Seguidores", "unit": ""},
        "views_total": {"label": "Views totales", "unit": ""},
        "views_avg": {"label": "Views por video (media)", "unit": ""},
        "likes_total": {"label": "Likes totales", "unit": ""},
        "comments_total": {"label": "Comentarios totales", "unit": ""},
        "shares_total": {"label": "Compartidos totales", "unit": ""},
        "profile_visits": {"label": "Visitas al perfil", "unit": ""},
        "link_clicks": {"label": "Clics en link bio", "unit": ""},
        "videos_published": {"label": "Videos publicados", "unit": ""},
    },
    "facebook": {
        "seguidores_pagina": {"label": "Seguidores pagina", "unit": ""},
        "alcance_total": {"label": "Alcance total", "unit": ""},
        "engagement_total": {"label": "Engagement total", "unit": ""},
        "link_clicks": {"label": "Clics en link", "unit": ""},
        "posts_published": {"label": "Posts publicados", "unit": ""},
        "group_responses": {"label": "Respuestas en grupos", "unit": ""},
    },
    "conversion": {
        "registros_app": {"label": "Registros en app", "unit": ""},
        "trials_started": {"label": "Trials iniciados", "unit": ""},
        "conversions_pro": {"label": "Conversiones a PRO", "unit": ""},
        "conversion_rate": {"label": "Tasa de conversion", "unit": "%"},
    },
}

DATA_FILE = Path(__file__).resolve().parent.parent / "output" / "kpi_data.json"


def load_data() -> dict:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"entries": [], "created_at": datetime.now().isoformat()}


def save_data(data: dict):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def init_tracking():
    """Inicializa el archivo de tracking."""
    data = {
        "entries": [],
        "created_at": datetime.now().isoformat(),
        "targets": {
            "mes_1": KPIS["mes_1"],
            "mes_3": KPIS["mes_3"],
        },
    }
    save_data(data)
    return data


def log_metric(platform: str, metric: str, value: float, date: str = None, notes: str = ""):
    """Registra una metrica."""
    data = load_data()
    entry = {
        "date": date or datetime.now().strftime("%Y-%m-%d"),
        "platform": platform,
        "metric": metric,
        "value": value,
        "notes": notes,
        "logged_at": datetime.now().isoformat(),
    }
    data["entries"].append(entry)
    save_data(data)
    return entry


def get_latest_values() -> dict:
    """Obtiene los ultimos valores registrados por metrica."""
    data = load_data()
    latest = {}
    for entry in data["entries"]:
        key = f"{entry['platform']}_{entry['metric']}"
        if key not in latest or entry["date"] > latest[key]["date"]:
            latest[key] = entry
    return latest


def generate_status_report() -> dict:
    """Genera un reporte de estado actual."""
    data = load_data()
    latest = get_latest_values()
    targets = KPIS["mes_1"]

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_entries": len(data["entries"]),
        "platforms": {},
        "targets_comparison": [],
        "recommendations": [],
    }

    # Aggregate by platform
    for platform, metrics in KPI_DEFINITIONS.items():
        platform_data = {}
        for metric_key, metric_info in metrics.items():
            full_key = f"{platform}_{metric_key}"
            if full_key in latest:
                platform_data[metric_key] = {
                    "label": metric_info["label"],
                    "value": latest[full_key]["value"],
                    "date": latest[full_key]["date"],
                }
        if platform_data:
            report["platforms"][platform] = platform_data

    # Compare against targets
    target_mappings = {
        "seguidores_tiktok": ("tiktok", "seguidores"),
        "views_por_video": ("tiktok", "views_avg"),
        "seguidores_facebook": ("facebook", "seguidores_pagina"),
        "registros_app": ("conversion", "registros_app"),
        "conversion_trial": ("conversion", "conversion_rate"),
    }

    for target_key, (platform, metric) in target_mappings.items():
        if target_key in targets:
            low, high = targets[target_key]
            full_key = f"{platform}_{metric}"
            current = latest[full_key]["value"] if full_key in latest else 0
            status = "above" if current >= high else "on_track" if current >= low else "below"
            report["targets_comparison"].append({
                "metric": target_key,
                "current": current,
                "target_low": low,
                "target_high": high,
                "status": status,
            })

    # Generate recommendations
    for comparison in report["targets_comparison"]:
        if comparison["status"] == "below":
            report["recommendations"].append(
                f"⚠️ {comparison['metric']}: {comparison['current']} vs objetivo {comparison['target_low']}-{comparison['target_high']}. "
                f"Necesita atencion."
            )
        elif comparison["status"] == "above":
            report["recommendations"].append(
                f"🎯 {comparison['metric']}: {comparison['current']} — superando objetivo. Mantener estrategia."
            )

    if not report["recommendations"]:
        report["recommendations"].append(
            "📊 Sin datos suficientes. Registra metricas con --log para obtener recomendaciones."
        )

    return report


def generate_month_report() -> dict:
    """Genera reporte completo del mes."""
    data = load_data()
    entries = data["entries"]

    # Group by week
    weeks = {}
    for entry in entries:
        date = datetime.strptime(entry["date"], "%Y-%m-%d")
        week_num = date.isocalendar()[1]
        if week_num not in weeks:
            weeks[week_num] = []
        weeks[week_num].append(entry)

    report = {
        "generated_at": datetime.now().isoformat(),
        "period": "Mes 1",
        "total_data_points": len(entries),
        "weeks_tracked": len(weeks),
        "weekly_breakdown": {},
        "totals": {},
        "targets": KPIS["mes_1"],
        "status": generate_status_report(),
    }

    for week_num, week_entries in sorted(weeks.items()):
        week_summary = {}
        for entry in week_entries:
            key = f"{entry['platform']}_{entry['metric']}"
            if key not in week_summary:
                week_summary[key] = {"values": [], "platform": entry["platform"], "metric": entry["metric"]}
            week_summary[key]["values"].append(entry["value"])

        report["weekly_breakdown"][f"week_{week_num}"] = {
            k: {"avg": sum(v["values"]) / len(v["values"]), "max": max(v["values"]), "count": len(v["values"])}
            for k, v in week_summary.items()
        }

    return report


def format_status_readable(report: dict) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("📊 ESTADO KPIs — TRAMITUP MARKETING")
    lines.append(f"   Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lines.append(f"   Datos registrados: {report['total_entries']}")
    lines.append("=" * 70)
    lines.append("")

    for platform, metrics in report["platforms"].items():
        lines.append(f"📈 {platform.upper()}")
        for key, data in metrics.items():
            lines.append(f"   {data['label']}: {data['value']} (actualizado: {data['date']})")
        lines.append("")

    if report["targets_comparison"]:
        lines.append("🎯 OBJETIVOS MES 1")
        for comp in report["targets_comparison"]:
            icon = "✅" if comp["status"] == "above" else "🟡" if comp["status"] == "on_track" else "🔴"
            lines.append(
                f"   {icon} {comp['metric']}: {comp['current']} "
                f"(objetivo: {comp['target_low']}-{comp['target_high']})"
            )
        lines.append("")

    lines.append("💡 RECOMENDACIONES")
    for rec in report["recommendations"]:
        lines.append(f"   {rec}")
    lines.append("")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="KPI Tracker Bot")
    parser.add_argument("--init", action="store_true", help="Inicializar tracking")
    parser.add_argument("--log", action="store_true", help="Registrar metrica")
    parser.add_argument("--platform", choices=["tiktok", "facebook", "conversion"], help="Plataforma")
    parser.add_argument("--metric", type=str, help="Nombre de la metrica")
    parser.add_argument("--value", type=float, help="Valor")
    parser.add_argument("--date", type=str, help="Fecha (YYYY-MM-DD)")
    parser.add_argument("--notes", type=str, default="", help="Notas")
    parser.add_argument("--status", action="store_true", help="Ver estado actual")
    parser.add_argument("--report", choices=["month1"], help="Generar reporte")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    args = parser.parse_args()

    if args.init:
        data = init_tracking()
        print(f"✅ Tracking inicializado. Archivo: {DATA_FILE}")
        print(f"   Objetivos cargados para mes 1 y mes 3.")
    elif args.log:
        if not args.platform or not args.metric or args.value is None:
            print("❌ Necesitas --platform, --metric y --value")
            return
        entry = log_metric(args.platform, args.metric, args.value, args.date, args.notes)
        print(f"✅ Registrado: {entry['platform']}/{entry['metric']} = {entry['value']} ({entry['date']})")
    elif args.status:
        report = generate_status_report()
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(format_status_readable(report))
    elif args.report:
        report = generate_month_report()
        if args.json:
            output_dir = Path(__file__).resolve().parent.parent / "output"
            out_file = output_dir / f"report_{args.report}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"✅ Reporte guardado en {out_file}")
        else:
            print(format_status_readable(report["status"]))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
