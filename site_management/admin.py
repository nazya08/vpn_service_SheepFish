"""
AdminPanel for the site_management app.
"""
from django.contrib import admin

from site_management.models.access_log import AccessLog
from site_management.models.page_transition import PageTransition
from site_management.models.website import Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'original_url', 'created_at')
    search_fields = ('name', 'user__username', 'original_url')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)


@admin.register(PageTransition)
class PageTransitionAdmin(admin.ModelAdmin):
    list_display = ('user', 'website', 'from_url', 'to_url', 'transition_time')
    search_fields = ('user__username', 'website__name', 'from_url', 'to_url')
    list_filter = ('transition_time', 'website', 'user')
    ordering = ('-transition_time',)


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'website', 'accessed_at', 'data_uploaded', 'data_downloaded')
    search_fields = ('user__username', 'website__name')
    list_filter = ('accessed_at', 'website', 'user')
    ordering = ('-accessed_at',)
