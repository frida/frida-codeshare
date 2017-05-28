from django.conf.urls import url

from fridasnippits.apps.frontend import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^new/?', views.new),
    url(r'^(?P<nickname>\@\w+)/(?P<project_name>[a-zA-Z0-9\-]+)/', views.project_view, name='project_view'),
    url(r'^(?P<nickname>\@\w+)/(?P<project_name>[a-zA-Z0-9\-]+)/edit/?', views.project_edit, name='project_edit')
]
