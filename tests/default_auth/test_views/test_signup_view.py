import pytest

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse

from tests.conftest import client

User = get_user_model()


@pytest.mark.django_db
def test_valid_signup_view(client):
    # Checking that the user can successfully register with the correct data
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "StrongPassword123",
        "password2": "StrongPassword123",
    }
    response = client.post(reverse("signup"), data)

    assert response.status_code == 302
    assert response.url == reverse("create_profile")

    user = User.objects.filter(username="testuser")
    assert user.exists()
    assert user.values("password") != data["password"]


@pytest.mark.django_db
def test_invalid_signup_view(client):
    # Checking that the user cannot register with incorrect data
    data = {
        "username": "testuser",
        "email": "invalidemail",
        "password": "StrongPassword123",
        "password2": "StrongPassword123",
    }
    response = client.post(reverse("signup"), data)

    assert response.status_code == 200
    assert response.context["form"].errors

    assert not User.objects.filter(username="testuser").exists()


@pytest.mark.django_db
def test_create_duplicate_user():
    # Checking for the creation of a duplicate contact, which should result in an IntegrityError.
    User.objects.create(
        username="testuser",
        email="testuser@example.com",
        password="StrongPassword123",
    )

    with pytest.raises(IntegrityError):
        User.objects.create(
            username="testuser",
            email="testuser@example.com",
            password="StrongPassword123",
        )
