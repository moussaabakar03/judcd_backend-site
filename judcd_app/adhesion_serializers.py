from rest_framework import serializers
from .adhesion_models import Adhesion, HistoriqueAdhesion
from django.contrib.auth.models import User

class AdhesionCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'une adhésion"""
    
    class Meta:
        model = Adhesion
        fields = [
            'nom', 'prenom', 'email', 'telephone', 'date_naissance', 'lieu_naissance',
            'profession', 'adresse', 'motivations', 'competences', 'disponibilites',
            'capture_depot', 'reference_paiement'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'capture_depot': {'required': True},
        }
    
    def validate_email(self, value):
        """Vérifie que l'email n'est pas déjà utilisé"""
        if Adhesion.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé pour une adhésion en cours.")
        return value
    
    def validate_date_naissance(self, value):
        """Vérifie que la personne est majeure"""
        from datetime import date
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("Vous devez être majeur pour adhérer.")
        return value

class AdhesionListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des adhésions (admin)"""
    
    age = serializers.SerializerMethodField()
    jours_restants = serializers.SerializerMethodField()
    
    class Meta:
        model = Adhesion
        fields = [
            'id', 'nom', 'prenom', 'email', 'telephone', 'profession', 
            'date_demande', 'date_approbation', 'date_expiration', 'statut',
            'montant_paye', 'traite_par', 'age', 'jours_restants'
        ]
    
    def get_age(self, obj):
        """Calcule l'âge du membre"""
        from datetime import date
        today = date.today()
        return today.year - obj.date_naissance.year - ((today.month, today.day) < (obj.date_naissance.month, obj.date_naissance.day))
    
    def get_jours_restants(self, obj):
        """Retourne le nombre de jours restants"""
        return obj.jours_restants()

class AdhesionDetailSerializer(serializers.ModelSerializer):
    """Serializer pour les détails d'une adhésion (admin)"""
    
    age = serializers.SerializerMethodField()
    jours_restants = serializers.SerializerMethodField()
    est_valide = serializers.SerializerMethodField()
    historique = serializers.SerializerMethodField()
    
    class Meta:
        model = Adhesion
        fields = '__all__'
    
    def get_age(self, obj):
        """Calcule l'âge du membre"""
        from datetime import date
        today = date.today()
        return today.year - obj.date_naissance.year - ((today.month, today.day) < (obj.date_naissance.month, obj.date_naissance.day))
    
    def get_jours_restants(self, obj):
        """Retourne le nombre de jours restants"""
        return obj.jours_restants()
    
    def get_est_valide(self, obj):
        """Vérifie si l'adhésion est valide"""
        return obj.est_valide()
    
    def get_historique(self, obj):
        """Retourne l'historique des actions"""
        historique = obj.historique.all().order_by('-date_action')
        return HistoriqueAdhesionSerializer(historique, many=True).data

class AdhesionActionSerializer(serializers.Serializer):
    """Serializer pour les actions admin sur les adhésions"""
    
    action = serializers.ChoiceField(choices=['APPROUVER', 'REJETER', 'RENOUVELER'])
    commentaires = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """Validation des actions"""
        action = data.get('action')
        
        if action == 'APPROUVER':
            # Vérifier que l'adhésion est en attente
            if self.instance.statut != 'EN_ATTENTE':
                raise serializers.ValidationError("Seules les adhésions en attente peuvent être approuvées")
        
        elif action == 'REJETER':
            # Vérifier que l'adhésion est en attente
            if self.instance.statut != 'EN_ATTENTE':
                raise serializers.ValidationError("Seules les adhésions en attente peuvent être rejetées")
        
        elif action == 'RENOUVELER':
            # Vérifier que l'adhésion est approuvée
            if self.instance.statut != 'APPROUVEE':
                raise serializers.ValidationError("Seules les adhésions approuvées peuvent être renouvelées")
        
        return data

class HistoriqueAdhesionSerializer(serializers.ModelSerializer):
    """Serializer pour l'historique des adhésions"""
    
    effectue_par_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = HistoriqueAdhesion
        fields = ['action', 'date_action', 'effectue_par', 'commentaires', 'effectue_par_nom']
    
    def get_effectue_par_nom(self, obj):
        """Retourne le nom de l'utilisateur qui a effectué l'action"""
        if obj.effectue_par:
            return f"{obj.effectue_par.first_name} {obj.effectue_par.last_name}".strip() or obj.effectue_par.username
        return "Système"

class AdhesionStatsSerializer(serializers.Serializer):
    """Serializer pour les statistiques des adhésions"""
    
    total_adhesions = serializers.IntegerField()
    adhesions_en_attente = serializers.IntegerField()
    adhesions_approuvees = serializers.IntegerField()
    adhesions_rejetees = serializers.IntegerField()
    adhesions_expirees = serializers.IntegerField()
    adhesions_valides = serializers.IntegerField()
    revenus_totaux = serializers.DecimalField(max_digits=12, decimal_places=2)
    adhesions_ce_mois = serializers.IntegerField()
    renouvellements_ce_mois = serializers.IntegerField()
