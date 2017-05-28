from django.conf.urls import url

from fridasnippits.apps.api import views

urlpatterns = [
    url(r'^create-new/?', views.create_new, name="create_new_project")
]
