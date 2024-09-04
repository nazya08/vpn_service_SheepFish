import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from site_management.models.access_log import AccessLog
from site_management.models.page_transition import PageTransition
from site_management.models.website import Website
from users.models import Profile

User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", email="testuser@example.com", password="StrongPassword123")


@pytest.fixture
def user_with_profile(user):
    Profile.objects.create(user=user)
    return user


@pytest.fixture
def website(user):
    return Website.objects.create(user=user, name="example.com", original_url="https://example.com")


@pytest.fixture
def log_access_data(user, website):
    website = website
    AccessLog.objects.create(
        user=user,
        website=website,
        data_uploaded=1024,
        data_downloaded=2048
    )


@pytest.fixture
def log_page_transition(user, website):
    website = website
    PageTransition.objects.create(
        user=user,
        website=website,
        from_url='/old-page/',
        to_url='/new-page/'
    )
