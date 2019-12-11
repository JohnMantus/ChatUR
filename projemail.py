from threading import Thread
from flask import current_app, render_template
from flask_mail import Mail, Message
import os
# from . import mail




# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)


# def send_email(to, subject, template, **kwargs):
#     app = current_app._get_current_object()
#     msg = Message(subject,sender=app.config.get("MAIL_USERNAME"), recipients=[to], body = "hello")
#     ##msg = Message(subject, sender="1275471354@qq.com", recipients=[to])
#     # msg.body = render_template(template + '.txt', **kwargs)
#     # msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr


# app.config.update(mail_settings)
mail = Mail()





def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    with app.app_context():
        msg = Message(subject,sender=app.config.get("MAIL_USERNAME"), recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)
