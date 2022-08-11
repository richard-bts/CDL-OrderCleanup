from ordercleanup import mail 
from flask_mail import Message
from datetime import datetime
from ordercleanup.config import config

import os

def send_error_email():
    file_name = 'error.log'
    today = datetime.today()
    today = today.strftime("%m/%d/%Y, %H:%M:%S")
    subject = 'Order Cleanup - ' + today
    msg = Message(
                    sender=str(config.MAIL_DEFAULT_SENDER),
                    subject=subject,
                    recipients = config.SUPPORT
                )
    msg.body = 'There was a server error when trying to perform the order cleanup report. Please check app log to see error'
    if file_name in os.listdir():
        file = open(file_name, 'rb')
        msg.attach(file_name, 'text/plain', file.read())
    mail.send(msg)