from django.apps import apps
from django.contrib import admin

app = apps.get_app_config("frontend")
for model_name, model in app.models.items():
    model_admin = type(model_name + "Admin", (admin.ModelAdmin,), {})

    model_admin.list_display = (
        model.admin_list_display
        if hasattr(model, "admin_list_display")
        else tuple([field.name for field in model._meta.fields])
    )
    model_admin.list_filter = (
        model.admin_list_filter
        if hasattr(model, "admin_list_filter")
        else model_admin.list_display
    )
    model_admin.list_display_links = (
        model.admin_list_display_links
        if hasattr(model, "admin_list_display_links")
        else ()
    )
    model_admin.list_editable = (
        model.admin_list_editable if hasattr(model, "admin_list_editable") else ()
    )
    model_admin.search_fields = (
        model.admin_search_fields if hasattr(model, "admin_search_fields") else ()
    )

    admin.site.register(model, model_admin)
