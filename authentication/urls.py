
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('send-otp/', views.send_otp, name='send-otp'),
    path('otp-verify/', views.otp_verify, name='otp-verify'),
    path('user-register/', views.user_register, name='user-register'),
    path('login/', views.MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('password-change/', views.ChangePasswordView.as_view(), name='password-change'),
    path('user-data-change/<int:pk>/', views.user_data_change, name='user-data-change'),
    path('find-user/<str:token>/', views.find_user_by_token, name='find-user'),
    path('user-profile-change/<int:pk>/', views.user_profile_change, name='user-profile-change'),
    path('get-user-profile/', views.get_user_profile, name='get-user-profile'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
