from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
# from rest_framework_simplejwt.tokens import RefreshToken

from user_data import models as user_data_models


class UserManager(BaseUserManager):

    def _create_user(self, email, password, full_name, **extra_fields):
        if not email:
            raise TypeError('Users should have a Email')
        if not password:
            raise TypeError('Users should have a password')
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save()

        # popular os dados do usuario
        current_user_data = user_data_models.UserData(email=email)
        current_user_data.save()

        # user.save(using=self._db)
        return user

    def create_user(self, email, password, full_name="", **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', False)
        return self._create_user(email, password, full_name, **extra_fields)

    def create_superuser(self, email, password, full_name="", **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', False)
        return self._create_user(email, password, full_name, **extra_fields)


# AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                #   'twitter': 'twitter', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # auth_provider = models.CharField(
        # max_length=255, blank=False,
        # null=False, default=AUTH_PROVIDERS.get('email'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def email_user(self, subject, message):
        if self.full_name:
            subject = self.full_name + ', ' + subject[0].lower() + subject[1:]

        send_mail(
            subject=subject,
            message=message,
            from_email=None,  # DEFAULT_FROM_EMAIL setting
            recipient_list=[self.email],
            fail_silently=False
        )

    def __str__(self):
        return self.email

