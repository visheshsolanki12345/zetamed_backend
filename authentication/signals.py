from django.contrib.auth.models import User
from django.dispatch import receiver, Signal
from django.db.models.signals import pre_init, pre_save, pre_delete, post_init, post_save, post_delete
from .models import Profile
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.utils.encoding import force_bytes, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


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
        # profileImage = file['profileImage'],
    )
    return


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # email_plaintext_message = f"https://my-guru-test.herokuapp.com/password-reset/{reset_password_token.key}"
    # uid = urlsafe_base64_encode(force_bytes(reset_password_token.user.id))
    # print('uid', uid)
    # findId = smart_str(urlsafe_base64_decode(uid))
    # print('find Id', findId)
    # token = PasswordResetTokenGenerator().make_token(reset_password_token.user)
    # if not PasswordResetTokenGenerator().check_token(reset_password_token.user, token):
    #     print('not token user verify')
    # else:
    #     print('token user verify')
    # print('token', token)

    email_plaintext_message = f"http://localhost:3000/password-reset/{reset_password_token.key}"

    send_mail(
        "Password Reset for {title}".format(title="Zetamed's password resest"),
        email_plaintext_message,
        "visheshsolanki12345@gmail.com",
        [reset_password_token.user.email]
    )