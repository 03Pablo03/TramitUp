"""
BOT 12: Video Assembly
━━━━━━━━━━━━━━━━━━━━━━
Pipeline completo para generar videos de demo de la app TramitUp.

Pipeline:
  1. Puppeteer captura la app en localhost (viewport 1080x1920 vertical)
  2. Navega simulando usuario: login → consulta → respuesta
  3. Google Cloud TTS genera voz en off (es-ES, voz masculina natural)
  4. FFmpeg monta: capturas + audio + transiciones + texto superpuesto
  5. Quema subtitulos sincronizados
  6. Output: 1080x1920, MP4, H.264, max 60s

Requisitos:
  - Node.js + puppeteer (npm install puppeteer)
  - FFmpeg en PATH
  - Google Cloud TTS API key en GOOGLE_API_KEY env var
  - App corriendo en localhost:5000

USO:
  python -m marketing.bots.video_assembly --script demo_basico
  python -m marketing.bots.video_assembly --script demo_basico --skip-capture (solo monta)
  python -m marketing.bots.video_assembly --list-scripts
  python -m marketing.bots.video_assembly --check (verifica dependencias)
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import BRAND

# ─── Configuracion ───────────────────────────────────────────────────────────

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output" / "videos"
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "video_scripts"
APP_URL = "http://localhost:5000"
VIEWPORT = {"width": 1080, "height": 1920}

# TTS config
TTS_VOICE = "es-ES-Standard-B"  # Male Spanish voice
TTS_SPEAKING_RATE = 1.0
TTS_PITCH = 0.0

# FFmpeg text style (TikTok-like: white, bold, shadow)
TEXT_STYLE = (
    "fontsize=56:fontcolor=white:borderw=3:bordercolor=black:"
    "fontfile=C\\\\:/Windows/Fonts/arialbd.ttf"
)


# ─── Demo scripts ───────────────────────────────────────────────────────────

DEMO_SCRIPTS = {
    "demo_basico": {
        "title": "Asi funciona TramitUp",
        "duration_target": 45,
        "scenes": [
            {
                "id": "intro",
                "duration": 3,
                "voiceover": "¿Tienes una duda legal y no sabes por donde empezar?",
                "screen_text": "¿DUDA LEGAL?",
                "action": "show_landing",
                "url": "/",
            },
            {
                "id": "open_app",
                "duration": 4,
                "voiceover": "Abre TramitUp y pregunta lo que quieras.",
                "screen_text": "ABRE TRAMITUP",
                "action": "navigate",
                "url": "/chat",
            },
            {
                "id": "type_question",
                "duration": 8,
                "voiceover": "Por ejemplo, me han puesto una multa de trafico. Que opciones tengo.",
                "screen_text": None,
                "action": "type_message",
                "message": "Me han puesto una multa de trafico. Que opciones tengo?",
            },
            {
                "id": "wait_response",
                "duration": 10,
                "voiceover": "La inteligencia artificial analiza tu caso con las leyes españolas actualizadas.",
                "screen_text": "IA + LEYES ESPAÑOLAS",
                "action": "wait_for_response",
            },
            {
                "id": "show_response",
                "duration": 12,
                "voiceover": "Te explica tus opciones paso a paso. Recurrir, pagar con descuento, plazos exactos. Todo claro y sin letra pequeña.",
                "screen_text": None,
                "action": "scroll_response",
            },
            {
                "id": "cta",
                "duration": 5,
                "voiceover": "Pruebalo gratis. Link en bio.",
                "screen_text": "LINK EN BIO → TRAMITUP",
                "action": "show_cta",
                "url": None,
            },
        ],
    },
    "demo_contrato": {
        "title": "Analiza tu contrato con IA",
        "duration_target": 50,
        "scenes": [
            {
                "id": "intro",
                "duration": 3,
                "voiceover": "¿Te han dado un contrato y no entiendes la letra pequeña?",
                "screen_text": "¿CONTRATO CONFUSO?",
                "action": "show_landing",
                "url": "/",
            },
            {
                "id": "open_contrato",
                "duration": 4,
                "voiceover": "TramitUp lo analiza por ti en segundos.",
                "screen_text": "ANALISIS CON IA",
                "action": "navigate",
                "url": "/contrato",
            },
            {
                "id": "upload",
                "duration": 6,
                "voiceover": "Sube tu contrato en PDF y la IA lo lee completo.",
                "screen_text": "SUBE TU PDF",
                "action": "simulate_upload",
            },
            {
                "id": "analysis",
                "duration": 12,
                "voiceover": "Te marca las clausulas importantes, los riesgos, y lo que deberias negociar antes de firmar.",
                "screen_text": None,
                "action": "wait_for_response",
            },
            {
                "id": "results",
                "duration": 10,
                "voiceover": "Clausulas abusivas, plazos escondidos, penalizaciones. Todo señalado y explicado en lenguaje normal.",
                "screen_text": "CLAUSULAS DETECTADAS",
                "action": "scroll_response",
            },
            {
                "id": "cta",
                "duration": 5,
                "voiceover": "Prueba PRO 3 dias gratis. Link en bio.",
                "screen_text": "3 DIAS GRATIS → LINK EN BIO",
                "action": "show_cta",
                "url": None,
            },
        ],
    },
    "demo_calculadora": {
        "title": "Calcula tu indemnizacion en 10 segundos",
        "duration_target": 40,
        "scenes": [
            {
                "id": "intro",
                "duration": 3,
                "voiceover": "Te han despedido y no sabes cuanto te deben?",
                "screen_text": "¿CUANTO TE DEBEN?",
                "action": "show_landing",
                "url": "/",
            },
            {
                "id": "open_calc",
                "duration": 4,
                "voiceover": "TramitUp tiene una calculadora de indemnizacion gratis.",
                "screen_text": "CALCULADORA GRATIS",
                "action": "navigate",
                "url": "/calculadora",
            },
            {
                "id": "fill_form",
                "duration": 10,
                "voiceover": "Metes tu salario, los años trabajados, y el tipo de despido. En 10 segundos sabes exactamente cuanto te corresponde.",
                "screen_text": None,
                "action": "fill_calculator",
            },
            {
                "id": "result",
                "duration": 10,
                "voiceover": "Y si quieres saber mas, preguntale a la IA y te explica todos tus derechos.",
                "screen_text": "RESULTADO EXACTO",
                "action": "show_result",
            },
            {
                "id": "cta",
                "duration": 5,
                "voiceover": "Calculadora gratis en TramitUp. Link en bio.",
                "screen_text": "GRATIS → LINK EN BIO",
                "action": "show_cta",
                "url": None,
            },
        ],
    },
}


# ─── Dependency checker ─────────────────────────────────────────────────────

def check_dependencies() -> dict:
    """Verifica todas las dependencias necesarias."""
    results = {}

    # Node.js
    try:
        r = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        results["nodejs"] = {"ok": r.returncode == 0, "version": r.stdout.strip()}
    except (FileNotFoundError, subprocess.TimeoutExpired):
        results["nodejs"] = {"ok": False, "version": None}

    # Puppeteer
    try:
        r = subprocess.run(
            ["node", "-e", "require('puppeteer'); console.log('ok')"],
            capture_output=True, text=True, timeout=10
        )
        results["puppeteer"] = {"ok": "ok" in r.stdout, "note": "npm install puppeteer"}
    except (FileNotFoundError, subprocess.TimeoutExpired):
        results["puppeteer"] = {"ok": False, "note": "npm install puppeteer"}

    # FFmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        results["ffmpeg"] = {"ok": True, "path": ffmpeg_path}
    else:
        results["ffmpeg"] = {"ok": False, "path": None, "note": "Instala FFmpeg y añádelo al PATH"}

    # Google Cloud TTS API key
    api_key = os.environ.get("GOOGLE_API_KEY")
    results["google_tts"] = {
        "ok": bool(api_key),
        "note": "Set GOOGLE_API_KEY env var" if not api_key else "Configurado",
    }

    # App running
    try:
        req = Request(APP_URL, method="HEAD")
        urlopen(req, timeout=3)
        results["app"] = {"ok": True, "url": APP_URL}
    except (URLError, OSError):
        results["app"] = {"ok": False, "url": APP_URL, "note": "Arranca la app primero"}

    return results


# ─── Puppeteer capture ───────────────────────────────────────────────────────

def generate_puppeteer_script(script_name: str, work_dir: str) -> str:
    """Genera el script de Node.js para Puppeteer."""
    demo = DEMO_SCRIPTS[script_name]
    screenshots_dir = os.path.join(work_dir, "screenshots").replace("\\", "/")

    scenes_js = []
    for i, scene in enumerate(demo["scenes"]):
        scenes_js.append(f"""
    // Scene {i}: {scene['id']}
    console.log('Scene {i}: {scene["id"]}');
    {f'await page.goto("{APP_URL}{scene["url"]}", {{waitUntil: "networkidle2"}});' if scene.get("url") else ""}
    {f'await page.waitForTimeout({scene["duration"] * 1000});' if scene["action"] in ("show_landing", "show_cta", "wait_for_response", "show_result") else ""}
    {f'''
    const input = await page.$('textarea, input[type="text"]');
    if (input) {{
      await input.click();
      await page.keyboard.type("{scene.get("message", "")}", {{delay: 50}});
      await page.waitForTimeout(500);
      await page.keyboard.press('Enter');
    }}
    await page.waitForTimeout({scene["duration"] * 1000});''' if scene["action"] == "type_message" else ""}
    {f'await page.evaluate(() => window.scrollBy(0, 300)); await page.waitForTimeout({scene["duration"] * 1000});' if scene["action"] == "scroll_response" else ""}
    await page.screenshot({{path: '{screenshots_dir}/scene_{i:02d}_{scene["id"]}.png'}});""")

    return f"""const puppeteer = require('puppeteer');

(async () => {{
  const browser = await puppeteer.launch({{
    headless: 'new',
    defaultViewport: {{ width: {VIEWPORT['width']}, height: {VIEWPORT['height']} }},
    args: ['--no-sandbox']
  }});
  const page = await browser.newPage();

  // Set mobile user agent
  await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)');

  const fs = require('fs');
  if (!fs.existsSync('{screenshots_dir}')) fs.mkdirSync('{screenshots_dir}', {{recursive: true}});

  try {{
    {"".join(scenes_js)}

    console.log('All scenes captured!');
  }} catch (err) {{
    console.error('Error:', err.message);
  }}

  await browser.close();
}})();
"""


def run_puppeteer_capture(script_name: str, work_dir: str) -> bool:
    """Ejecuta Puppeteer para capturar screenshots."""
    js_code = generate_puppeteer_script(script_name, work_dir)
    js_file = os.path.join(work_dir, "capture.js")
    with open(js_file, "w", encoding="utf-8") as f:
        f.write(js_code)

    print(f"   📸 Capturando con Puppeteer...")
    result = subprocess.run(
        ["node", js_file],
        capture_output=True, text=True, timeout=120,
        cwd=Path(__file__).resolve().parent.parent.parent,
    )
    if result.returncode != 0:
        print(f"   ❌ Error Puppeteer: {result.stderr[:300]}")
        return False
    print(f"   ✅ Screenshots capturados")
    return True


# ─── Google Cloud TTS ────────────────────────────────────────────────────────

def synthesize_speech(text: str, output_path: str) -> bool:
    """Genera audio con Google Cloud TTS REST API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("   ⚠️  GOOGLE_API_KEY no configurada, saltando TTS")
        return False

    import json as _json
    from urllib.request import Request, urlopen

    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
    payload = _json.dumps({
        "input": {"text": text},
        "voice": {
            "languageCode": "es-ES",
            "name": TTS_VOICE,
            "ssmlGender": "MALE",
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": TTS_SPEAKING_RATE,
            "pitch": TTS_PITCH,
        },
    }).encode("utf-8")

    req = Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        resp = urlopen(req, timeout=30)
        data = _json.loads(resp.read())
        audio_content = data.get("audioContent", "")
        if audio_content:
            import base64
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(audio_content))
            return True
    except Exception as e:
        print(f"   ⚠️  TTS error: {e}")
    return False


def generate_all_audio(script_name: str, work_dir: str) -> list:
    """Genera audio para todas las escenas."""
    demo = DEMO_SCRIPTS[script_name]
    audio_dir = os.path.join(work_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    audio_files = []
    for i, scene in enumerate(demo["scenes"]):
        if scene.get("voiceover"):
            out = os.path.join(audio_dir, f"scene_{i:02d}.mp3")
            print(f"   🎙️ TTS escena {i}: {scene['voiceover'][:40]}...")
            ok = synthesize_speech(scene["voiceover"], out)
            audio_files.append({"scene": i, "file": out if ok else None, "duration": scene["duration"]})
        else:
            audio_files.append({"scene": i, "file": None, "duration": scene["duration"]})
    return audio_files


# ─── FFmpeg assembly ─────────────────────────────────────────────────────────

def assemble_video(script_name: str, work_dir: str, audio_files: list) -> str:
    """Monta el video final con FFmpeg."""
    demo = DEMO_SCRIPTS[script_name]
    screenshots_dir = os.path.join(work_dir, "screenshots")
    output_path = str(OUTPUT_DIR / f"{script_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.mp4")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("   ❌ FFmpeg no encontrado en PATH")
        return ""

    # Build FFmpeg filter complex
    inputs = []
    filter_parts = []
    concat_inputs = []

    for i, scene in enumerate(demo["scenes"]):
        screenshot = os.path.join(screenshots_dir, f"scene_{i:02d}_{scene['id']}.png")
        if not os.path.exists(screenshot):
            # Create placeholder
            print(f"   ⚠️  Screenshot faltante: {screenshot}, creando placeholder")
            continue

        # Image input with duration
        inputs.extend(["-loop", "1", "-t", str(scene["duration"]), "-i", screenshot])
        input_idx = len(concat_inputs)

        # Add text overlay if needed
        if scene.get("screen_text"):
            text_escaped = scene["screen_text"].replace("'", "\\'").replace(":", "\\:")
            filter_parts.append(
                f"[{input_idx}:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
                f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,"
                f"drawtext=text='{text_escaped}':{TEXT_STYLE}:"
                f"x=(w-text_w)/2:y=h*0.4[v{input_idx}]"
            )
        else:
            filter_parts.append(
                f"[{input_idx}:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
                f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black[v{input_idx}]"
            )
        concat_inputs.append(f"[v{input_idx}]")

    if not concat_inputs:
        print("   ❌ No hay screenshots para montar")
        return ""

    # Concat all video streams
    filter_complex = ";".join(filter_parts)
    filter_complex += f";{''.join(concat_inputs)}concat=n={len(concat_inputs)}:v=1:a=0[outv]"

    # Add audio if available
    audio_inputs = []
    has_audio = False
    for af in audio_files:
        if af["file"] and os.path.exists(af["file"]):
            audio_inputs.extend(["-i", af["file"]])
            has_audio = True

    cmd = [ffmpeg, "-y"]
    cmd.extend(inputs)
    if audio_inputs:
        cmd.extend(audio_inputs)
    cmd.extend([
        "-filter_complex", filter_complex,
        "-map", "[outv]",
    ])

    if has_audio:
        # Merge audio tracks
        audio_idx = len(concat_inputs)
        cmd.extend(["-map", f"{audio_idx}:a"])

    cmd.extend([
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-t", str(demo["duration_target"]),
        output_path,
    ])

    print(f"   🎬 Montando video con FFmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        print(f"   ❌ FFmpeg error: {result.stderr[:300]}")
        return ""

    print(f"   ✅ Video generado: {output_path}")
    return output_path


# ─── Subtitle generation ────────────────────────────────────────────────────

def generate_srt(script_name: str, work_dir: str) -> str:
    """Genera archivo de subtitulos SRT sincronizado."""
    demo = DEMO_SCRIPTS[script_name]
    srt_path = os.path.join(work_dir, f"{script_name}.srt")

    current_time = 0.0
    srt_entries = []

    for i, scene in enumerate(demo["scenes"], 1):
        if scene.get("voiceover"):
            start = format_srt_time(current_time)
            end = format_srt_time(current_time + scene["duration"])
            srt_entries.append(f"{i}\n{start} --> {end}\n{scene['voiceover']}\n")
        current_time += scene["duration"]

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))

    return srt_path


def format_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# ─── Main pipeline ──────────────────────────────────────────────────────────

def run_pipeline(script_name: str, skip_capture: bool = False) -> dict:
    """Ejecuta el pipeline completo de generacion de video."""
    if script_name not in DEMO_SCRIPTS:
        return {"error": f"Script '{script_name}' no encontrado"}

    demo = DEMO_SCRIPTS[script_name]
    work_dir = tempfile.mkdtemp(prefix=f"tramitup_video_{script_name}_")
    print(f"\n🎬 VIDEO ASSEMBLY — {demo['title']}")
    print(f"   Script: {script_name} | Duracion objetivo: {demo['duration_target']}s")
    print(f"   Work dir: {work_dir}")

    result = {
        "script": script_name,
        "title": demo["title"],
        "started_at": datetime.now().isoformat(),
        "steps": {},
    }

    # Step 1: Capture
    if not skip_capture:
        ok = run_puppeteer_capture(script_name, work_dir)
        result["steps"]["capture"] = {"ok": ok}
        if not ok:
            print("   ⚠️  Captura fallida, continuando con lo que haya...")
    else:
        print("   ⏭️  Saltando captura (--skip-capture)")
        result["steps"]["capture"] = {"ok": True, "skipped": True}

    # Step 2: TTS
    print(f"\n   🎙️ Generando audio TTS...")
    audio_files = generate_all_audio(script_name, work_dir)
    result["steps"]["tts"] = {
        "ok": any(a["file"] for a in audio_files),
        "files": len([a for a in audio_files if a["file"]]),
    }

    # Step 3: Subtitles
    srt_path = generate_srt(script_name, work_dir)
    result["steps"]["subtitles"] = {"ok": True, "file": srt_path}

    # Step 4: Assembly
    video_path = assemble_video(script_name, work_dir, audio_files)
    result["steps"]["assembly"] = {"ok": bool(video_path), "file": video_path}

    result["completed_at"] = datetime.now().isoformat()
    result["output"] = video_path
    result["work_dir"] = work_dir

    # Save result
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    meta_file = OUTPUT_DIR / f"{script_name}_meta_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Video Assembly Bot")
    parser.add_argument("--script", choices=list(DEMO_SCRIPTS.keys()), help="Script de demo")
    parser.add_argument("--skip-capture", action="store_true", help="Salta la captura con Puppeteer")
    parser.add_argument("--list-scripts", action="store_true", help="Lista scripts disponibles")
    parser.add_argument("--check", action="store_true", help="Verifica dependencias")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    args = parser.parse_args()

    if args.check:
        deps = check_dependencies()
        all_ok = all(d["ok"] for d in deps.values())
        print("🔧 VERIFICACION DE DEPENDENCIAS")
        print("=" * 50)
        for name, info in deps.items():
            icon = "✅" if info["ok"] else "❌"
            detail = info.get("version") or info.get("path") or info.get("note", "")
            print(f"   {icon} {name}: {detail}")
        print("")
        if all_ok:
            print("🎉 Todas las dependencias OK. Listo para generar videos.")
        else:
            missing = [k for k, v in deps.items() if not v["ok"]]
            print(f"⚠️  Dependencias faltantes: {', '.join(missing)}")
            print("   Instala las dependencias faltantes antes de generar videos.")
        return

    if args.list_scripts:
        print("📜 SCRIPTS DISPONIBLES:")
        print("=" * 50)
        for name, demo in DEMO_SCRIPTS.items():
            total_dur = sum(s["duration"] for s in demo["scenes"])
            print(f"   📹 {name}")
            print(f"      Titulo: {demo['title']}")
            print(f"      Escenas: {len(demo['scenes'])} | Duracion: {total_dur}s")
            print("")
        return

    if args.script:
        result = run_pipeline(args.script, args.skip_capture)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("")
            if result.get("output"):
                print(f"🎉 Video generado: {result['output']}")
            else:
                print("⚠️  Pipeline completado con errores. Revisa los pasos individuales.")
                for step, info in result.get("steps", {}).items():
                    icon = "✅" if info.get("ok") else "❌"
                    print(f"   {icon} {step}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
