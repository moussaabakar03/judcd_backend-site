from rest_framework import serializers
from .models import Contact, Newsletter, Type_Partenaire, Partenaire, Don, Temoignage, Membre_Equipe, Type_Action, Galerie_Action, Action, Type_Actualite

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

class TypePartenaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Partenaire
        fields = '__all__'

class PartenaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partenaire
        fields = '__all__'

class DonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Don
        fields = '__all__'

class TemoignageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temoignage
        fields = '__all__'

class MembreEquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre_Equipe
        fields = '__all__'

class TypeActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Action
        fields = '__all__'

class GalerieActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Galerie_Action
        fields = '__all__'

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'

class TypeActualiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Actualite
        fields = '__all__'
