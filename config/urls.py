from django.contrib import admin
from django.urls import include, path  # добавляем include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("diary/", include("diary.urls", namespace="diary")),
    path("users/", include("users.urls", namespace="users")),
    path("accounts/", include("django.contrib.auth.urls")),
]
