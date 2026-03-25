# TramitUp Marketing Automation

Sistema de 12 bots especializados para la estrategia de marketing orgánico de TramitUp en TikTok, Facebook e Instagram.

## Requisitos

```bash
# Base (todos los bots)
pip install anthropic requests beautifulsoup4

# Video Assembly (bot 12)
npm install puppeteer
# + FFmpeg en PATH
# + GOOGLE_API_KEY env var (Google Cloud TTS)
```

## Variables de entorno

```bash
export ANTHROPIC_API_KEY="sk-ant-..."     # Bots 7-11 (IA)
export GOOGLE_API_KEY="AIza..."           # Bot 12 (TTS)
```

## Quick Start

```bash
# Generar TODO el contenido del mes (bots sin IA)
python -m marketing.run all

# Ver ayuda completa
python -m marketing.run --help
```

## Bots disponibles

### Contenido (sin API externa)

| # | Bot | Comando | Descripción |
|---|-----|---------|-------------|
| 1 | **TikTok Script Writer** | `tiktok` | Guiones completos con gancho/desarrollo/CTA, 12 formatos |
| 2 | **Facebook Post Generator** | `facebook` | Posts para página FB, 8 formatos (carrusel, valor, caso real...) |
| 3 | **Community Response** | `community` | Respuestas para grupos de Facebook, 22 plantillas por tema |
| 4 | **Content Calendar** | `calendar` | Calendario editorial semanal/mensual (TikTok + FB + comunidad) |
| 5 | **Caption & Hashtag Optimizer** | `caption` | Captions optimizados por plataforma + testing A/B |
| 6 | **KPI Tracker** | `kpi` | Tracking de métricas, comparación con objetivos, reportes |

### IA (requieren `ANTHROPIC_API_KEY`)

| # | Bot | Comando | Descripción |
|---|-----|---------|-------------|
| 7 | **Trend Detector** | `trends` | Detecta tendencias legales en España, sugiere ideas de vídeo |
| 8 | **Comment Reply** | `reply` | Respuestas naturales a comentarios, detecta oportunidades de vídeo |
| 9 | **Content Repurposer** | `repurpose` | Transforma un guion TikTok en 5 plataformas (FB, carrusel, X, YT...) |
| 10 | **A/B Title Tester** | `titles` | 4 variantes de título/gancho con análisis de patrón viral |
| 11 | **FAQ Scraper** | `faqs` | Preguntas frecuentes reales categorizadas con ángulo para vídeo |

### Video (requiere Node.js + Puppeteer + FFmpeg + `GOOGLE_API_KEY`)

| # | Bot | Comando | Descripción |
|---|-----|---------|-------------|
| 12 | **Video Assembly** | `video` | Pipeline completo: captura app → TTS → FFmpeg → vídeo vertical |

## Comandos detallados

### Bot 1: TikTok Script Writer
```bash
python -m marketing.run tiktok --all                          # 12 guiones del mes
python -m marketing.run tiktok --topic multas                 # Guion individual
python -m marketing.run tiktok --topic alquiler --format top_3_listicle
python -m marketing.run tiktok --topic multas --json          # Output JSON
```

### Bot 2: Facebook Post Generator
```bash
python -m marketing.run facebook --all                        # 12 posts del mes
python -m marketing.run facebook --topic laboral              # Post individual
python -m marketing.run facebook --topic consumo --format caso_real
```

### Bot 3: Community Response
```bash
python -m marketing.run community --templates                 # Todas las plantillas
python -m marketing.run community --topic alquiler            # Respuesta por tema
python -m marketing.run community --topic laboral --question "Me han despedido"
```

### Bot 4: Content Calendar
```bash
python -m marketing.run calendar --month 1                    # Calendario completo
python -m marketing.run calendar --week 2                     # Semana específica
```

### Bot 5: Caption & Hashtag Optimizer
```bash
python -m marketing.run caption --platform tiktok --topic multas
python -m marketing.run caption --platform facebook --topic alquiler
python -m marketing.run caption --platform tiktok --topic laboral --ab   # Test A/B
```

### Bot 6: KPI Tracker
```bash
python -m marketing.run kpi --init                            # Inicializar
python -m marketing.run kpi --status                          # Estado actual
python -m marketing.run kpi --log --platform tiktok --metric views --value 2500
python -m marketing.run kpi --report month1                   # Reporte mensual
```

### Bot 7: Trend Detector
```bash
python -m marketing.run trends                                # Tendencias generales
python -m marketing.run trends --category laboral             # Por categoría
python -m marketing.run trends --category alquiler --json
```

### Bot 8: Comment Reply
```bash
python -m marketing.run reply --comment "¿Me pueden echar si no pago un mes?"
python -m marketing.run reply --comment "Esto es mentira" --platform tiktok
python -m marketing.run reply --file comments.json            # Batch processing
```

Formato del archivo JSON para batch:
```json
[
  {"text": "¿Pueden subirme el alquiler?", "context": "vídeo sobre derechos inquilinos"},
  {"text": "Esto me pasó a mí", "context": "vídeo sobre multas"},
  "comentario simple sin contexto"
]
```

### Bot 9: Content Repurposer
```bash
python -m marketing.run repurpose --topic multas              # Genera TikTok + repurposea
python -m marketing.run repurpose --file script.json          # Desde archivo
python -m marketing.run repurpose --all-month                 # Todo el mes
```

Output por pieza:
- Post largo Facebook (300-500 palabras)
- Carrusel 5-7 slides
- Story/Reel caption (125 chars)
- Twitter/X thread (4-6 tweets)
- YouTube Shorts descripción

### Bot 10: A/B Title Tester
```bash
python -m marketing.run titles --topic multas
python -m marketing.run titles --topic laboral --angle "despido sin preaviso"
python -m marketing.run titles --topic alquiler --json
```

Genera 4 variantes usando patrones diferentes:
- Pregunta / curiosidad
- Negación / prohibición
- Números / datos
- Consecuencias / revelación

### Bot 11: FAQ Scraper
```bash
python -m marketing.run faqs --category alquiler              # Una categoría
python -m marketing.run faqs --category laboral --limit 10    # Más preguntas
python -m marketing.run faqs --all                            # Todas las categorías
```

Categorías: `alquiler`, `laboral`, `multas`, `consumo`, `herencias`, `vuelos`, `tramites`, `autonomos`, `familia`

### Bot 12: Video Assembly
```bash
python -m marketing.run video --check                         # Verificar dependencias
python -m marketing.run video --list-scripts                  # Ver scripts disponibles
python -m marketing.run video --script demo_basico            # Generar vídeo
python -m marketing.run video --script demo_basico --skip-capture  # Solo montar
```

Scripts de demo disponibles:
- `demo_basico` — Demo general de la app (45s)
- `demo_contrato` — Análisis de contrato con IA (50s)
- `demo_calculadora` — Calculadora de indemnización (40s)

## Estructura del proyecto

```
marketing/
├── __init__.py
├── config.py                      # Configuración central (marca, voz, CTAs, hashtags, KPIs)
├── llm.py                         # Helper para Claude API (anthropic SDK)
├── run.py                         # CLI principal — orquesta todos los bots
├── README.md
├── bots/
│   ├── __init__.py
│   ├── tiktok_scriptwriter.py     # Bot 1:  TikTok Script Writer
│   ├── facebook_posts.py          # Bot 2:  Facebook Post Generator
│   ├── community_bot.py           # Bot 3:  Community Response
│   ├── calendar_bot.py            # Bot 4:  Content Calendar
│   ├── caption_optimizer.py       # Bot 5:  Caption & Hashtag Optimizer
│   ├── kpi_tracker.py             # Bot 6:  KPI Tracker
│   ├── trend_detector.py          # Bot 7:  Trend Detector
│   ├── comment_reply.py           # Bot 8:  Comment Reply
│   ├── content_repurposer.py      # Bot 9:  Content Repurposer
│   ├── ab_title_tester.py         # Bot 10: A/B Title Tester
│   ├── faq_scraper.py             # Bot 11: FAQ Scraper
│   └── video_assembly.py          # Bot 12: Video Assembly
└── output/                        # Contenido generado (gitignored)
    ├── tiktok_month_YYYYMM.txt
    ├── facebook_month_YYYYMM.txt
    ├── community_templates_YYYYMMDD.txt
    ├── calendar_YYYYMM.txt
    ├── kpi_data.json
    ├── trends_*.txt
    ├── replies_*.txt
    ├── repurposed_*.txt
    ├── titles_*.txt
    ├── faqs_*.txt
    └── videos/
        └── demo_basico_*.mp4

```

## Modelo de IA

Los bots 7-11 usan **Claude claude-sonnet-4-20250514** (`claude-sonnet-4-20250514`) via la API de Anthropic. La configuración está centralizada en `marketing/llm.py`.

## Temas soportados

`multas` · `alquiler` · `laboral` · `consumo` · `herencias` · `vuelos` · `tramites`

Cada tema tiene hooks, datos legales reales y hashtags configurados en `config.py`.
