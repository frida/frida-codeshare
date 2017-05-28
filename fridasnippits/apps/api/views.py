import hashlib
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from fridasnippits.apps.api.schemas import UpdateProjectSchema, NewProjectSchema
from fridasnippits.apps.frontend.models import Project, Category, User


@login_required
@require_http_methods(["POST",])
def create_new(request):
    try:
        cleaned_data = NewProjectSchema(json.loads(request.body))
        project_category = Category.objects.get(name=cleaned_data['category'])
        project = Project.objects.create(
            owner=request.user,
            category=project_category,
            project_name=cleaned_data['name'],
            project_source=cleaned_data['source'],
            hash=hashlib.sha256(cleaned_data['source'].encode('utf-8')).hexdigest(),
            description=cleaned_data['description'],
            project_slug=Project.generate_slug(cleaned_data['name'])
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
@require_http_methods(["POST", "DELETE"])
def update_project(request, nickname, project_slug):
    try:
        project_owner = User.objects.get(nickname=nickname)
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
