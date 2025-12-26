from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.api.v1.urls')),
    path('api/v1/', include('articles.api.v1.urls')),
    path('api/v1/', include('tags.api.v1.urls')),
    path('api/v1/', include('comments.api.v1.urls')),
]
