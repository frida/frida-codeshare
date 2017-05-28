from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import redirect

import django_auth0.views

def logout_view(request):
    logout(request)
    return redirect('/')

def hook_login_process(function):
    def wrapper(request):
        try:
            ret = function(request)
        except:
            return redirect('/')

        if 'profile' in request.session and not request.user.nickname:
            request.user.nickname = request.session['profile']['nickname']
            assert request.user.nickname
            request.user.save()

        return ret

    return wrapper

admin.autodiscover()

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^auth/callback/?', hook_login_process(django_auth0.views.process_login)),

    url(r'^django_admin/', admin.site.urls),

    url(r'^sign-out/?', logout_view),
    url(r'^api/', include('fridasnippits.apps.api.urls')),
    url(r'', include('fridasnippits.apps.frontend.urls')),

]
