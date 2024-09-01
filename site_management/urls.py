"""
URLs for the site_management app.
"""
from django.urls import path, re_path
from django.views.generic import TemplateView

from site_management.views.stats import StatsDashboardView
from site_management.views.website import CreateSiteView, website_management_view, ProxyView

urlpatterns = [
    path("", website_management_view, name="website_management_main"),
    path('create/', CreateSiteView.as_view(), name='create_website'),
    path('stats/', TemplateView.as_view(template_name='site_management/stats_dashboard.html'), name='stats_dashboard'),
    path('stats-dashboard/', StatsDashboardView.as_view(), name='stats_dashboard'),
    re_path(r'^(?P<user_site_name>[^/]+)/(?P<route>.*)$', ProxyView.as_view(), name='proxy_view'),
]
