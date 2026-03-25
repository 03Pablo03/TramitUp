"""
Base de datos SQLite para el sistema de marketing.
Almacena: contenido generado, métricas, tendencias, FAQs, A/B tests, logs.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

from marketing.core.config_loader import data_dir

DB_PATH = data_dir() / "marketing.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def db():
    """Context manager para transacciones."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Crea todas las tablas si no existen."""
    with db() as conn:
        conn.executescript("""
        -- Contenido generado
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_type TEXT NOT NULL,          -- tiktok_script, fb_post, carousel, thread, etc.
            platform TEXT NOT NULL,              -- tiktok, facebook, instagram, twitter, youtube
            category TEXT,                       -- multas, alquiler, laboral, etc.
            title TEXT NOT NULL,
            body TEXT,                           -- JSON con todo el contenido
            format TEXT,                         -- mito_vs_realidad, carrusel, etc.
            status TEXT DEFAULT 'draft',         -- draft, ready, published, archived
            published_at TEXT,
            file_paths TEXT,                     -- JSON array de archivos generados
            parent_id INTEGER,                   -- Para contenido repurposeado
            metadata TEXT,                       -- JSON extra
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (parent_id) REFERENCES content(id)
        );

        -- Tendencias detectadas
        CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,                -- google_trends, boe, news, social
            category TEXT,
            title TEXT NOT NULL,
            description TEXT,
            urgency TEXT DEFAULT 'media',        -- alta, media, baja
            viral_potential TEXT DEFAULT 'medio', -- alto, medio, bajo
            url TEXT,
            detected_at TEXT DEFAULT (datetime('now')),
            expires_at TEXT,
            status TEXT DEFAULT 'new',           -- new, used, expired, dismissed
            metadata TEXT
        );

        -- FAQs descubiertas
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            source TEXT,                         -- reddit, facebook, google_paa, foro
            search_volume TEXT DEFAULT 'medio',
            viral_potential TEXT DEFAULT 'medio',
            answer_summary TEXT,
            video_angle TEXT,                    -- JSON con sugerencia de vídeo
            times_seen INTEGER DEFAULT 1,
            last_seen_at TEXT DEFAULT (datetime('now')),
            created_at TEXT DEFAULT (datetime('now')),
            UNIQUE(category, question)
        );

        -- Métricas por publicación
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER,
            platform TEXT NOT NULL,
            date TEXT NOT NULL,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            saves INTEGER DEFAULT 0,
            link_clicks INTEGER DEFAULT 0,
            profile_visits INTEGER DEFAULT 0,
            registrations INTEGER DEFAULT 0,
            conversions INTEGER DEFAULT 0,
            engagement_rate REAL DEFAULT 0.0,
            metadata TEXT,
            recorded_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (content_id) REFERENCES content(id)
        );

        -- Tests A/B
        CREATE TABLE IF NOT EXISTS ab_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER,
            test_type TEXT NOT NULL,             -- title, hook, caption, hashtags, thumbnail
            variant_a TEXT NOT NULL,             -- JSON
            variant_b TEXT NOT NULL,             -- JSON
            variant_c TEXT,
            variant_d TEXT,
            winner TEXT,                         -- a, b, c, d
            results TEXT,                        -- JSON con métricas comparativas
            status TEXT DEFAULT 'pending',       -- pending, running, completed
            created_at TEXT DEFAULT (datetime('now')),
            completed_at TEXT,
            FOREIGN KEY (content_id) REFERENCES content(id)
        );

        -- Hashtags intelligence
        CREATE TABLE IF NOT EXISTS hashtags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            hashtag TEXT NOT NULL,
            category TEXT,
            volume_tier TEXT DEFAULT 'medio',    -- alto, medio, nicho
            is_blacklisted INTEGER DEFAULT 0,
            last_trending_at TEXT,
            times_used INTEGER DEFAULT 0,
            avg_engagement REAL DEFAULT 0.0,
            created_at TEXT DEFAULT (datetime('now')),
            UNIQUE(platform, hashtag)
        );

        -- Calendario editorial
        CREATE TABLE IF NOT EXISTS calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER,
            platform TEXT NOT NULL,
            scheduled_date TEXT NOT NULL,
            scheduled_time TEXT,
            status TEXT DEFAULT 'scheduled',     -- scheduled, published, skipped, failed
            publish_result TEXT,                 -- JSON con resultado de publicación
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (content_id) REFERENCES content(id)
        );

        -- Log de operaciones
        CREATE TABLE IF NOT EXISTS operations_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT NOT NULL,             -- generate, publish, scrape, analyze, etc.
            module TEXT,                         -- trend_detector, video_assembly, etc.
            status TEXT DEFAULT 'success',       -- success, error, warning
            details TEXT,
            duration_ms INTEGER,
            created_at TEXT DEFAULT (datetime('now'))
        );

        -- Audience insights
        CREATE TABLE IF NOT EXISTS audience_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            pain_point TEXT NOT NULL,
            language_used TEXT,                  -- Frases reales que usa la gente
            source TEXT,
            frequency TEXT DEFAULT 'media',
            sentiment TEXT DEFAULT 'neutral',
            created_at TEXT DEFAULT (datetime('now')),
            UNIQUE(category, pain_point)
        );

        -- Indexes
        CREATE INDEX IF NOT EXISTS idx_content_platform ON content(platform);
        CREATE INDEX IF NOT EXISTS idx_content_category ON content(category);
        CREATE INDEX IF NOT EXISTS idx_content_status ON content(status);
        CREATE INDEX IF NOT EXISTS idx_trends_status ON trends(status);
        CREATE INDEX IF NOT EXISTS idx_metrics_content ON metrics(content_id);
        CREATE INDEX IF NOT EXISTS idx_calendar_date ON calendar(scheduled_date);
        CREATE INDEX IF NOT EXISTS idx_faqs_category ON faqs(category);
        """)


# ─── Helpers CRUD ────────────────────────────────────────────────────────────

def insert_content(content_type: str, platform: str, title: str, body: dict,
                   category: str = None, format: str = None, parent_id: int = None,
                   file_paths: list = None, metadata: dict = None) -> int:
    with db() as conn:
        cur = conn.execute("""
            INSERT INTO content (content_type, platform, category, title, body, format,
                                 parent_id, file_paths, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (content_type, platform, category, title, json.dumps(body, ensure_ascii=False),
              format, parent_id, json.dumps(file_paths or []), json.dumps(metadata or {})))
        return cur.lastrowid


def insert_trend(source: str, title: str, description: str = None,
                 category: str = None, urgency: str = "media",
                 viral_potential: str = "medio", url: str = None,
                 expires_at: str = None, metadata: dict = None) -> int:
    with db() as conn:
        cur = conn.execute("""
            INSERT INTO trends (source, category, title, description, urgency,
                                viral_potential, url, expires_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (source, category, title, description, urgency, viral_potential,
              url, expires_at, json.dumps(metadata or {})))
        return cur.lastrowid


def insert_faq(category: str, question: str, source: str = None,
               search_volume: str = "medio", viral_potential: str = "medio",
               answer_summary: str = None, video_angle: dict = None) -> int:
    with db() as conn:
        cur = conn.execute("""
            INSERT INTO faqs (category, question, source, search_volume,
                              viral_potential, answer_summary, video_angle)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(category, question) DO UPDATE SET
                times_seen = times_seen + 1,
                last_seen_at = datetime('now')
        """, (category, question, source, search_volume, viral_potential,
              answer_summary, json.dumps(video_angle or {})))
        return cur.lastrowid


def insert_metric(content_id: int, platform: str, date: str, **kwargs) -> int:
    fields = ["views", "likes", "comments", "shares", "saves",
              "link_clicks", "profile_visits", "registrations", "conversions"]
    values = {f: kwargs.get(f, 0) for f in fields}
    total_engagement = values["likes"] + values["comments"] + values["shares"] + values["saves"]
    values["engagement_rate"] = (total_engagement / values["views"] * 100) if values["views"] > 0 else 0

    with db() as conn:
        cur = conn.execute(f"""
            INSERT INTO metrics (content_id, platform, date,
                {', '.join(fields)}, engagement_rate)
            VALUES (?, ?, ?, {', '.join(['?'] * len(fields))}, ?)
        """, (content_id, platform, date, *[values[f] for f in fields], values["engagement_rate"]))
        return cur.lastrowid


def log_operation(operation: str, module: str, status: str = "success",
                  details: str = None, duration_ms: int = None):
    with db() as conn:
        conn.execute("""
            INSERT INTO operations_log (operation, module, status, details, duration_ms)
            VALUES (?, ?, ?, ?, ?)
        """, (operation, module, status, details, duration_ms))


def query(sql: str, params: tuple = ()) -> list[dict]:
    """Ejecuta un SELECT y devuelve lista de dicts."""
    with db() as conn:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]


def query_one(sql: str, params: tuple = ()) -> dict | None:
    rows = query(sql, params)
    return rows[0] if rows else None
