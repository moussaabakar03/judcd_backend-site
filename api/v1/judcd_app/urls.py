from rest_framework import routers
from api.v1.judcd_app.views.views import *
from api.v1.judcd_app.views.auth_views import custom_login, custom_refresh, get_user_info
from api.v1.judcd_app.views.public_views import (
    public_partenaires, public_team, public_actions, public_temoignages,
    public_types_actions, public_types_partenaires, public_contact,
    public_newsletter, public_donation, public_temoignage, public_stats, public_galerie_action
)
from . import adhesion_urls
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'newsletter', NewsletterViewSet, basename='newsletter')
router.register(r'type-partenaire', TypePartenaireViewSet, basename='type-partenaire')
router.register(r'partenaire', PartenaireViewSet, basename='partenaire')
router.register(r'don', DonViewSet, basename='don')
router.register(r'temoignage', TemoignageViewSet, basename='temoignage')
router.register(r'membre-equipe', MembreEquipeViewSet, basename='membre-equipe')
router.register(r'type-action', TypeActionViewSet, basename='type-action')
router.register(r'galerie-action', GalerieActionViewSet, basename='galerie-action')
router.register(r'action', ActionViewSet, basename='action')
router.register(r'type-actualite', TypeActualiteViewSet, basename='type-actualite')


urlpatterns = [
    path('', include(router.urls)),
    
    # JWT endpoints personnalisés (compatibles Python 3.14)
    path('login/', custom_login),
    path('refresh/', custom_refresh),
    path('auth/me/', get_user_info),
    
    # Endpoints publics (sans authentification)
    path('public/partenaires/', public_partenaires),
    path('public/team/', public_team),
    path('public/actions/', public_actions),
    path('public/temoignages/', public_temoignages),
    path('public/types-actions/', public_types_actions),
    path('public/types-partenaires/', public_types_partenaires),
    path('public/contact/', public_contact),
    path('public/newsletter/', public_newsletter),
    path('public/donation/', public_donation),
    path('public/temoignage/', public_temoignage),
    path('public/galerie-action/', public_galerie_action),
    path('public/stats/', public_stats),
    
    # Endpoints adhésions
] + adhesion_urls.urlpatterns