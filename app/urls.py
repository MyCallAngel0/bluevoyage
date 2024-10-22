from django.urls import path
from . import views


urlpatterns = [
    path('random/', views.randomPage, name="random"),
    path('test/', views.testPage, name="test"),
    path('login', views.loginTestPage, name="login-test"),
    path('register', views.registerTestPage, name="register-test"),
    path('logout', views.logoutUser, name="logout"),
]