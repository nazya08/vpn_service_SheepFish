"""
- `PageTransition model`: Represents a record of a user navigating from one URL to another on a website.
 Includes fields for the user, the website, the originating and destination URLs, and the time of the transition.
"""
from django.contrib.auth import get_user_model
from django.db import models

from site_management.models.website import Website

User = get_user_model()


class PageTransition(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='page_transitions', verbose_name='User',
    )
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name='page_transitions', verbose_name='Website',
    )
    from_url = models.URLField('From URL',)
    to_url = models.URLField('To URL',)
    transition_time = models.DateTimeField('Transition time', auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} navigated from {self.from_url} to {self.to_url}"
