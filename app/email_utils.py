import smtplib
from email.message import EmailMessage

from flask import current_app


def send_report_email(recipient, subject, body, attachment_path=None):
    server = current_app.config["MAIL_SERVER"]
    username = current_app.config["MAIL_USERNAME"]
    password = current_app.config["MAIL_PASSWORD"]
    sender = current_app.config["MAIL_SENDER"] or username
    if not all([server, username, password, sender]):
        return False, "Email is not configured. Set MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD, and MAIL_SENDER."

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content(body)

    if attachment_path:
        with open(attachment_path, "rb") as file:
            message.add_attachment(
                file.read(),
                maintype="application",
                subtype="pdf",
                filename="health_report.pdf",
            )

    with smtplib.SMTP(server, current_app.config["MAIL_PORT"]) as smtp:
        if current_app.config["MAIL_USE_TLS"]:
            smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(message)

    return True, "Email sent successfully."
