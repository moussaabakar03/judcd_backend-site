import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from judcd_app.auth_serializers import (
    LoginSerializer, RefreshTokenSerializer, LoginResponseSerializer, UserSerializer
)


# Secret key pour JWT (devrait être dans settings)
JWT_SECRET = getattr(settings, 'SECRET_KEY', 'django-insecure-default')
JWT_ALGORITHM = 'HS256'
JWT_ACCESS_TOKEN_LIFETIME = timedelta(minutes=60)
JWT_REFRESH_TOKEN_LIFETIME = timedelta(days=1)


def generate_tokens(user):
    """Génère les tokens d'accès et de refresh"""
    now = datetime.utcnow()
    
    access_payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': now + JWT_ACCESS_TOKEN_LIFETIME,
        'iat': now,
        'type': 'access'
    }
    
    refresh_payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': now + JWT_REFRESH_TOKEN_LIFETIME,
        'iat': now,
        'type': 'refresh'
    }
    
    access_token = jwt.encode(access_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return {
        'access': access_token,
        'refresh': refresh_token,
        'access_lifetime': JWT_ACCESS_TOKEN_LIFETIME.total_seconds(),
        'refresh_lifetime': JWT_REFRESH_TOKEN_LIFETIME.total_seconds()
    }


@swagger_auto_schema(
    method='POST',
    request_body=LoginSerializer,
    responses={
        200: LoginResponseSerializer,
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "error": "Username and password are required"
                }
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                    "error": "Invalid credentials"
                }
            }
        )
    },
    operation_description="Authentification utilisateur et génération des tokens JWT",
    operation_id="auth_login"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login(request):
    """Endpoint de login personnalisé"""
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'error': 'Username and password are required',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    user = authenticate(username=username, password=password)
    
    if user is not None and user.is_active:
        tokens = generate_tokens(user)
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        
        return Response({
            'access': tokens['access'],
            'refresh': tokens['refresh'],
            'user': user_data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    method='POST',
    request_body=RefreshTokenSerializer,
    responses={
        200: LoginResponseSerializer,
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "error": "Refresh token is required"
                }
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                    "error": "Refresh token has expired"
                }
            }
        )
    },
    operation_description="Rafraîchissement du token d'accès JWT",
    operation_id="auth_refresh"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def custom_refresh(request):
    """Endpoint de refresh token personnalisé"""
    serializer = RefreshTokenSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'error': 'Refresh token is required',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    refresh_token = serializer.validated_data['refresh']
    
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        if payload.get('type') != 'refresh':
            return Response({
                'error': 'Invalid token type'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        from django.contrib.auth.models import User
        user = User.objects.get(id=payload['user_id'])
        
        if not user.is_active:
            return Response({
                'error': 'User account is disabled'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Générer de nouveaux tokens
        tokens = generate_tokens(user)
        
        return Response({
            'access': tokens['access'],
            'refresh': tokens['refresh']
        }, status=status.HTTP_200_OK)
        
    except jwt.ExpiredSignatureError:
        return Response({
            'error': 'Refresh token has expired'
        }, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({
            'error': 'Invalid refresh token'
        }, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """Obtenir les informations de l'utilisateur connecté"""
    try:
        serializer = UserSerializer(request.user)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
