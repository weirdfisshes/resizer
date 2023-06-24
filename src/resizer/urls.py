import django.contrib
import django.urls

import api.urls
from . import docs


urlpatterns = [
    django.urls.path(
        'docs/',
        docs.schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    django.urls.path('', django.urls.include(api.urls.api_patterns)),
]
