"""
TramitUp Marketing CLI
━━━━━━━━━━━━━━━━━━━━━━
Runner principal que orquesta todos los bots de marketing.

CONTENIDO (sin API):
  python -m marketing.run tiktok --all              Genera todos los guiones TikTok del mes
  python -m marketing.run tiktok --topic multas     Genera un guion de TikTok sobre multas
  python -m marketing.run facebook --all            Genera todos los posts de Facebook del mes
  python -m marketing.run facebook --topic alquiler Genera un post de Facebook sobre alquiler
  python -m marketing.run community --templates     Genera todas las plantillas de respuesta
  python -m marketing.run community --topic laboral Genera respuesta sobre tema laboral
  python -m marketing.run calendar --month 1        Genera calendario completo del mes
  python -m marketing.run calendar --week 2         Genera calendario de la semana 2
  python -m marketing.run caption --platform tiktok --topic multas
  python -m marketing.run kpi --status              Ver estado de KPIs
  python -m marketing.run all                       Genera TODO el contenido del mes 1

IA (requiere ANTHROPIC_API_KEY):
  python -m marketing.run trends                             Detectar tendencias legales
  python -m marketing.run trends --category laboral          Tendencias por categoria
  python -m marketing.run reply --comment "texto"            Responder a un comentario
  python -m marketing.run reply --file comments.json         Procesar batch de comentarios
  python -m marketing.run repurpose --topic multas           Repurposear guion a multi-plataforma
  python -m marketing.run repurpose --all-month              Repurposear todo el mes
  python -m marketing.run titles --topic alquiler            Generar variantes A/B de titulo
  python -m marketing.run titles --topic laboral --angle "despido sin preaviso"
  python -m marketing.run faqs --category alquiler           Buscar FAQs reales
  python -m marketing.run faqs --all                         FAQs de todas las categorias

VIDEO (requiere Node.js + Puppeteer + FFmpeg + GOOGLE_API_KEY):
  python -m marketing.run video --check                      Verificar dependencias
  python -m marketing.run video --list-scripts               Ver scripts disponibles
  python -m marketing.run video --script demo_basico         Generar video de demo
"""

import sys
import json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _get_arg(args: list, flag: str, default=None):
    """Extrae el valor de un flag de los args."""
    if flag in args:
        idx = args.index(flag)
        if idx + 1 < len(args):
            return args[idx + 1]
    return default


def _has_flag(args: list, flag: str) -> bool:
    return flag in args


# ─── Bot runners ─────────────────────────────────────────────────────────────

def run_tiktok(args):
    from marketing.bots.tiktok_scriptwriter import generate_script, generate_full_month, format_script_readable

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    if _has_flag(args, "--all"):
        scripts = generate_full_month()
        if _has_flag(args, "--json"):
            out_file = output_dir / f"tiktok_month_{datetime.now().strftime('%Y%m')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(scripts, f, ensure_ascii=False, indent=2)
        else:
            full_text = "\n".join(format_script_readable(s) for s in scripts)
            out_file = output_dir / f"tiktok_month_{datetime.now().strftime('%Y%m')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(full_text)
        print(f"✅ {len(scripts)} guiones TikTok guardados en {out_file}")
    elif _has_flag(args, "--topic"):
        topic = _get_arg(args, "--topic")
        fmt = _get_arg(args, "--format")
        script = generate_script(topic, fmt)
        if _has_flag(args, "--json"):
            print(json.dumps(script, ensure_ascii=False, indent=2))
        else:
            print(format_script_readable(script))
    else:
        print("Uso: marketing.run tiktok [--all | --topic TEMA] [--format FORMATO] [--json]")


def run_facebook(args):
    from marketing.bots.facebook_posts import generate_post, generate_full_month, format_post_readable

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    if _has_flag(args, "--all"):
        posts = generate_full_month()
        if _has_flag(args, "--json"):
            out_file = output_dir / f"facebook_month_{datetime.now().strftime('%Y%m')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)
        else:
            full_text = "\n".join(format_post_readable(p) for p in posts)
            out_file = output_dir / f"facebook_month_{datetime.now().strftime('%Y%m')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(full_text)
        print(f"✅ {len(posts)} posts Facebook guardados en {out_file}")
    elif _has_flag(args, "--topic"):
        topic = _get_arg(args, "--topic")
        fmt = _get_arg(args, "--format")
        post = generate_post(topic, fmt)
        if _has_flag(args, "--json"):
            print(json.dumps(post, ensure_ascii=False, indent=2))
        else:
            print(format_post_readable(post))
    else:
        print("Uso: marketing.run facebook [--all | --topic TEMA] [--format FORMATO] [--json]")


def run_community(args):
    from marketing.bots.community_bot import generate_response, generate_all_templates, format_response_readable

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    if _has_flag(args, "--templates"):
        responses = generate_all_templates()
        if _has_flag(args, "--json"):
            out_file = output_dir / f"community_templates_{datetime.now().strftime('%Y%m%d')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(responses, f, ensure_ascii=False, indent=2)
        else:
            full_text = "\n".join(format_response_readable(r) for r in responses)
            out_file = output_dir / f"community_templates_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(full_text)
        print(f"✅ {len(responses)} plantillas guardadas en {out_file}")
    elif _has_flag(args, "--topic"):
        topic = _get_arg(args, "--topic")
        question = _get_arg(args, "--question")
        resp = generate_response(topic, question)
        if _has_flag(args, "--json"):
            print(json.dumps(resp, ensure_ascii=False, indent=2))
        else:
            print(format_response_readable(resp))
    else:
        print("Uso: marketing.run community [--templates | --topic TEMA --question PREGUNTA] [--json]")


def run_calendar(args):
    from marketing.bots.calendar_bot import get_month_calendar, get_week_calendar, format_month_readable, format_week_readable

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    if _has_flag(args, "--month"):
        weeks = get_month_calendar()
        if _has_flag(args, "--json"):
            out_file = output_dir / f"calendar_{datetime.now().strftime('%Y%m')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(weeks, f, ensure_ascii=False, indent=2)
        else:
            text = format_month_readable(weeks)
            out_file = output_dir / f"calendar_{datetime.now().strftime('%Y%m')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(text)
        print(f"✅ Calendario guardado en {out_file}")
    elif _has_flag(args, "--week"):
        week = int(_get_arg(args, "--week", "1"))
        week_data = get_week_calendar(week)
        if _has_flag(args, "--json"):
            print(json.dumps(week_data, ensure_ascii=False, indent=2))
        else:
            print(format_week_readable(week_data))
    else:
        print("Uso: marketing.run calendar [--month 1 | --week N] [--json]")


def run_caption(args):
    from marketing.bots.caption_optimizer import generate_caption, generate_ab_variants, format_caption_readable

    if not _has_flag(args, "--platform"):
        print("Uso: marketing.run caption --platform [tiktok|facebook] --topic TEMA [--ab] [--json]")
        return

    platform = _get_arg(args, "--platform", "tiktok")
    topic = _get_arg(args, "--topic")
    title = _get_arg(args, "--title")

    if _has_flag(args, "--ab") and topic:
        ab = generate_ab_variants(platform, topic)
        if _has_flag(args, "--json"):
            print(json.dumps(ab, ensure_ascii=False, indent=2))
        else:
            print("--- VARIANTE A ---")
            print(format_caption_readable(ab["variant_a"]))
            print("--- VARIANTE B ---")
            print(format_caption_readable(ab["variant_b"]))
    elif topic:
        result = generate_caption(platform, topic, title)
        if _has_flag(args, "--json"):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_caption_readable(result))
    else:
        print("Necesitas --topic TEMA")


def run_kpi(args):
    from marketing.bots.kpi_tracker import init_tracking, log_metric, generate_status_report, generate_month_report, format_status_readable

    if _has_flag(args, "--init"):
        init_tracking()
        print("✅ KPI tracking inicializado.")
    elif _has_flag(args, "--log"):
        platform = _get_arg(args, "--platform")
        metric = _get_arg(args, "--metric")
        value_str = _get_arg(args, "--value")
        value = float(value_str) if value_str else None
        if platform and metric and value is not None:
            entry = log_metric(platform, metric, value)
            print(f"✅ Registrado: {entry['platform']}/{entry['metric']} = {entry['value']}")
        else:
            print("Necesitas: --platform, --metric, --value")
    elif _has_flag(args, "--status"):
        report = generate_status_report()
        if _has_flag(args, "--json"):
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(format_status_readable(report))
    elif _has_flag(args, "--report"):
        report = generate_month_report()
        if _has_flag(args, "--json"):
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(format_status_readable(report["status"]))
    else:
        print("Uso: marketing.run kpi [--init | --status | --log --platform X --metric Y --value Z | --report month1]")


# ─── NEW BOTS (IA) ──────────────────────────────────────────────────────────

def run_trends(args):
    from marketing.bots.trend_detector import detect_trends, format_trends_readable

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    category = _get_arg(args, "--category", "general")
    print(f"🔍 Buscando tendencias ({category})...")
    result = detect_trends(category)

    if _has_flag(args, "--json"):
        out_file = output_dir / f"trends_{category}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"\n✅ Guardado en {out_file}")
    else:
        text = format_trends_readable(result)
        out_file = output_dir / f"trends_{category}_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(text)
        print(f"✅ Guardado en {out_file}")


def run_reply(args):
    from marketing.bots.comment_reply import classify_and_reply, process_comments_batch, format_reply_readable

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    platform = _get_arg(args, "--platform", "tiktok")
    context = _get_arg(args, "--context", "")

    if _has_flag(args, "--comment"):
        comment = _get_arg(args, "--comment")
        result = classify_and_reply(comment, platform, context)
        if _has_flag(args, "--json"):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_reply_readable(result))
    elif _has_flag(args, "--file"):
        file_path = Path(_get_arg(args, "--file"))
        if not file_path.exists():
            print(f"❌ Archivo no encontrado: {file_path}")
            return
        with open(file_path, "r", encoding="utf-8") as f:
            comments = json.load(f)
        if not isinstance(comments, list):
            comments = [comments]
        print(f"📝 Procesando {len(comments)} comentarios ({platform})...")
        results = process_comments_batch(comments, platform)

        if _has_flag(args, "--json"):
            out_file = output_dir / f"replies_{platform}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ {len(results)} respuestas guardadas en {out_file}")
        else:
            for r in results:
                print(format_reply_readable(r))
    else:
        print("Uso: marketing.run reply [--comment TEXTO | --file comments.json] [--platform tiktok|facebook] [--json]")


def run_repurpose(args):
    from marketing.bots.content_repurposer import repurpose_script, format_repurposed_readable

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    if _has_flag(args, "--file"):
        file_path = _get_arg(args, "--file")
        with open(file_path, "r", encoding="utf-8") as f:
            scripts = json.load(f)
        if not isinstance(scripts, list):
            scripts = [scripts]
        results = []
        for i, s in enumerate(scripts, 1):
            print(f"♻️  [{i}/{len(scripts)}] {s.get('metadata', {}).get('title', '?')[:50]}...")
            results.append(repurpose_script(s))
        if _has_flag(args, "--json"):
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for r in results:
                print(format_repurposed_readable(r))
    elif _has_flag(args, "--topic"):
        topic = _get_arg(args, "--topic")
        fmt = _get_arg(args, "--format")
        from marketing.bots.tiktok_scriptwriter import generate_script
        print(f"🎵 Generando guion TikTok ({topic})...")
        script = generate_script(topic, fmt)
        print(f"♻️  Repurposeando a multi-plataforma...")
        result = repurpose_script(script)
        if _has_flag(args, "--json"):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_repurposed_readable(result))
            out_file = output_dir / f"repurposed_{topic}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(format_repurposed_readable(result))
            print(f"✅ Guardado en {out_file}")
    elif _has_flag(args, "--all-month"):
        from marketing.bots.tiktok_scriptwriter import generate_full_month
        scripts = generate_full_month()
        results = []
        for i, s in enumerate(scripts, 1):
            print(f"♻️  [{i}/{len(scripts)}] {s.get('metadata', {}).get('title', '?')[:50]}...")
            results.append(repurpose_script(s))
        out_file = output_dir / f"repurposed_month_{datetime.now().strftime('%Y%m')}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ {len(results)} piezas repurposeadas en {out_file}")
    else:
        print("Uso: marketing.run repurpose [--topic TEMA | --file script.json | --all-month] [--json]")


def run_titles(args):
    from marketing.bots.ab_title_tester import generate_title_variants, format_variants_readable

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    if not _has_flag(args, "--topic"):
        print("Uso: marketing.run titles --topic TEMA [--angle ANGULO] [--json]")
        return

    topic = _get_arg(args, "--topic")
    angle = _get_arg(args, "--angle")

    print(f"🧪 Generando variantes de titulo ({topic})...")
    result = generate_title_variants(topic, angle)
    if _has_flag(args, "--json"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_variants_readable(result))
        out_file = output_dir / f"titles_{topic}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(format_variants_readable(result))
        print(f"✅ Guardado en {out_file}")


def run_faqs(args):
    from marketing.bots.faq_scraper import scrape_faqs, scrape_all_categories, format_faqs_readable

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    limit = int(_get_arg(args, "--limit", "8"))

    if _has_flag(args, "--all"):
        print(f"🔍 Scrapeando FAQs de todas las categorias...")
        results = scrape_all_categories(limit)
        total = sum(len(r.get("questions", [])) for r in results if "error" not in r)
        if _has_flag(args, "--json"):
            out_file = output_dir / f"faqs_all_{datetime.now().strftime('%Y%m%d')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n✅ {total} preguntas guardadas en {out_file}")
        else:
            for r in results:
                print(format_faqs_readable(r))
    elif _has_flag(args, "--category"):
        category = _get_arg(args, "--category")
        print(f"🔍 Buscando FAQs sobre {category}...")
        result = scrape_faqs(category, limit)
        if _has_flag(args, "--json"):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_faqs_readable(result))
    else:
        print("Uso: marketing.run faqs [--category TEMA | --all] [--limit N] [--json]")


def run_video(args):
    from marketing.bots.video_assembly import check_dependencies, run_pipeline, DEMO_SCRIPTS

    if _has_flag(args, "--check"):
        deps = check_dependencies()
        all_ok = all(d["ok"] for d in deps.values())
        print("🔧 VERIFICACION DE DEPENDENCIAS")
        print("=" * 50)
        for name, info in deps.items():
            icon = "✅" if info["ok"] else "❌"
            detail = info.get("version") or info.get("path") or info.get("note", "")
            print(f"   {icon} {name}: {detail}")
        if all_ok:
            print("\n🎉 Todas las dependencias OK.")
        else:
            missing = [k for k, v in deps.items() if not v["ok"]]
            print(f"\n⚠️  Faltantes: {', '.join(missing)}")
    elif _has_flag(args, "--list-scripts"):
        print("📜 SCRIPTS DISPONIBLES:")
        for name, demo in DEMO_SCRIPTS.items():
            dur = sum(s["duration"] for s in demo["scenes"])
            print(f"   📹 {name}: {demo['title']} ({dur}s, {len(demo['scenes'])} escenas)")
    elif _has_flag(args, "--script"):
        script_name = _get_arg(args, "--script")
        skip = _has_flag(args, "--skip-capture")
        result = run_pipeline(script_name, skip)
        if _has_flag(args, "--json"):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif result.get("output"):
            print(f"\n🎉 Video generado: {result['output']}")
        else:
            print("\n⚠️  Pipeline completado con errores.")
    else:
        print("Uso: marketing.run video [--check | --list-scripts | --script NOMBRE] [--skip-capture] [--json]")


# ─── run all ─────────────────────────────────────────────────────────────────

def run_all():
    """Genera TODO el contenido del Mes 1 (bots sin IA)."""
    print("🚀 GENERANDO CONTENIDO COMPLETO — MES 1")
    print("=" * 50)

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    print("\n🎵 Generando guiones TikTok...")
    from marketing.bots.tiktok_scriptwriter import generate_full_month as tiktok_month, format_script_readable
    tiktok_scripts = tiktok_month()
    with open(output_dir / f"tiktok_month_{datetime.now().strftime('%Y%m')}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(format_script_readable(s) for s in tiktok_scripts))
    print(f"   ✅ {len(tiktok_scripts)} guiones TikTok")

    print("📘 Generando posts Facebook...")
    from marketing.bots.facebook_posts import generate_full_month as fb_month, format_post_readable
    fb_posts = fb_month()
    with open(output_dir / f"facebook_month_{datetime.now().strftime('%Y%m')}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(format_post_readable(p) for p in fb_posts))
    print(f"   ✅ {len(fb_posts)} posts Facebook")

    print("💬 Generando plantillas de comunidad...")
    from marketing.bots.community_bot import generate_all_templates, format_response_readable
    community = generate_all_templates()
    with open(output_dir / f"community_templates_{datetime.now().strftime('%Y%m%d')}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(format_response_readable(r) for r in community))
    print(f"   ✅ {len(community)} plantillas de comunidad")

    print("📅 Generando calendario editorial...")
    from marketing.bots.calendar_bot import get_month_calendar, format_month_readable
    calendar = get_month_calendar()
    with open(output_dir / f"calendar_{datetime.now().strftime('%Y%m')}.txt", "w", encoding="utf-8") as f:
        f.write(format_month_readable(calendar))
    print(f"   ✅ Calendario de {len(calendar)} semanas")

    print("📊 Inicializando KPI tracker...")
    from marketing.bots.kpi_tracker import init_tracking
    init_tracking()
    print("   ✅ KPI tracker listo")

    summary = {
        "generated_at": datetime.now().isoformat(),
        "month": 1,
        "content": {
            "tiktok_scripts": len(tiktok_scripts),
            "facebook_posts": len(fb_posts),
            "community_templates": len(community),
            "calendar_weeks": len(calendar),
        },
        "output_dir": str(output_dir),
    }
    with open(output_dir / "generation_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 50}")
    print(f"🎉 CONTENIDO GENERADO:")
    print(f"   🎵 {len(tiktok_scripts)} guiones TikTok")
    print(f"   📘 {len(fb_posts)} posts Facebook")
    print(f"   💬 {len(community)} respuestas comunidad")
    print(f"   📅 Calendario de {len(calendar)} semanas")
    print(f"   📊 KPI tracker inicializado")
    print(f"\n   📁 Todo en: {output_dir}")
    print(f"\n💡 Para bots con IA: trends, reply, repurpose, titles, faqs (requieren ANTHROPIC_API_KEY)")


# ─── Command registry ───────────────────────────────────────────────────────

COMMANDS = {
    # Content bots (sin API)
    "tiktok": run_tiktok,
    "facebook": run_facebook,
    "community": run_community,
    "calendar": run_calendar,
    "caption": run_caption,
    "kpi": run_kpi,
    "all": lambda _: run_all(),
    # AI bots (requieren ANTHROPIC_API_KEY)
    "trends": run_trends,
    "reply": run_reply,
    "repurpose": run_repurpose,
    "titles": run_titles,
    "faqs": run_faqs,
    # Video bot (requiere Node.js + Puppeteer + FFmpeg + GOOGLE_API_KEY)
    "video": run_video,
}


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        print("Comandos disponibles:")
        print("\n  📦 Contenido (sin API):")
        for cmd in ["tiktok", "facebook", "community", "calendar", "caption", "kpi", "all"]:
            print(f"    {cmd}")
        print("\n  🤖 IA (requiere ANTHROPIC_API_KEY):")
        for cmd in ["trends", "reply", "repurpose", "titles", "faqs"]:
            print(f"    {cmd}")
        print("\n  🎬 Video (requiere Node.js + Puppeteer + FFmpeg + GOOGLE_API_KEY):")
        for cmd in ["video"]:
            print(f"    {cmd}")
        return

    command = args[0]
    if command not in COMMANDS:
        print(f"❌ Comando '{command}' no encontrado.")
        print(f"Comandos: {', '.join(COMMANDS.keys())}")
        return

    COMMANDS[command](args[1:])


if __name__ == "__main__":
    main()
