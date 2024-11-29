from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('verify/<uuid:token>', VerifyEmailView.as_view()),
    path('verify-otp', VerifyOTPView.as_view()),
    path('profile/<int:pk>', UserProfileView.as_view()),
]