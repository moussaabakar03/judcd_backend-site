from rest_framework import viewsets
from judcd_app.models import *
from api.v1.judcd_app.serializers.serializers import *

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

class TypePartenaireViewSet(viewsets.ModelViewSet):
    queryset = Type_Partenaire.objects.all()
    serializer_class = TypePartenaireSerializer

class PartenaireViewSet(viewsets.ModelViewSet):
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireSerializer

class DonViewSet(viewsets.ModelViewSet):
    queryset = Don.objects.all()
    serializer_class = DonSerializer

class TemoignageViewSet(viewsets.ModelViewSet):
    queryset = Temoignage.objects.all()
    serializer_class = TemoignageSerializer

class MembreEquipeViewSet(viewsets.ModelViewSet):
    queryset = Membre_Equipe.objects.all()
    serializer_class = MembreEquipeSerializer

class TypeActionViewSet(viewsets.ModelViewSet):
    queryset = Type_Action.objects.all()
    serializer_class = TypeActionSerializer

class GalerieActionViewSet(viewsets.ModelViewSet):
    queryset = Galerie_Action.objects.all()
    serializer_class = GalarieActionSerializer

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

class TypeActualiteViewSet(viewsets.ModelViewSet):
    queryset = Type_Actualite.objects.all()
    serializer_class = TypeActualiteSerializer

