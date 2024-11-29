from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Class used to create the table for users in the database"""
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True, blank=True)
    verify_token = models.UUIDField(null=True, blank=True, editable=False)

    bio = models.CharField(max_length=255, blank=True)
    # profile_image = models.ImageField()

    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # If the username is empty, set it to the email
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

    # Sets the table name in the database
    class Meta:
        db_table = 'auth_user'

