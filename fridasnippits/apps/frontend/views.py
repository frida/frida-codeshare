from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from fridasnippits.apps.frontend.models import Category, Project, User


def index(request):
    return render(request, 'index.html')

@login_required
def new(request):
    return render(request, 'new.html', {
        "categories": Category.objects.all()
    })

@login_required
def project_view(request, nickname, project_name):
    try:
        project_user = User.objects.get(nickname=nickname[1:])
        project = Project.objects.get(owner=project_user, project_name=project_name.lower())
    except Project.DoesNotExist:
        raise Http404

    return render(request, 'project_view.html', {
        "project": project,
        "is_owner": project.is_owned_by(request.user)
    })


@login_required
def project_edit(request, nickname, project_name):
    try:
        project = Project.objects.get(project_name=project_name)
    except:
        pass

    return render(request, 'project_view.html')
