from rest_framework import viewsets
from judcd_app.models import *
from judcd_app.serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]  # Lecture publique
        return [IsAuthenticated]  # Écriture nécessite authentification

class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [IsAuthenticated]

class TypePartenaireViewSet(viewsets.ModelViewSet):
    queryset = Type_Partenaire.objects.all()
    serializer_class = TypePartenaireSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]  # Lecture publique
        return [IsAuthenticated]  # Écriture nécessite authentification

class PartenaireViewSet(viewsets.ModelViewSet):
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]  # Lecture publique
        return [IsAuthenticated]  # Écriture nécessite authentification

class DonViewSet(viewsets.ModelViewSet):
    queryset = Don.objects.all()
    serializer_class = DonSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]  # Lecture publique
        return [IsAuthenticated]  # Écriture nécessite authentification

class TemoignageViewSet(viewsets.ModelViewSet):
    queryset = Temoignage.objects.all()
    serializer_class = TemoignageSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]  # Lecture publique
        return [IsAuthenticated]  # Écriture nécessite authentification

class MembreEquipeViewSet(viewsets.ModelViewSet):
    queryset = Membre_Equipe.objects.all()
    serializer_class = MembreEquipeSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]  # Lecture publique
        return [IsAuthenticated]  # Écriture nécessite authentification

class TypeActionViewSet(viewsets.ModelViewSet):
    queryset = Type_Action.objects.all()
    serializer_class = TypeActionSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]  # Lecture publique
        return [IsAuthenticated]  # Écriture nécessite authentification

class GalerieActionViewSet(viewsets.ModelViewSet):
    queryset = Galerie_Action.objects.all()
    serializer_class = GalerieActionSerializer
    permission_classes = [IsAuthenticated]  # Par défaut, nécessite authentification

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]  # Lecture publique
        return [IsAuthenticated]  # Écriture nécessite authentification

class TypeActualiteViewSet(viewsets.ModelViewSet):
    queryset = Type_Actualite.objects.all()
    serializer_class = TypeActualiteSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]  # Lecture publique
        return [IsAuthenticated]  # Écriture nécessite authentification

