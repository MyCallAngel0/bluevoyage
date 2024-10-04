from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register2"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.homePage, name="home"),

    path('test/', views.homePage, name="random"),
]