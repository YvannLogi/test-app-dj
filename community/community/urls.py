from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "bo"
admin.site.index_title = "Tableau d'administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls", namespace="accounts")),
    path("", include("core.urls", namespace="core")),

    path("__reload__/", include("django_browser_reload.urls")),
]