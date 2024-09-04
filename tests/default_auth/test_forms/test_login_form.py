import pytest
from default_auth.forms import LoginForm
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_invalid_login_form():
    # Check the validation of a form with incorrect data
    form_data = {
        "username": "User123",
        "password": "",
    }

    form = LoginForm(data=form_data)
    assert form.is_valid() is False


@pytest.mark.django_db
def test_valid_login_form():
    # Check the validation of a form with correct data
    form_data = {
        "username": "User123",
        "password": "value1324",
    }
    form = LoginForm(data=form_data)
    assert form.is_valid() is True


@pytest.mark.django_db
def test_invalid_login():
    # Verify failed login with incorrect data
    User.objects.create_user(username="testuser", password="correctpassword")
    login_data = {"username": "testuser", "password": "wrongpassword"}
    form = LoginForm(data=login_data)
    assert form.is_valid() is True
    assert authenticate(username=login_data["username"], password=login_data["password"]) is None


@pytest.mark.django_db
def test_valid_login():
    # Verify correct login with correct data
    User.objects.create_user(username="testuser", password="correctpassword")
    login_data = {"username": "testuser", "password": "correctpassword"}
    form = LoginForm(data=login_data)
    assert form.is_valid() is True
    assert authenticate(username=login_data["username"], password=login_data["password"]) is not None
