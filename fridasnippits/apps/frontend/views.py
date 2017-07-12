import hashlib

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from fridasnippits.apps.frontend.models import Category, Project, User


def index(request):
    projects = Project.objects.annotate(count=Count('liked_by')).order_by('-count')[:6]
    for project in projects:
        project.url = request.build_absolute_uri(reverse('project_view', kwargs={"nickname": "@" + project.owner.nickname, "project_slug": project.project_slug}))
    return render(request, 'index.html', {
        "projects": projects,
        "projects_are_odd": len(projects) % 2 == 1
    })

def browse(request):
    projects = Project.objects.annotate(count=Count('liked_by')).order_by('-count')
    paginator = Paginator(projects, 16)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    for project in results:
        project.url = request.build_absolute_uri(reverse('project_view', kwargs={"nickname": "@" + project.owner.nickname, "project_slug": project.project_slug}))
        project.is_owner = project.is_owned_by(request.user)

    return render(request, 'browse.html', {
        'projects': results,
        "projects_are_odd": len(results) % 2 == 1
    })

@login_required
def new(request):
    return render(request, 'new.html', {
        "categories": Category.objects.all(),
        "disable_sidebar": True
    })

def project_view(request, nickname, project_slug):
    try:
        project_user = User.objects.get(nickname__iexact=nickname[1:])
        project = Project.objects.get(owner=project_user, project_slug=project_slug.lower())
        project.increment_view()
    except:
        raise Http404

    return render(request, 'project_view.html', {
        "project": project,
        "is_owner": project.is_owned_by(request.user),
        "user_has_liked_project": project.is_liked_by(request.user),
        "fingerprint": hashlib.sha256(project.project_source.encode('utf-8')).hexdigest()
    })


@login_required
def project_edit(request, nickname, project_slug):
    try:
        requested_user = User.objects.get(nickname__iexact=nickname[1:])
        project = Project.objects.get(project_slug=project_slug.lower())
        if requested_user != request.user:
            raise Http404
    except:
        raise Http404

    return render(request, 'edit.html', {
        "project": project,
        "categories": Category.objects.all(),
    })

def user_info_view(request, nickname):
    nickname = nickname[1:]

    try:
        requested_user = User.objects.get(nickname__iexact=nickname)
        projects_queryset = Project.objects.filter(owner=requested_user)
        for project in projects_queryset:
            project.url = request.build_absolute_uri(reverse('project_view', kwargs={"nickname": "@" + requested_user.nickname, "project_slug": project.project_slug}))
    except:
        raise Http404

    return render(request, "user_info.html", {
        "is_owner": requested_user == request.user,
        "info_user": requested_user,
        "projects": projects_queryset,
        "projects_are_odd": len(projects_queryset) % 2 == 1
    })