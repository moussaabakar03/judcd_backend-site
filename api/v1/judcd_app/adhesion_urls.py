from django.urls import path
from .views.adhesion_views import (
    creer_adhesion, lister_adhesions, detail_adhesion,
    action_adhesion, statistiques_adhesions
)

urlpatterns = [
    # Public endpoints
    path('adhesion/creer/', creer_adhesion, name='creer_adhesion'),
    
    # Admin endpoints
    path('admin/adhesions/', lister_adhesions, name='lister_adhesions'),
    path('admin/adhesions/<uuid:adhesion_id>/', detail_adhesion, name='detail_adhesion'),
    path('admin/adhesions/<uuid:adhesion_id>/action/', action_adhesion, name='action_adhesion'),
    path('admin/adhesions/statistiques/', statistiques_adhesions, name='statistiques_adhesions'),
]
