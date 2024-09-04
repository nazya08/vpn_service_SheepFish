import pytest

from django.urls import reverse
from django.db.utils import IntegrityError

from site_management.models.access_log import AccessLog
from site_management.models.page_transition import PageTransition
from tests.conftest import client, user, log_access_data, log_page_transition, website


@pytest.mark.django_db
def test_log_access(log_access_data):
    assert AccessLog.objects.count() == 1
    log = AccessLog.objects.first()
    assert log.data_uploaded == 1024
    assert log.data_downloaded == 2048


@pytest.mark.django_db
def test_log_page_transition(log_page_transition):
    assert PageTransition.objects.count() == 1
    transition = PageTransition.objects.first()
    assert transition.from_url == '/old-page/'
    assert transition.to_url == '/new-page/'


@pytest.mark.django_db
def test_stats_dashboard_view(client, user, log_access_data, log_page_transition):
    client.login(username=user.username, password='StrongPassword123')
    response = client.get(reverse('stats_dashboard'))

    assert response.status_code == 200
    assert 'page_transitions' in response.context
    assert 'traffic_stats' in response.context

    page_transitions = response.context['page_transitions']
    traffic_stats = response.context['traffic_stats']

    assert len(page_transitions) == 1
    assert page_transitions[0]['transitions_count'] == 1

    assert len(traffic_stats) == 1
    assert traffic_stats[0]['total_uploaded'] == 1024
    assert traffic_stats[0]['total_downloaded'] == 2048


@pytest.mark.django_db
def test_log_access_invalid_data(user, website):
    with pytest.raises(IntegrityError):
        AccessLog.objects.create(
            user=user,
            website=website,
            data_uploaded=None,  # This should raise an error as data_uploaded is mandatory
            data_downloaded=2048
        )
