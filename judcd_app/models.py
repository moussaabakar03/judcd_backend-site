from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    sujet = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    
class Type_Partenaire(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Partenaire(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='partenaires/')
    type_partenaire = models.ForeignKey(Type_Partenaire, on_delete=models.CASCADE)
    lien = models.URLField()

    def __str__(self):
        return self.nom
    
class Don(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    moyen_paiement = models.CharField(max_length=50)
    numero_transaction = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} - {self.montant}"
    

class Temoignage(models.Model):
    nom = models.CharField(max_length=100)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    photo = models.ImageField(upload_to='temoignages/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.date}"
    

class Membre_Equipe(models.Model):
    nom_complet = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='equipe/', blank=True, null=True)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    reseaux_sociaux = models.JSONField()  # Ex: {"linkedin": "url", "twitter": "url"}
    infos = models.TextField()

    def __str__(self):
        return f"{self.nom_complet} - {self.role}"
    

    
class Type_Action(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Galerie_Action(models.Model):
    image = models.ImageField(upload_to='galerie/', blank=True, null=True)

    def __str__(self):
        return f"Image {self.id}"

class Action(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    lieu = models.CharField(max_length=200)
    type_action = models.ForeignKey(Type_Action, on_delete=models.CASCADE)
    image_couverture = models.ImageField(upload_to='actions/', blank=True, null=True)
    galerie = models.ManyToManyField(Galerie_Action, blank=True)


    def __str__(self):
        return self.titre


class Type_Actualite(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Actualite(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    type_actualite = models.ForeignKey(Type_Actualite, on_delete=models.CASCADE)
    image_couverture = models.ImageField(upload_to='actualites/')

    def __str__(self):
        return self.titre

