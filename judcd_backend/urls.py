"""
URL configuration for judcd_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static


from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="JUDCD API",
#         default_version='v1',
#         description="Documentation de l'API JUDCD",
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

# from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="JUDCD API",
        default_version='v1',
        description="Documentation de l'API JUDCD",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/v1/', include('api.v1.judcd_app.urls')),

    path('', include('judcd_app.urls')),


    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    
    # Redoc (optionnel)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

