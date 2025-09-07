from django.contrib import admin
from django.urls import path, include  # добавляем include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('diary/', include('diary.urls', namespace='diary')),  # подключаем маршруты diary
    path('accounts/', include('django.contrib.auth.urls')),
]
