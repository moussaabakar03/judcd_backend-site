from rest_framework import routers
from api.v1.judcd_app.views.views import *
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


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', include(router.urls)),

    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

]