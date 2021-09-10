from django.core.mail import EmailMessage

# Util class to send verification email
class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(subject=data['subject'],body=data['email_body'],to=[data['email_to']])
        email.send()