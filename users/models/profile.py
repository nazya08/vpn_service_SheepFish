from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        'users.User', models.CASCADE, related_name='profile',
        verbose_name='User', primary_key=True,
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True, verbose_name='Profile Picture')
    bio = models.TextField(null=True, blank=True, verbose_name='Bio')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Date of Birth')

    class Meta:
        verbose_name = "User's profile"
        verbose_name_plural = "Users profiles"

    def __str__(self):
        return f'{self.user} ({self.pk})'
