import hashlib
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from fridasnippits.apps.api.schemas import UpdateProjectSchema, NewProjectSchema, LikeProjectSchema
from fridasnippits.apps.frontend.models import Project, Category, User
from fridasnippits.core.github import get_latest_frida_release


@login_required
@require_http_methods(["POST",])
def create_new(request):
    try:
        cleaned_data = NewProjectSchema(json.loads(request.body))
        project_category = Category.objects.get(name=cleaned_data['category'])
        latest_release = get_latest_frida_release()
        project = Project.objects.create(
            owner=request.user,
            category=project_category,
            project_name=cleaned_data['name'],
            project_source=cleaned_data['source'],
            hash=hashlib.sha256(cleaned_data['source'].encode('utf-8')).hexdigest(),
            description=cleaned_data['description'],
            project_slug=Project.generate_slug(cleaned_data['name']),
            latest_version=latest_release
        )
        return JsonResponse({
            "success": True,
            "link": request.build_absolute_uri(reverse('project_view', kwargs={"nickname": "@" + request.user.nickname, "project_slug": project.project_slug}))
        })
    except:
        return JsonResponse({
            "success": False,
            "error": "Invalid input!"
        }, status=400)

@login_required
@require_http_methods(["POST",])
def like_project(request):
    try:
        cleaned_data = LikeProjectSchema(json.loads(request.body))

        project_uuid = cleaned_data['project_uuid']

        if request.user.liked_projects.filter(project_id=project_uuid).exists():
            return JsonResponse({
                "success": False,
                "error": "Already liked this project!"
            }, status=400)

        project = Project.objects.get(project_id=project_uuid)

        request.user.liked_projects.add(project)
        request.user.save()

        return JsonResponse({
            "success": True,
        })
    except:
        return JsonResponse({
            "success": False,
            "error": "Invalid input!"
        }, status=400)

@login_required
@require_http_methods(["POST", "DELETE"])
def update_project(request, nickname, project_slug):
    try:
        project_owner = User.objects.get(nickname__iexact=nickname)
        if project_owner != request.user:
            return JsonResponse({
                "success": False,
                "error": "You're not allowed to edit this!"
            }, status=400)
    except:
        return JsonResponse({
            "success": False,
            "error": "You're not allowed to edit this!"
        }, status=400)

    if request.method == "DELETE":
        project = Project.objects.get(owner=request.user, project_slug=project_slug)
        project.delete()
        return JsonResponse({
            "success": True
        })

    try:
        cleaned_data = UpdateProjectSchema(json.loads(request.body))
        project = Project.objects.get(owner=request.user, project_slug=project_slug)
        project_category = Category.objects.get(name=cleaned_data['category'])

        project.category = project_category
        project.project_source = cleaned_data['source']
        project.description = cleaned_data['description']
        project.hash = hashlib.sha256(cleaned_data['source'].encode('utf-8')).hexdigest()

        project.save()

        return JsonResponse({
            "success": True
        })

    except:
        return JsonResponse({
            "success": False,
            "error": "Invalid input!"
        }, status=400)


def project_data(request, nickname, project_slug):
    try:
        owner = User.objects.get(nickname__iexact=nickname)
        project = Project.objects.get(owner=owner, project_slug=project_slug)
        return HttpResponse(json.dumps(project.serialize(), indent=4), content_type="application/json")
    except:
        return JsonResponse({
            "success": False,
            "error": "Not found!"
        }, status=404)

def user_projects(request, nickname):
    try:
        owner = User.objects.get(nickname__iexact=nickname)
        payload = []
        for project in owner.project_set.all():
            payload.append(project.serialize())

        return HttpResponse(json.dumps(payload, indent=4), content_type="application/json")
    except:
        return JsonResponse({
            "success": False,
            "error": "Not found!"
        }, status=404)
