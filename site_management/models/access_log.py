"""
- `AccessLog model`: Logs details of user access to a website,
 including the user, the website, the timestamp of access,
 and the amount of data uploaded and downloaded.
"""
from django.contrib.auth import get_user_model
from django.db import models

from site_management.models.website import Website

User = get_user_model()


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_logs', verbose_name='User',)
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='access_logs', verbose_name='Website',)
    accessed_at = models.DateTimeField('Accessed at', auto_now_add=True)
    data_uploaded = models.PositiveIntegerField('Data uploaded', default=0)
    data_downloaded = models.PositiveIntegerField('Data downloaded', default=0)

    def __str__(self):
        return f"{self.user.username} accessed {self.website.name} at {self.accessed_at}"
