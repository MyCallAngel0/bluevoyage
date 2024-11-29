from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True, blank=True)
    verify_token = models.UUIDField(blank=True, editable=False)

    bio = models.CharField(max_length=255, blank=True)

    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # If the username is empty, set it to the email
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'auth_user'

