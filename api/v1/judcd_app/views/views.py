from rest_framework import viewsets
from judcd_app.models import *
from api.v1.judcd_app.serializers.serializers import *
from rest_framework.permissions import IsAuthenticated

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    permission_classes = [IsAuthenticated]

class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [IsAuthenticated]

class TypePartenaireViewSet(viewsets.ModelViewSet):
    queryset = Type_Partenaire.objects.all()
    serializer_class = TypePartenaireSerializer
    permission_classes = [IsAuthenticated]

class PartenaireViewSet(viewsets.ModelViewSet):
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireSerializer
    permission_classes = [IsAuthenticated]

class DonViewSet(viewsets.ModelViewSet):
    queryset = Don.objects.all()
    serializer_class = DonSerializer
    permission_classes = [IsAuthenticated]

class TemoignageViewSet(viewsets.ModelViewSet):
    queryset = Temoignage.objects.all()
    serializer_class = TemoignageSerializer
    permission_classes = [IsAuthenticated]

class MembreEquipeViewSet(viewsets.ModelViewSet):
    queryset = Membre_Equipe.objects.all()
    serializer_class = MembreEquipeSerializer
    permission_classes = [IsAuthenticated]

class TypeActionViewSet(viewsets.ModelViewSet):
    queryset = Type_Action.objects.all()
    serializer_class = TypeActionSerializer
    permission_classes = [IsAuthenticated]

class GalerieActionViewSet(viewsets.ModelViewSet):
    queryset = Galerie_Action.objects.all()
    serializer_class = GalarieActionSerializer
    permission_classes = [IsAuthenticated]

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsAuthenticated]

class TypeActualiteViewSet(viewsets.ModelViewSet):
    queryset = Type_Actualite.objects.all()
    serializer_class = TypeActualiteSerializer
    permission_classes = [IsAuthenticated]

