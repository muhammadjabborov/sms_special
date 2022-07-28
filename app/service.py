from django.core.mail import EmailMessage
import random
import threading

from app.models import User


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(email):
        message_data = {'message': 'Pleas check your email'}
        user = User.objects.get(email=email)
        email_subject = 'Hi ' + user.email + ' Please take your activation code'
        email_body = str(random.randint(1000, 10000))
        user.activation_code = email_body
        user.save()
        data = {
            'email_subject': email_subject,
            'email_body': email_body,
            'to_email': user.email
        }
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()
        return message_data


def send_email(activation_code: str, email: str,username:str):
    user = User.objects.get(email=email)

    message_data = {
        'message': 'Successfull'
    }
    error_message_data = {
        'message': 'The activation code is not the same'
    }
    if user.activation_code == activation_code:
        user.is_verified = True
        user.username = username
        user.save()
        return message_data
    return error_message_data
