import pytest

from django.urls import reverse

from site_management.models.website import Website
from site_management.forms.website import WebsiteForm
from tests.conftest import client, user


@pytest.mark.django_db
def test_create_site_view_get(client, user):
    client.login(username=user.username, password='StrongPassword123')
    url = reverse('create_website')
    response = client.get(url)

    assert response.status_code == 200
    assert 'site_management/create_website.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], WebsiteForm)


@pytest.mark.django_db
def test_create_site_view_post_valid_data(client, user):
    client.login(username=user.username, password='StrongPassword123')
    url = reverse('create_website')
    response = client.post(url, {
        'name': 'Test Site',
        'original_url': 'https://testsite.com'
    })

    assert response.status_code == 302
    assert response.url == reverse('website_management_main')

    site = Website.objects.get(name='Test Site')
    assert site.original_url == 'https://testsite.com'
    assert site.user == user


@pytest.mark.django_db
def test_create_site_view_post_invalid_data(client, user):
    client.login(username=user.username, password='StrongPassword123')
    url = reverse('create_website')
    response = client.post(url, {
        'name': '',
        'url': 'invalid-url'
    })

    assert response.status_code == 200
    assert 'form' in response.context
    assert not response.context['form'].is_valid()
    assert Website.objects.count() == 0
