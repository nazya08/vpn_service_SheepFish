import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from tests.conftest import client, user


User = get_user_model()


@pytest.mark.django_db
def test_valid_login_view(client, user):
    # Checking that the user can successfully authenticate with the correct data
    data = {
        "username": "testuser",
        "password": "StrongPassword123",
    }
    response = client.post(reverse("login"), data)

    assert response.status_code == 302
    assert response.url == reverse("home")

    # Checking that the user is authenticated after a successful login
    assert "_auth_user_id" in response.client.session
    assert response.client.session["_auth_user_id"] == str(user.pk)

    user_obj = User.objects.get(username="testuser")
    assert user_obj.is_authenticated
    assert user_obj.is_active
    assert user_obj.is_staff is False


@pytest.mark.django_db
def test_invalid_login_view(client, user):
    # Checking that the user cannot authenticate with incorrect data
    data = {
        "username": "testuser",
        "password": "WrongPassword123",  # incorrect password
    }
    response = client.post(reverse("login"), data)

    assert response.status_code == 200
    assert response.context["user"].is_authenticated is False
    assert "Invalid username or password." in response.content.decode("utf-8")


@pytest.mark.django_db
def test_invalid_form_login_view(client, user):
    # Checking that the user cannot authenticate with incorrect form data
    data = {
        "username": "",
        "password": "",
    }
    response = client.post(reverse("login"), data)

    assert response.status_code == 200
    assert response.context["user"].is_authenticated is False
    assert "Please correct the errors below." in response.content.decode("utf-8")
