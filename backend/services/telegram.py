import aiohttp
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


async def send_lead_notification(lead: Lead) -> bool:
    if not settings.bot_token or not settings.chat_id:
        return False

    text = format_lead_message(lead)
    url = f"https://api.telegram.org/bot{settings.bot_token}/sendMessage"

    payload = {
        "chat_id": settings.chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                data = await response.json()
                return data.get("ok", False)
    except Exception as exc:
        print(f"Telegram send error: {exc}")
        return False
