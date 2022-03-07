from django.contrib.auth.models import User
from django.dispatch import receiver, Signal
from django.db.models.signals import pre_init, pre_save, pre_delete, post_init, post_save, post_delete
from .models import Profile
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


user_profile_data = Signal(providing_args=['request', 'user'])
@receiver(user_profile_data)
def save_profile(sender, request, **kwargs):
    data = request.data
    file = request.FILES
    user_obj = User.objects.get(id = kwargs['user'])
    Profile.objects.create(
        user = user_obj,
        mobileNo = data['mobileNo'],
        iAm = data['iAm'],
        speciality = data['speciality'],
        clinicName = data['clinicName'],
        profileImage = file['profileImage'],
    )
    return


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # email_plaintext_message = f"https://my-guru-test.herokuapp.com/password-reset/{reset_password_token.key}"
    email_plaintext_message = f"http://localhost:3000/password-reset/{reset_password_token.key}"

    send_mail(
        "Password Reset for {title}".format(title="Zetamed's password resest"),
        email_plaintext_message,
        "visheshsolanki12345@gmail.com",
        [reset_password_token.user.email]
    )