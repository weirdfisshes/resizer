import django.urls

from . import views


api_patterns = [
    django.urls.path('resize_image', views.ImageAPI.as_view(), name="resize_image"),
]
