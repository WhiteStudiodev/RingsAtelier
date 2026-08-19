from pathlib import Path

import aiohttp
from aiohttp_socks import ProxyConnector
from loguru import logger
from sqlalchemy.orm import Session

from config import settings
from database import Lead


METHOD_LABELS = {
    "tg": "Telegram",
    "max": "Max",
    "vk": "ВКонтакте",
    "phone": "Телефон",
}


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def format_lead_message(lead: Lead) -> str:
    lines = [
        "<b>Новая заявка с сайта Rings Atelier</b>",
        "",
        f"<b>Имя:</b> {escape_html(lead.name)}",
        f"<b>Способ связи:</b> {METHOD_LABELS.get(lead.method, lead.method)}",
        f"<b>Контакт:</b> {escape_html(lead.contact)}",
        f"<b>Сообщение:</b> {escape_html(lead.message or '—')}",
    ]
    return "\n".join(lines)


async def send_telegram_message(chat_id: str, text: str) -> bool:
    """Send an HTML message to a Telegram chat."""
    if not settings.bot_token or not chat_id:
        logger.warning("Telegram bot_token or chat_id is not configured")
        return False

    base_url = settings.telegram_api_url.rstrip("/")
    url = f"{base_url}/bot{settings.bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    logger.debug("Sending Telegram message to {}", base_url)

    try:
        connector = None
        if settings.proxy_url:
            logger.debug("Using proxy: {}", settings.proxy_url)
            connector = ProxyConnector.from_url(settings.proxy_url)

        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(
                url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                data = await response.json()
                if not data.get("ok", False):
                    logger.error("Telegram API returned error: {}", data)
                    return False
                logger.info("Telegram message sent successfully")
                return True
    except Exception:
        logger.exception("Telegram send error")
        return False


async def send_telegram_document(chat_id: str, file_path: Path, caption: str) -> bool:
    """Send a document file to a Telegram chat."""
    if not settings.bot_token or not chat_id:
        logger.warning("Telegram bot_token or chat_id is not configured")
        return False

    if not file_path or not file_path.exists():
        logger.warning("Document not found: {}", file_path)
        return False

    base_url = settings.telegram_api_url.rstrip("/")
    url = f"{base_url}/bot{settings.bot_token}/sendDocument"

    logger.debug("Sending Telegram document to {}", base_url)

    try:
        connector = None
        if settings.proxy_url:
            logger.debug("Using proxy: {}", settings.proxy_url)
            connector = ProxyConnector.from_url(settings.proxy_url)

        data = aiohttp.FormData()
        data.add_field("chat_id", chat_id)
        data.add_field("caption", caption)
        data.add_field("parse_mode", "HTML")
        with open(file_path, "rb") as f:
            data.add_field("document", f, filename=file_path.name)

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(
                    url,
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=120),
                ) as response:
                    resp_data = await response.json()
                    if not resp_data.get("ok", False):
                        logger.error("Telegram API returned error: {}", resp_data)
                        return False
                    logger.info("Telegram document sent successfully")
                    return True
    except Exception:
        logger.exception("Telegram document send error")
        return False


async def send_lead_notification(lead: Lead) -> bool:
    if not settings.bot_token or not settings.chat_id:
        logger.warning("Telegram bot_token or chat_id is not configured")
        return False

    text = format_lead_message(lead)
    return await send_telegram_message(settings.chat_id, text)
