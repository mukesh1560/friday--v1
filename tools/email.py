"""
tools/email.py — Email sending for Friday
Uses Gmail SMTP with an App Password (2FA must be enabled on Gmail).

Setup:
  1. Go to myaccount.google.com → Security → App passwords
  2. Generate a password for "Mail"
  3. Put it in config.py as EMAIL_APP_PASSWORD
"""

import smtplib
from email.mime.text      import MIMEText
from email.mime.multipart import MIMEMultipart
import config


def send_email(to: str, subject: str, body: str) -> str:
    """Send an email via Gmail SMTP."""

    if not config.EMAIL_ADDRESS or config.EMAIL_ADDRESS == "YOUR_GMAIL@gmail.com":
        return "❌ Set EMAIL_ADDRESS in config.py first."
    if not config.EMAIL_APP_PASSWORD or config.EMAIL_APP_PASSWORD == "YOUR_APP_PASSWORD":
        return "❌ Set EMAIL_APP_PASSWORD in config.py first."
    if not to:
        return "❌ No recipient email address provided."
    if not subject:
        subject = "(No Subject)"
    if not body:
        body = ""

    try:
        msg            = MIMEMultipart()
        msg["From"]    = config.EMAIL_ADDRESS
        msg["To"]      = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            server.login(config.EMAIL_ADDRESS, config.EMAIL_APP_PASSWORD)
            server.sendmail(config.EMAIL_ADDRESS, to, msg.as_string())

        return f"✅ Email sent to {to} — Subject: '{subject}'"

    except smtplib.SMTPAuthenticationError:
        return (
            "❌ Gmail authentication failed.\n"
            "Make sure you're using an App Password (not your regular password).\n"
            "Guide: myaccount.google.com → Security → App passwords"
        )
    except smtplib.SMTPRecipientsRefused:
        return f"❌ Recipient address '{to}' was refused."
    except TimeoutError:
        return "❌ Connection to Gmail timed out."
    except Exception as e:
        return f"❌ Email failed: {e}"
