import asyncio
import shutil
from datetime import datetime, timedelta, time
from pathlib import Path

from loguru import logger

from config import settings
from services.telegram import send_telegram_document, send_telegram_message


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


async def send_backup_notification(backup_path: Path | None, success: bool) -> None:
    """Send the daily backup report to the backup Telegram chat."""
    if not settings.bot_token or not settings.backup_chat_id:
        logger.warning(
            "Backup notification skipped: BOT_TOKEN or BACKUP_CHAT_ID is not configured"
        )
        return

    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    if success and backup_path:
        size_bytes = backup_path.stat().st_size
        size_text = _humanize_size(size_bytes)
        caption = (
            f"<b>✅ Бэкап БД Rings Atelier</b>\n\n"
            f"Файл: <code>{backup_path.name}</code>\n"
            f"Размер: {size_text}\n"
            f"Время: {now_str} UTC"
        )
        await send_telegram_document(settings.backup_chat_id, backup_path, caption)
    else:
        text = (
            f"<b>❌ Бэкап БД Rings Atelier не удался</b>\n\n"
            f"Время: {now_str} UTC\n"
            f"Проверьте логи сервера."
        )
        await send_telegram_message(settings.backup_chat_id, text)


def _humanize_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    return f"{size_bytes / (1024 * 1024):.2f} MB"


async def run_backup() -> None:
    backup_path = await create_backup()
    await send_backup_notification(backup_path, backup_path is not None)


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
    """Background task: run DB backup once a day at the configured UTC time."""
    while True:
        try:
            target_time = _parse_time(settings.backup_time_utc)
            wait = _seconds_until_next_run(target_time)
            logger.info(
                "Next DB backup scheduled at {} UTC (in {:.0f}s)",
                target_time,
                wait,
            )
            await asyncio.sleep(wait)
            await run_backup()
            # Sleep a minute to avoid running twice within the same scheduled minute.
            await asyncio.sleep(60)
        except Exception:
            logger.exception("Backup scheduler error")
            await asyncio.sleep(3600)
