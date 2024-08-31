from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number=None, email=None, password=None, username=None, **extra_fields):
        if not (email or phone_number or username):
            raise ValidationError('Please provide either an email, phone number, or username.')

        if email:
            email = self.normalize_email(email)
            if self.model.objects.filter(email=email).exists():
                raise ValidationError('A user with this email already exists.')

        if phone_number and self.model.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('A user with this phone number already exists.')

        if not username:
            if email:
                username = email.split('@')[0]  # Використовує частину email до '@'
            else:
                username = phone_number

        user = self.model(username=username, **extra_fields)
        if email:
            user.email = email
        if phone_number:
            user.phone_number = phone_number

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, email=None, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )

    def create_superuser(self, phone_number=None, email=None, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )
