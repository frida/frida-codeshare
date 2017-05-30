import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import F
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
    views = models.IntegerField(default=0)
    hash = models.TextField()
    project_slug = models.TextField()
    latest_version = models.TextField()

    class Meta:
        unique_together = ("owner", "project_slug")

    def serialize(self):
        return {
            "id": str(self.project_id),
            "project_name": self.project_name,
            "description": self.description,
            "source": self.project_source,
            "slug": self.project_slug,
            "frida_version": self.latest_version
        }

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
        return self._human_format(self.liked_by.count())

    @property
    def view_count(self):
        return self._human_format(self.views)

    @property
    def frida_command(self):
        return "$ frida --codeshare {}/{}".format(self.owner.nickname, self.slug)

    def increment_view(self):
        self.views = F('views') + 1
        self.save()

    def is_owned_by(self, user):
        return user == self.owner

    def is_liked_by(self, user):
        return user.id in self.liked_by.values_list('id', flat=True)

class User(AbstractUser, TimeStampedModel):
    nickname = models.TextField(null=True)
    api_token = models.TextField(unique=True, default=generate_api_token)
    liked_projects = models.ManyToManyField(Project, related_name="liked_by")

    def mark_as_admin(self):
        self.is_superuser = True
        self.is_staff = True
        self.save()


class Category(TimeStampedModel):
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.TextField()