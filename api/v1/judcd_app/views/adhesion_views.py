from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from judcd_app.adhesion_models import Adhesion, HistoriqueAdhesion
from judcd_app.adhesion_serializers import (
    AdhesionCreateSerializer, AdhesionListSerializer, 
    AdhesionDetailSerializer, AdhesionActionSerializer,
    HistoriqueAdhesionSerializer, AdhesionStatsSerializer
)
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def creer_adhesion(request):
    """Créer une nouvelle demande d'adhésion"""
    serializer = AdhesionCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        adhesion = serializer.save()
        
        # Créer l'historique
        HistoriqueAdhesion.objects.create(
            adhesion=adhesion,
            action='CREATION',
            commentaires="Demande d'adhésion soumise automatiquement"
        )
        
        # Envoyer l'email de confirmation
        try:
            envoyer_email_confirmation(adhesion)
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email de confirmation: {e}")
        
        return Response({
            'success': True,
            'message': 'Votre demande d\'adhésion a été soumise avec succès. Vous recevrez un email de confirmation.',
            'data': AdhesionListSerializer(adhesion).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'error': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def lister_adhesions(request):
    """Lister toutes les adhésions (admin)"""
    statut = request.GET.get('statut', None)
    
    adhesions = Adhesion.objects.all()
    
    if statut:
        adhesions = adhesions.filter(statut=statut)
    
    serializer = AdhesionListSerializer(adhesions, many=True)
    return Response({
        'success': True,
        'data': serializer.data
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def detail_adhesion(request, adhesion_id):
    """Détails d'une adhésion (admin)"""
    try:
        adhesion = Adhesion.objects.get(id=adhesion_id)
        serializer = AdhesionDetailSerializer(adhesion)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Adhesion.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Adhésion non trouvée'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def action_adhesion(request, adhesion_id):
    """Effectuer une action sur une adhésion (approuver/rejeter/renouveler)"""
    try:
        adhesion = Adhesion.objects.get(id=adhesion_id)
        serializer = AdhesionActionSerializer(adhesion, data=request.data)
        
        if serializer.is_valid():
            action = serializer.validated_data['action']
            commentaires = serializer.validated_data.get('commentaires', '')
            
            # Traiter l'action
            if action == 'APPROUVER':
                approuver_adhesion(adhesion, request.user, commentaires)
            elif action == 'REJETER':
                rejeter_adhesion(adhesion, request.user, commentaires)
            elif action == 'RENOUVELER':
                renouveler_adhesion(adhesion, request.user, commentaires)
            
            return Response({
                'success': True,
                'message': f'Action "{action}" effectuée avec succès',
                'data': AdhesionDetailSerializer(adhesion).data
            })
        
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Adhesion.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Adhésion non trouvée'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def statistiques_adhesions(request):
    """Statistiques des adhésions (admin)"""
    from django.db.models import Count, Sum
    from datetime import datetime, timedelta
    
    total_adhesions = Adhesion.objects.count()
    adhesions_en_attente = Adhesion.objects.filter(statut='EN_ATTENTE').count()
    adhesions_approuvees = Adhesion.objects.filter(statut='APPROUVEE').count()
    adhesions_rejetees = Adhesion.objects.filter(statut='REJETEE').count()
    adhesions_expirees = Adhesion.objects.filter(statut='EXPIREE').count()
    
    # Adhésions valides (non expirées)
    adhesions_valides = Adhesion.objects.filter(
        statut='APPROUVEE',
        date_expiration__gt=timezone.now()
    ).count()
    
    # Revenus totaux
    revenus_totaux = Adhesion.objects.filter(
        statut='APPROUVEE'
    ).aggregate(total=Sum('montant_paye'))['total'] or 0
    
    # Ce mois-ci
    debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    adhesions_ce_mois = Adhesion.objects.filter(date_demande__gte=debut_mois).count()
    renouvellements_ce_mois = Adhesion.objects.filter(
        historique__action='RENOUVELLEMENT',
        historique__date_action__gte=debut_mois
    ).distinct().count()
    
    stats = {
        'total_adhesions': total_adhesions,
        'adhesions_en_attente': adhesions_en_attente,
        'adhesions_approuvees': adhesions_approuvees,
        'adhesions_rejetees': adhesions_rejetees,
        'adhesions_expirees': adhesions_expirees,
        'adhesions_valides': adhesions_valides,
        'revenus_totaux': revenus_totaux,
        'adhesions_ce_mois': adhesions_ce_mois,
        'renouvellements_ce_mois': renouvellements_ce_mois
    }
    
    serializer = AdhesionStatsSerializer(stats)
    return Response({
        'success': True,
        'data': serializer.data
    })

def approuver_adhesion(adhesion, utilisateur, commentaires):
    """Approuver une adhésion"""
    adhesion.statut = 'APPROUVEE'
    adhesion.date_approbation = timezone.now()
    adhesion.date_expiration = timezone.now() + timezone.timedelta(days=365)
    adhesion.traite_par = utilisateur
    adhesion.commentaires_admin = commentaires
    adhesion.save()
    
    # Créer l'historique
    HistoriqueAdhesion.objects.create(
        adhesion=adhesion,
        action='APPROBATION',
        effectue_par=utilisateur,
        commentaires=commentaires
    )
    
    # Envoyer l'email d'approbation
    try:
        envoyer_email_approbation(adhesion)
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email d'approbation: {e}")

def rejeter_adhesion(adhesion, utilisateur, commentaires):
    """Rejeter une adhésion"""
    adhesion.statut = 'REJETEE'
    adhesion.traite_par = utilisateur
    adhesion.commentaires_admin = commentaires
    adhesion.save()
    
    # Créer l'historique
    HistoriqueAdhesion.objects.create(
        adhesion=adhesion,
        action='REJET',
        effectue_par=utilisateur,
        commentaires=commentaires
    )
    
    # Envoyer l'email de rejet
    try:
        envoyer_email_rejet(adhesion)
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email de rejet: {e}")

def renouveler_adhesion(adhesion, utilisateur, commentaires):
    """Renouveler une adhésion"""
    ancienne_expiration = adhesion.date_expiration
    adhesion.date_expiration = timezone.now() + timezone.timedelta(days=365)
    adhesion.traite_par = utilisateur
    adhesion.save()
    
    # Créer l'historique
    HistoriqueAdhesion.objects.create(
        adhesion=adhesion,
        action='RENOUVELLEMENT',
        effectue_par=utilisateur,
        commentaires=f"Renouvellement. Ancienne expiration: {ancienne_expiration}. {commentaires}"
    )
    
    # Envoyer l'email de renouvellement
    try:
        envoyer_email_renouvellement(adhesion)
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email de renouvellement: {e}")

def envoyer_email_confirmation(adhesion):
    """Envoyer l'email de confirmation de demande"""
    sujet = f"JUDCD - Confirmation de votre demande d'adhésion"
    
    context = {
        'adhesion': adhesion,
        'association': {
            'nom': 'JUDCD',
            'email': 'contact@judcd.tg',
            'telephone': '+228 00 00 00 00',
            'adresse': 'Lomé, Togo'
        }
    }
    
    message_html = render_to_string('emails/confirmation_adhesion.html', context)
    message_text = render_to_string('emails/confirmation_adhesion.txt', context)
    
    send_mail(
        sujet,
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        [adhesion.email],
        html_message=message_html,
        fail_silently=False
    )

def envoyer_email_approbation(adhesion):
    """Envoyer l'email d'approbation"""
    sujet = f"JUDCD - Votre adhésion a été approuvée !"
    
    context = {
        'adhesion': adhesion,
        'association': {
            'nom': 'JUDCD',
            'email': 'contact@judcd.tg',
            'telephone': '+228 00 00 00 00',
            'adresse': 'Lomé, Togo'
        }
    }
    
    message_html = render_to_string('emails/approbation_adhesion.html', context)
    message_text = render_to_string('emails/approbation_adhesion.txt', context)
    
    send_mail(
        sujet,
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        [adhesion.email],
        html_message=message_html,
        fail_silently=False
    )

def envoyer_email_rejet(adhesion):
    """Envoyer l'email de rejet"""
    sujet = f"JUDCD - Information concernant votre demande d'adhésion"
    
    context = {
        'adhesion': adhesion,
        'association': {
            'nom': 'JUDCD',
            'email': 'contact@judcd.tg',
            'telephone': '+228 00 00 00 00',
            'adresse': 'Lomé, Togo'
        }
    }
    
    message_html = render_to_string('emails/rejet_adhesion.html', context)
    message_text = render_to_string('emails/rejet_adhesion.txt', context)
    
    send_mail(
        sujet,
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        [adhesion.email],
        html_message=message_html,
        fail_silently=False
    )

def envoyer_email_renouvellement(adhesion):
    """Envoyer l'email de renouvellement"""
    sujet = f"JUDCD - Votre adhésion a été renouvelée !"
    
    context = {
        'adhesion': adhesion,
        'association': {
            'nom': 'JUDCD',
            'email': 'contact@judcd.tg',
            'telephone': '+228 00 00 00 00',
            'adresse': 'Lomé, Togo'
        }
    }
    
    message_html = render_to_string('emails/renouvellement_adhesion.html', context)
    message_text = render_to_string('emails/renouvellement_adhesion.txt', context)
    
    send_mail(
        sujet,
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        [adhesion.email],
        html_message=message_html,
        fail_silently=False
    )
