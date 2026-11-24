import asyncio
import shutil
from datetime import datetime, timedelta, time, timezone
from pathlib import Path
from time import monotonic

import aiohttp
from loguru import logger
from sqlalchemy import func

from config import settings
from database import Lead, SessionLocal
from services.telegram import send_telegram_message

MSK = timezone(timedelta(hours=3))


def get_db_file_path() -> Path | None:
    """Resolve the SQLite database file path from the database URL."""
    if not settings.database_url.startswith("sqlite:///"):
        logger.warning("Automatic backup is only supported for SQLite databases")
        return None

    # sqlite:///./leads.db   -> ./leads.db
    # sqlite:////abs/path/db -> /abs/path/db
    db_path_str = settings.database_url.removeprefix("sqlite:///")
    return Path(db_path_str).resolve()


def cleanup_old_backups(backup_dir: Path, retention_days: int) -> None:
    """Delete backup files older than retention_days."""
    cutoff = datetime.utcnow() - timedelta(days=retention_days)
    for path in backup_dir.glob("leads_*.db"):
        try:
            mtime = datetime.utcfromtimestamp(path.stat().st_mtime)
            if mtime < cutoff:
                path.unlink()
                logger.info("Deleted old DB backup: {}", path)
        except Exception:
            logger.exception("Failed to delete old backup: {}", path)


async def create_backup() -> Path | None:
    """Copy the SQLite DB to a timestamped backup file."""
    db_path = get_db_file_path()
    if not db_path:
        return None

    if not db_path.exists():
        logger.error("Database file not found: {}", db_path)
        return None

    backup_dir = Path(settings.backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = backup_dir / f"leads_{timestamp}.db"

    try:
        shutil.copy2(db_path, backup_path)
        # Ensure the backup mtime reflects the backup time, not the source DB age.
        backup_path.touch()
        cleanup_old_backups(backup_dir, settings.backup_retention_days)
        logger.info("DB backup created: {}", backup_path)
        return backup_path
    except Exception:
        logger.exception("DB backup failed")
        return None


async def check_site() -> tuple[bool, str]:
    """Check that the public site responds; returns (ok, human-readable detail)."""
    try:
        start = monotonic()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                settings.site_check_url,
                timeout=aiohttp.ClientTimeout(total=10),
                allow_redirects=True,
            ) as response:
                elapsed = monotonic() - start
                detail = f"HTTP {response.status}, {elapsed:.1f} с"
                return response.status == 200, detail
    except Exception as exc:
        logger.warning("Site check failed: {}", exc)
        return False, type(exc).__name__


def get_leads_stats() -> tuple[int, int]:
    """Return (leads in the last 24h, total leads)."""
    since = datetime.utcnow() - timedelta(hours=24)
    with SessionLocal() as db:
        total = db.query(func.count(Lead.id)).scalar() or 0
        fresh = (
            db.query(func.count(Lead.id))
            .filter(Lead.created_at >= since)
            .scalar()
            or 0
        )
    return fresh, total


async def send_daily_report(
    backup_path: Path | None, site_ok: bool, site_detail: str
) -> None:
    """Send the daily status report to the backup Telegram chat."""
    if not settings.bot_token or not settings.backup_chat_id:
        logger.warning(
            "Daily report skipped: BOT_TOKEN or BACKUP_CHAT_ID is not configured"
        )
        return

    backup_ok = backup_path is not None
    now_str = datetime.now(MSK).strftime("%d.%m.%Y %H:%M МСК")

    header = (
        "✅ Всё хорошо — сайт работает в штатном режиме"
        if site_ok and backup_ok
        else "⚠️ Требует внимания"
    )
    lines = [f"<b>{header}</b>", ""]

    if site_ok:
        lines.append(f"🌐 Сайт: доступен ({site_detail})")
    else:
        lines.append(f"🌐 Сайт: НЕ ОТВЕЧАЕТ ({site_detail})")

    if backup_ok:
        size_text = _humanize_size(backup_path.stat().st_size)
        lines.append(f"🗂 Бэкап БД: создан ({size_text})")
    else:
        lines.append("🗂 Бэкап БД: НЕ СОЗДАН — проверьте логи сервера")

    try:
        fresh, total = get_leads_stats()
        lines.append(f"💬 Заявки: +{fresh} за сутки, всего {total}")
    except Exception:
        logger.exception("Failed to count leads")
        lines.append("💬 Заявки: ошибка подсчёта")

    lines.append(f"🕒 {now_str}")

    await send_telegram_message(settings.backup_chat_id, "\n".join(lines))


def _humanize_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    return f"{size_bytes / (1024 * 1024):.2f} MB"


async def run_daily_report() -> None:
    backup_path = await create_backup()
    site_ok, site_detail = await check_site()
    await send_daily_report(backup_path, site_ok, site_detail)


def _parse_time(time_str: str) -> time:
    hour, minute = map(int, time_str.split(":"))
    return time(hour, minute)


def _seconds_until_next_run(target_time: time) -> float:
    now = datetime.utcnow()
    target = datetime.combine(now.date(), target_time)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds()


async def backup_scheduler() -> None:
    """Background task: daily DB backup + site status report at the configured UTC time."""
    while True:
        try:
            target_time = _parse_time(settings.backup_time_utc)
            wait = _seconds_until_next_run(target_time)
            logger.info(
                "Next daily report scheduled at {} UTC (in {:.0f}s)",
                target_time,
                wait,
            )
            await asyncio.sleep(wait)
            await run_daily_report()
            # Sleep a minute to avoid running twice within the same scheduled minute.
            await asyncio.sleep(60)
        except Exception:
            logger.exception("Backup scheduler error")
            await asyncio.sleep(3600)
