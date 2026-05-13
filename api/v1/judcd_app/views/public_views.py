from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from judcd_app.models import *

# ==========================================
# VUES PUBLIQUES JUDCD - ACCES SANS AUTHENTIFICATION
# ==========================================

@api_view(['GET'])
@permission_classes([AllowAny])
def public_partenaires(request):
    """Récupérer tous les partenaires publiquement"""
    partenaires = Partenaire.objects.select_related('type_partenaire').all()
    data = []
    for partenaire in partenaires:
        data.append({
            'id': partenaire.id,
            'nom': partenaire.nom,
            'description': partenaire.description,
            'logo': partenaire.logo.url if partenaire.logo else None,
            'type_partenaire': partenaire.type_partenaire.nom,
            'lien': partenaire.lien
        })
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_team(request):
    """Récupérer tous les membres de l'équipe publiquement"""
    members = Membre_Equipe.objects.all()
    data = []
    for member in members:
        data.append({
            'id': member.id,
            'nom_complet': member.nom_complet,
            'role': member.role,
            'photo': member.photo.url if member.photo else None,
            'telephone': member.telephone,
            'email': member.email,
            'reseaux_sociaux': member.reseaux_sociaux or {},
            'infos': member.infos
        })
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_actions(request):
    """Récupérer toutes les actions publiquement"""
    actions = Action.objects.select_related('type_action').prefetch_related('galerie').all()
    data = []
    for action in actions:
        galerie_images = [img.image.url for img in action.galerie.all() if img.image]
        data.append({
            'id': action.id,
            'titre': action.titre,
            'description': action.description,
            'date': action.date,
            'lieu': action.lieu,
            'type_action': action.type_action.nom,
            'image_couverture': action.image_couverture.url if action.image_couverture else None,
            'galerie': galerie_images
        })
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_temoignages(request):
    """Récupérer tous les témoignages publiquement"""
    temoignages = Temoignage.objects.all().order_by('-date')
    data = []
    for temoignage in temoignages:
        data.append({
            'id': temoignage.id,
            'nom': temoignage.nom,
            'titre': temoignage.titre,
            'message': temoignage.message,
            'photo': temoignage.photo.url if temoignage.photo else None,
            'date': temoignage.date
        })
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_types_actions(request):
    """Récupérer les types d'actions publiquement"""
    types = Type_Action.objects.all()
    data = [{'id': t.id, 'nom': t.nom} for t in types]
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_types_partenaires(request):
    """Récupérer les types de partenaires publiquement"""
    types = Type_Partenaire.objects.all()
    data = [{'id': t.id, 'nom': t.nom} for t in types]
    return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def public_contact(request):
    """Envoyer un message de contact publiquement"""
    try:
        contact = Contact.objects.create(
            name=request.data.get('name'),
            email=request.data.get('email'),
            telephone=request.data.get('telephone'),
            sujet=request.data.get('sujet'),
            message=request.data.get('message')
        )
        return Response({
            'success': True,
            'message': 'Message envoyé avec succès'
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def public_newsletter(request):
    """S'inscrire à la newsletter publiquement"""
    try:
        email = request.data.get('email')
        if not email:
            return Response({
                'success': False,
                'error': 'Email requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        newsletter, created = Newsletter.objects.get_or_create(
            email=email,
            defaults={'email': email}
        )
        
        if created:
            return Response({
                'success': True,
                'message': 'Inscription réussie à la newsletter'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'error': 'Email déjà inscrit'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def public_donation(request):
    """Faire un don publiquement"""
    try:
        don = Don.objects.create(
            nom=request.data.get('nom'),
            email=request.data.get('email'),
            montant=request.data.get('montant'),
            message=request.data.get('message', ''),
            moyen_paiement=request.data.get('moyen_paiement'),
            numero_transaction=request.data.get('numero_transaction')
        )
        return Response({
            'success': True,
            'message': 'Don enregistré avec succès',
            'don_id': don.id
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def public_temoignage(request):
    """Ajouter un témoignage publiquement"""
    try:
        temoignage = Temoignage.objects.create(
            nom=request.data.get('nom'),
            titre=request.data.get('titre'),
            message=request.data.get('message')
        )
        return Response({
            'success': True,
            'message': 'Témoignage ajouté avec succès',
            'temoignage_id': temoignage.id
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_galerie_action(request):
    """Récupérer toutes les images de la galerie publiquement avec pagination"""
    try:
        # Paramètres de pagination
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 12))
        category = request.GET.get('category', None)
        
        # Filtrage par catégorie si fourni
        queryset = Galerie_Action.objects.all()
        if category:
            queryset = queryset.filter(category__icontains=category)
        
        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        total_count = queryset.count()
        
        galerie_items = queryset[start:end]
        data = []
        for item in galerie_items:
            data.append({
                'id': item.id,
                'image': item.image.url if item.image else None,
                'category': item.category if hasattr(item, 'category') else None,
                'title': item.title if hasattr(item, 'title') else None,
                'description': item.description if hasattr(item, 'description') else None,
                'created_at': item.created_at.isoformat() if hasattr(item, 'created_at') else None
            })
        
        return Response({
            'count': total_count,
            'next': f"/api/v1/public/galerie-action/?page={page + 1}&page_size={page_size}" if end < total_count else None,
            'previous': f"/api/v1/public/galerie-action/?page={page - 1}&page_size={page_size}" if page > 1 else None,
            'results': data,
            'total_pages': (total_count + page_size - 1) // page_size
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_stats(request):
    """Récupérer les statistiques publiques"""
    try:
        stats = {
            'total_partenaires': Partenaire.objects.count(),
            'total_actions': Action.objects.count(),
            'total_temoignages': Temoignage.objects.count(),
            'total_team_members': Membre_Equipe.objects.count(),
            'total_donations': Don.objects.count(),
            'total_donations_amount': Don.objects.aggregate(
                total=models.Sum('montant')
            )['total'] or 0
        }
        return Response(stats)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
