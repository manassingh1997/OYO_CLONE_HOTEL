import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import Hotel

def generateRandomToken():
    return str(uuid.uuid4())

def sendEmailToken(email,token,r):
    subject = "Verify Your Email Address"
    message = f"""Hi Please verify your email account by clicking this link http://127.0.0.1:8000/accounts/verify-account/{r}{token}
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently = False,
    )


def sendOTPtoEmail(email,otp):
    subject = "OTP for Account Login"
    message = f"""Hi, use this OPT to login {otp}
    """
    html_message = f"""<p>Hi, use this OTP to login: <b>{otp}</b></p>"""
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently = False,
        html_message=html_message # HTML Message
    )

def generateSlug(hotel_name):
    slug = slugify(hotel_name) + "-" + str(uuid.uuid4()).split('-')[0]
    if Hotel.objects.filter(hotel_slug = slug).exists():
        return generateSlug(hotel_name)
    return slug