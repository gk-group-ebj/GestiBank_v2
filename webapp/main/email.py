from threading import Thread

from flask import current_app

from webapp.extensions import mail, db
#from webapp.bdd.models import User
from flask_mail import Message


def send_async_email(p_app, msg):
    with p_app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body=None, html_body=None):
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=recipients
    )

    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


if __name__ == "__main__":
    test_msg = Message('sujet',
                       sender='moez@gmail.com',
                       recipients=['melou_python_email@maildrop.cc'])
    test_msg.body = "corps du message"
    test_msg.html = "<h1>HTML Body</h1>"

    with current_app.app_context():
        mail.send(test_msg)
