import pytest
from django.urls import reverse

from tests.conftest import client, user
from users.forms import ProfileForm


@pytest.mark.django_db
def test_profile_create_view_access(client, user):
    client.login(username=user.username, password='StrongPassword123')
    url = reverse('create_profile')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], ProfileForm)


@pytest.mark.django_db
def test_profile_create_view_post_valid_data(client, user):
    client.login(username=user.username, password='StrongPassword123')
    url = reverse('create_profile')
    response = client.post(url, {
        'bio': 'New bio',
        'profile_picture': '',
    })
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_profile_create_view_redirect_for_anonymous_user(client):
    url = reverse('create_profile')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/?next=/users/create-profile/')
