import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel
from django.utils.crypto import get_random_string

def generate_api_token():
    return get_random_string(64)

class Project(TimeStampedModel):
    project_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey('frontend.User')
    category = models.ForeignKey('frontend.Category')
    project_name = models.TextField()
    project_source = models.TextField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    hash = models.TextField()
    slug = models.TextField()

    @staticmethod
    def generate_slug(name):
        return name.replace(' ', '-').lower()

    def is_owned_by(self, user):
        return user == self.owner

class User(AbstractUser, TimeStampedModel):
    nickname = models.TextField(null=True)
    api_token = models.TextField(unique=True, default=generate_api_token)

class Category(TimeStampedModel):
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.TextField()