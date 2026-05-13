from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Crée automatiquement un superutilisateur depuis les variables d\'environnement'

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not username or not email or not password:
            self.stdout.write(
                self.style.ERROR('Les variables d\'environnement DJANGO_SUPERUSER_USERNAME, '
                                'DJANGO_SUPERUSER_EMAIL et DJANGO_SUPERUSER_PASSWORD sont requises')
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'L\'utilisateur "{username}" existe déjà')
            )
            return

        try:
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f'Superutilisateur "{username}" créé avec succès')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur lors de la création du superutilisateur: {e}')
            )
