from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('list.urls')),
]

# from rest_framework.authtoken import views
from . import views

urlpatterns += [
    path('api-token-auth/', views.CustomAuthToken.as_view())
]
