import pytest
import requests

from django.urls import reverse

from site_management.models.website import Website
from tests.conftest import client, user


@pytest.fixture
def mock_requests_get(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '<html><body><a href="https://example.com/test">Test</a></body></html>'
    mock_response.content = mock_response.text.encode('utf-8')
    mock_response.headers = {'Content-Type': 'text/html'}
    return mocker.patch('requests.get', return_value=mock_response)


@pytest.mark.django_db
def test_proxy_view_get_existing_website(client, user, mock_requests_get):
    client.login(username=user.username, password='StrongPassword123')
    Website.objects.create(user=user, name='testsite', original_url='https://example.com')

    url = reverse('proxy_view', kwargs={'user_site_name': 'testsite', 'route': ''})
    response = client.get(url)

    assert response.status_code == 200
    assert response['Content-Type'] == 'text/html'
    assert 'href="/testsite/test"' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_proxy_view_get_nonexistent_website(client):
    url = reverse('proxy_view', kwargs={'user_site_name': 'nonexistent', 'route': ''})
    response = client.get(url)

    assert response.status_code == 404
    assert "Website not found" in response.content.decode('utf-8')


@pytest.mark.django_db
def test_proxy_view_get_request_exception(client, user, mocker):
    Website.objects.create(user=user, name='testsite', original_url='https://example.com')

    mocker.patch('requests.get', side_effect=requests.RequestException('Connection error'))

    url = reverse('proxy_view', kwargs={'user_site_name': 'testsite', 'route': ''})
    response = client.get(url)

    assert response.status_code == 404
    assert "Error fetching the original site" in response.content.decode('utf-8')


@pytest.mark.django_db
def test_proxy_view_logs_access_and_transition(client, user, mocker, mock_requests_get):
    client.login(username=user.username, password='StrongPassword123')
    Website.objects.create(user=user, name='testsite', original_url='https://example.com')

    mock_log_transition = mocker.patch('site_management.views.stats.LogAccessMixin.log_transition')
    mock_log_access = mocker.patch('site_management.views.stats.LogAccessMixin.log_access')

    url = reverse('proxy_view', kwargs={'user_site_name': 'testsite', 'route': ''})
    response = client.get(url)

    assert response.status_code == 200

    assert mock_log_transition.called
    assert mock_log_access.called
