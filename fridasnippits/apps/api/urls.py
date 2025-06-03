from django.urls import re_path
from fridasnippits.apps.api import views

urlpatterns = [
    re_path(r"^create-new/?", views.create_new, name="create_new_project"),
    re_path(
        r"^update/(?P<nickname>[\w\-]+)/(?P<project_slug>[a-zA-Z0-9\-]+)/",
        views.update_project,
        name="update_project",
    ),
    re_path(r"^like/?", views.like_project, name="like_project"),
    re_path(
        r"^project/(?P<nickname>[\w\-]+)/(?P<project_slug>[a-zA-Z0-9\-]+)/?",
        views.project_data,
        name="project_data",
    ),
    re_path(
        r"^project/(?P<nickname>[\w\-]+)/?", views.user_projects, name="user_projects"
    ),
    re_path(r"^search/?", views.search, name="search_projects"),
]
