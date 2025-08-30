from django.urls import include, re_path
from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import RedirectView


from fridasnippits.apps.api import views


def logout_view(request):
    logout(request)
    return redirect("/")


def hook_login_process(function):
    def wrapper(request):
        try:
            ret = function(request)
        except:
            return redirect("/")

        if "profile" in request.session and not request.user.nickname:
            request.user.nickname = request.session["profile"]["nickname"]
            assert request.user.nickname
            request.user.save()

        return ret

    return wrapper


admin.autodiscover()

urlpatterns = [
    # Include social_django URLs (handles /login/auth0 and /complete/auth0/)
    re_path('', include('social_django.urls', namespace='social')),
    
    re_path(r"^django_admin/", admin.site.urls),
    re_path(r"^sign-out/?", logout_view),
    re_path(r"^api/", include("fridasnippits.apps.api.urls")),
    re_path(r"", include("fridasnippits.apps.frontend.urls")),
    re_path("search/", views.search, name="search"),
]
