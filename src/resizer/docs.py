import drf_yasg
import drf_yasg.views
import rest_framework


schema_view = drf_yasg.views.get_schema_view(
    drf_yasg.openapi.Info(
        title="Сервис уменьшения картинок",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=drf_yasg.openapi.Contact(email="contact@snippets.local"),
        license=drf_yasg.openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(rest_framework.permissions.AllowAny,),
)