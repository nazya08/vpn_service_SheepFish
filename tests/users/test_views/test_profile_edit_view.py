import pytest

from django.urls import reverse

from tests.conftest import client, user, user_with_profile
from users.forms import ProfileEditForm


@pytest.mark.django_db
def test_profile_edit_view_access(client, user_with_profile):
    client.login(username=user_with_profile.username, password='StrongPassword123')
    url = reverse('profile_editing')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], ProfileEditForm)


@pytest.mark.django_db
def test_profile_edit_view_post_valid_data(client, user_with_profile):
    client.login(username=user_with_profile.username, password='StrongPassword123')
    url = reverse('profile_editing')
    response = client.post(url, {
        'bio': 'Updated bio',
        'profile_picture': '',
    })
    assert response.status_code == 302
    assert response.url == reverse('profile')


@pytest.mark.django_db
def test_profile_edit_view_post_invalid_data(client, user_with_profile):
    client.login(username=user_with_profile.username, password='StrongPassword123')
    url = reverse('profile_editing')
    response = client.post(url, {})
    assert response.status_code == 302
    assert response.url == reverse('profile')


@pytest.mark.django_db
def test_profile_edit_view_redirect_for_anonymous_user(client):
    url = reverse('profile_editing')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/?next=/users/profile-edit/')
