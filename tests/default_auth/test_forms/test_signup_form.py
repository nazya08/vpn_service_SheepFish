import pytest
from default_auth.forms import SignupForm


@pytest.fixture
def valid_signup_form_data():
    return {
        "username": "User123",
        "email": "user_123@gmail.com",
        "password": "Value1324",
        "password2": "Value1324",
    }


@pytest.mark.django_db
def test_invalid_signup_form():
    # Check the validation of a form with incorrect data
    form_data = {
        "username": "",
        "email": "invalid_email",
        "password": "123",
        "password2": "123",
    }

    form = SignupForm(data=form_data)
    assert form.is_valid() is False


@pytest.mark.django_db
def test_valid_signup_form(valid_signup_form_data):
    # Check the validation of a form with correct data
    form = SignupForm(data=valid_signup_form_data)
    assert form.is_valid() is True


@pytest.mark.django_db
def test_password_mismatch():
    # Check for incorrect password entry
    form_data = {
        "username": "User123",
        "email": "user_123@gmail.com",
        "password": "value1324",
        "password2": "value124",
    }
    form = SignupForm(data=form_data)
    assert form.is_valid() is False
    assert "password" in form.errors


@pytest.mark.django_db
def test_password_correctness(valid_signup_form_data):
    # Check for correct password entry
    form = SignupForm(data=valid_signup_form_data)
    assert form.is_valid() is True
    assert "password" not in form.errors
    assert "password" in form.cleaned_data


@pytest.mark.django_db
def test_signup_form_save(valid_signup_form_data):
    # Checking the creation of a user with the correct data
    form = SignupForm(data=valid_signup_form_data)
    assert form.is_valid() is True

    user = form.save()
    assert user is not None
    assert user.username == valid_signup_form_data["username"]
    assert user.email == valid_signup_form_data["email"]
    assert user.password == valid_signup_form_data["password"]


@pytest.mark.django_db
def test_signup_form_user_activation(valid_signup_form_data):
    # Checking that a new user is created with an active status
    form = SignupForm(data=valid_signup_form_data)
    assert form.is_valid() is True

    user = form.save()
    assert user.is_active is True
