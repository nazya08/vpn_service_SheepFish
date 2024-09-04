import pytest

from django.urls import reverse

from tests.conftest import client, user, user_with_profile


@pytest.mark.django_db
def test_profile_view_access(client, user_with_profile):
    client.login(username=user_with_profile.username, password='StrongPassword123')
    url = reverse('profile')
    response = client.get(url)
    assert response.status_code == 200
    assert 'user' in response.context
    assert response.context['user'] == user_with_profile


@pytest.mark.django_db
def test_profile_view_redirect_for_anonymous_user(client):
    url = reverse('profile')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/?next=/users/profile/')
