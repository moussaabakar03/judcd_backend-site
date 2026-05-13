from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Adhesion(models.Model):
    """Modèle pour les demandes d'adhésion"""
    
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente de validation'),
        ('APPROUVEE', 'Approuvée'),
        ('REJETEE', 'Rejetée'),
        ('EXPIREE', 'Expirée'),
    ]
    
    # Informations personnelles
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=100, verbose_name="Lieu de naissance")
    profession = models.CharField(max_length=100, verbose_name="Profession")
    adresse = models.TextField(verbose_name="Adresse")
    
    # Informations d'adhésion
    date_demande = models.DateTimeField(auto_now_add=True, verbose_name="Date de demande")
    date_approbation = models.DateTimeField(null=True, blank=True, verbose_name="Date d'approbation")
    date_expiration = models.DateTimeField(null=True, blank=True, verbose_name="Date d'expiration")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE', verbose_name="Statut")
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00, verbose_name="Montant payé")
    
    # Preuve de paiement
    capture_depot = models.ImageField(upload_to='adhesions/preuves/', verbose_name="Preuve de dépôt")
    reference_paiement = models.CharField(max_length=100, blank=True, verbose_name="Référence de paiement")
    
    # Informations supplémentaires
    motivations = models.TextField(verbose_name="Motivations pour adhérer")
    competences = models.TextField(blank=True, verbose_name="Compétences et expériences")
    disponibilites = models.TextField(blank=True, verbose_name="Disponibilités")
    
    # Suivi administratif
    traite_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Traité par")
    commentaires_admin = models.TextField(blank=True, verbose_name="Commentaires administrateur")
    
    class Meta:
        verbose_name = "Adhésion"
        verbose_name_plural = "Adhésions"
        ordering = ['-date_demande']
    
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.statut}"
    
    def est_valide(self):
        """Vérifie si l'adhésion est valide"""
        if self.statut != 'APPROUVEE' or not self.date_expiration:
            return False
        return timezone.now() <= self.date_expiration
    
    def jours_restants(self):
        """Calcule le nombre de jours restants avant expiration"""
        if not self.date_expiration:
            return 0
        delta = self.date_expiration - timezone.now()
        return max(0, delta.days)
    
    def renouveler(self):
        """Renouvelle l'adhésion pour 1 an"""
        self.date_expiration = timezone.now() + timezone.timedelta(days=365)
        self.save()

class HistoriqueAdhesion(models.Model):
    """Historique des actions sur les adhésions"""
    
    ACTION_CHOICES = [
        ('CREATION', 'Création de la demande'),
        ('APPROBATION', 'Approbation'),
        ('REJET', 'Rejet'),
        ('RENOUVELLEMENT', 'Renouvellement'),
        ('EXPIRATION', 'Expiration'),
    ]
    
    adhesion = models.ForeignKey(Adhesion, on_delete=models.CASCADE, related_name='historique')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    date_action = models.DateTimeField(auto_now_add=True)
    effectue_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    commentaires = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Historique d'adhésion"
        verbose_name_plural = "Historiques d'adhésions"
        ordering = ['-date_action']
    
    def __str__(self):
        return f"{self.adhesion} - {self.action} - {self.date_action}"
