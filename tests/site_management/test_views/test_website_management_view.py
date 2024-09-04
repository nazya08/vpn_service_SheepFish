import pytest

from django.urls import reverse

from tests.conftest import client, user


@pytest.mark.django_db
def test_website_management_view(client, user):
    client.login(username=user.username, password='StrongPassword123')
    url = reverse('website_management_main')
    response = client.get(url)
    assert response.status_code == 200
