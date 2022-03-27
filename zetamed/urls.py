
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from patient import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authentication/', include('authentication.urls')),
    path('api/patient/', include('patient.urls')),    
    path('self/', views.test),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)