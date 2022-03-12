from django.contrib.auth.models import User
from django.dispatch import receiver, Signal
from django.db.models.signals import pre_init, pre_save, pre_delete, post_init, post_save, post_delete
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.core.files.base import ContentFile

def user_directory_path(instance, filename):
    profile_pic_name = f'patient-images/{instance.user.username}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    else:
        default_storage.save(profile_pic_name, ContentFile(filename.read()))
    return profile_pic_name


patient_profile_data = Signal(providing_args=['request', 'obj'])
@receiver(patient_profile_data)
def save_patient(sender, request, **kwargs):
    file = request.FILES
    obj = kwargs['obj']
    obj.patientImage =  user_directory_path(request, file['patientImage'])
    obj.save()
    return


