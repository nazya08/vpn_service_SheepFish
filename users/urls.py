"""
URLs for the users app.
"""
from django.urls import path

from . import views


urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('profile-edit/', views.ProfileEditView.as_view(), name="profile_editing"),
    path('create-profile/', views.ProfileCreateView.as_view(), name='create_profile'),
]
