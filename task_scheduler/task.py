from celery import shared_task
from comman_functions import views

@shared_task
def otp_request_twillo_task(mobileNo, msg):
    views.otp_request_twillo(mobileNo, msg)
    return
