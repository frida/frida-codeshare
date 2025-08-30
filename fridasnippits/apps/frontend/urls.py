from django.urls import re_path

from fridasnippits.apps.frontend import views

urlpatterns = [
    re_path(r"^$", views.index),
    re_path(r"^new/?", views.new),
    re_path(r"^browse/?", views.browse),
    re_path(
        r"^(?P<nickname>\@[\w\-]+)/(?P<project_slug>[a-zA-Z0-9\-]+)/edit/?",
        views.project_edit,
        name="project_edit",
    ),
    re_path(
        r"^(?P<nickname>\@[\w\-]+)/(?P<project_slug>[a-zA-Z0-9\-]+)/",
        views.project_view,
        name="project_view",
    ),
    re_path(
        r"^(?P<nickname>\@[\w\-]+)/?$", views.user_info_view, name="user_info_view"
    ),
]
