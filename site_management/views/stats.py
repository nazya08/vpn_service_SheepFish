"""
This file contains mixins and views for logging user interactions with websites
and displaying statistical data on these interactions.

Classes included:

- `LogAccessMixin`: Provides methods to log user access and page transitions to the database.
- `StatsDashboardView`: A view that aggregates and displays statistics on page transitions and traffic data,
  filtered by the logged-in user, on the dashboard page.
"""

from django.db.models import Count, Sum
from django.views.generic import TemplateView

from site_management.models.access_log import AccessLog
from site_management.models.page_transition import PageTransition


class LogAccessMixin:
    def log_access(self, user, website, data_uploaded, data_downloaded):
        AccessLog.objects.create(
            user=user,
            website=website,
            data_uploaded=data_uploaded,
            data_downloaded=data_downloaded
        )

    def log_transition(self, user, website, from_url, to_url):
        PageTransition.objects.create(
            user=user,
            website=website,
            from_url=from_url,
            to_url=to_url
        )


class StatsDashboardView(TemplateView):
    template_name = 'site_management/stats_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Collecting transition statistics
        page_transitions = PageTransition.objects.filter(user=user).values('website__name').annotate(
            transitions_count=Count('id')
        ).order_by('-transitions_count')

        # Collecting traffic statistics
        traffic_stats = AccessLog.objects.filter(user=user).values('website__name').annotate(
            total_uploaded=Sum('data_uploaded'),
            total_downloaded=Sum('data_downloaded')
        ).order_by('-total_uploaded', '-total_downloaded')

        context['page_transitions'] = page_transitions
        context['traffic_stats'] = traffic_stats

        return context
