from email.message import EmailMessage

import aiosmtplib
from loguru import logger

from config import settings
from database import Lead


METHOD_LABELS = {
    "tg": "Telegram",
    "max": "Max",
    "vk": "ВКонтакте",
    "phone": "Телефон",
}


def format_lead_email_text(lead: Lead) -> str:
    lines = [
        "Новая заявка с сайта Rings Atelier",
        "",
        f"Имя: {lead.name}",
        f"Способ связи: {METHOD_LABELS.get(lead.method, lead.method)}",
        f"Контакт: {lead.contact}",
        f"Сообщение: {lead.message or '—'}",
    ]
    return "\n".join(lines)


def format_lead_email_html(lead: Lead) -> str:
    return f"""\
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Новая заявка с сайта Rings Atelier</title>
</head>
<body>
    <h2>Новая заявка с сайта Rings Atelier</h2>
    <table>
        <tr><td><b>Имя:</b></td><td>{lead.name}</td></tr>
        <tr><td><b>Способ связи:</b></td><td>{METHOD_LABELS.get(lead.method, lead.method)}</td></tr>
        <tr><td><b>Контакт:</b></td><td>{lead.contact}</td></tr>
        <tr><td><b>Сообщение:</b></td><td>{lead.message or '—'}</td></tr>
    </table>
</body>
</html>
"""


async def send_lead_email(lead: Lead) -> bool:
    if not settings.smtp_user or not settings.smtp_password:
        logger.warning("SMTP user or password is not configured")
        return False

    from_addr = settings.smtp_from or settings.smtp_user
    to_addr = settings.smtp_to or settings.smtp_user

    if not to_addr:
        logger.warning("SMTP recipient is not configured")
        return False

    message = EmailMessage()
    message["From"] = from_addr
    message["To"] = to_addr
    message["Subject"] = "Новая заявка с сайта Rings Atelier"
    message.set_content(format_lead_email_text(lead))
    message.add_alternative(format_lead_email_html(lead), subtype="html")

    try:
        logger.debug(
            "Sending email notification via {}:{}", settings.smtp_host, settings.smtp_port
        )
        await aiosmtplib.send(
            message,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_password,
            use_tls=True,
        )
        logger.info("Email notification sent successfully")
        return True
    except Exception:
        logger.exception("Email send error")
        return False
