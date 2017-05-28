import hashlib
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from fridasnippits.apps.api.schemas import NewProjectSchema
from fridasnippits.apps.frontend.models import Project, Category


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
            slug=Project.generate_slug(cleaned_data['name'])
        )
        return JsonResponse({
            "success": True,
            "link": request.build_absolute_uri(reverse('project_view', kwargs={"nickname": "@" + request.user.nickname, "project_name": project.project_slug}))
        })
    except:
        return JsonResponse({
            "success": False,
            "error": "Invalid input!"
        }, status=400)