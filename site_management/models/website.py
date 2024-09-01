"""
- `Website model`: Represents a website added by a user, including fields for the website's name, URL, and creation date.
"""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Website(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sites', verbose_name='User',)
    name = models.CharField('Name', max_length=100, unique=True)
    original_url = models.URLField('Website URL')
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    def __str__(self):
        return self.name
