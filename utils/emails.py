import logging

import requests

from flask import current_app


logger = logging.getLogger(__name__)

def send_email(to, subject, html):
    """Send a transactional email via Resend without blocking the caller."""
    api_key = current_app.config.get("RESEND_API_KEY")
    from_email = current_app.config.get("RESEND_FROM_EMAIL")
    if not api_key or not from_email:
        logger.warning("Resend is not fully configured; skipped email to %s", to)
        return False

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": from_email,
                "to": [to],
                "subject": subject,
                "html": html,
            },
            timeout=15,
        )

        response.raise_for_status()
        return True
    except requests.HTTPError as error:
        response = error.response
        logger.error(
            "Resend rejected email to %s: %s",
            to,
            response.text if response is not None else str(error),
        )
        return False
    except requests.RequestException:
        logger.exception("Resend email delivery failed for %s", to)
        return False



























