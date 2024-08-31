"""
URLs for the default_auth app.
"""
from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name="logout"),
]
