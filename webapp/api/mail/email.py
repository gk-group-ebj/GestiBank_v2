from flask import render_template, current_app
from webapp.main.email import send_email


def send_password_reset_email(p_user):
    token = p_user.get_reset_password_token()
    subject = "Gestibank : Re(Init) your password"
    sender = current_app.config['ADMINS_EMAIL']
    recipients = [p_user.email]
    text_body = render_template("auth/email/email_reset_password.txt", user=p_user, token=token)
    html_body = render_template("auth/email/email_reset_password.html", user=p_user, token=token)

    send_email(subject=subject, sender=sender, recipients=recipients, text_body=text_body, html_body=html_body)
