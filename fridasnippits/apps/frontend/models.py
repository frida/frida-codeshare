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
    description = models.TextField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    hash = models.TextField()
    project_slug = models.TextField()

    class Meta:
        unique_together = ("owner", "project_slug")

    @staticmethod
    def generate_slug(name):
        return name.replace(' ', '-').lower()

    def _human_format(self, num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        # add more suffixes if you need them
        return '%d%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    @property
    def vote_count(self):
        return self._human_format(self.likes)

    @property
    def view_count(self):
        return self._human_format(self.views)

    @property
    def frida_command(self):
        return "$ frida --codeshare {}/{}".format(self.owner.nickname, self.slug)

    def is_owned_by(self, user):
        return user == self.owner

class User(AbstractUser, TimeStampedModel):
    nickname = models.TextField(null=True)
    api_token = models.TextField(unique=True, default=generate_api_token)

    def mark_as_admin(self):
        self.is_superuser = True
        self.is_staff = True
        self.save()


class Category(TimeStampedModel):
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.TextField()