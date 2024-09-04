import pytest

from django.contrib.auth import logout
from django.urls import reverse

from tests.conftest import client


@pytest.mark.django_db
def test_valid_logout_view(client):
    # Checking that the user is logged out after executing a POST logout request
    data = {
        "username": "testuser",
        "password": "StrongPassword123",
    }
    response = client.post(reverse("logout"), data)

    assert response.status_code == 302
    assert response.url == reverse("home")


@pytest.mark.django_db
def test_user_is_not_authenticated(client):
    # Checking that the user is no longer authenticated after logging out
    logout(client)

    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert "_auth_user_id" not in client.session
