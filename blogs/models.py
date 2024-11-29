from django.db import models
from django.contrib.postgres.fields import ArrayField
from enum import Enum
from django.conf import settings
from django.core.exceptions import ValidationError


# Enum class for access level
class AccessLevel(Enum):
    PRIVATE = 1
    FOLLOWERS_ONLY = 2
    PUBLIC = 3

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.replace('_', ' ').title()) for tag in cls]


# Enum class for interaction type
class InteractionType(Enum):
    LIKE = 1
    COMMENT = 2
    BOOKMARK = 3
    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.replace('_', ' ').title()) for tag in cls]


# Table for blogs; references auth_user
class Blogs(models.Model):
    blog_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_user"
    )
    title = models.CharField(max_length=50, blank=True)
    content = models.CharField(max_length=2500, blank=True)
    tags = ArrayField(models.CharField(max_length=30), size=10)
    access_level = models.IntegerField(
        choices=AccessLevel.choices(),
        default=AccessLevel.PUBLIC.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        for tag in self.tags:
            if len(tag) > 30:
                raise ValidationError(f"Tag '{tag}' exceeds the maximum length of 30 characters.")
        
        if len(self.title) > 50:
            raise ValidationError("The title exceeds the maximum length of 50 characters.")

        if len(self.content) > 2500:
            raise ValidationError("The content exceeds the maximum length of 2500 characters.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "blogs"


# Table for comments; references auth_user & blogs
class Comments(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_comments"
    )
    blog = models.ForeignKey(
        "blogs",
        on_delete=models.CASCADE,
        related_name="blog_comments"
    )
    interaction = models.OneToOneField(
        "interactions",
        on_delete=models.CASCADE,
        related_name="comment_interaction"
    )
    content = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if len(self.content) > 200:
            raise ValidationError("The comment content exceeds the maximum length of 200 characters.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "comments"


# Table for interactions; references auth_user & blogs
class Interactions(models.Model):
    interaction_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="interactions_user"
    )
    blog = models.ForeignKey(
        "blogs",
        on_delete=models.CASCADE,
        related_name="interactions_blog"
    )
    type = models.IntegerField(
        choices=InteractionType.choices(),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "interactions" 


class Followers(models.Model):
    action_id = models.BigAutoField(primary_key=True)
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers_user"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following_user"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("A user cannot follow themselves.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_following"
            )
        ]
        db_table = "followers" 