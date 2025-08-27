from django.db import models

class Auteur(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Auteur"
        verbose_name_plural = "Auteurs"

class Livre(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    date_sortie = models.DateField(verbose_name="Date de sortie")
    auteur = models.ForeignKey(
        Auteur,
        on_delete=models.CASCADE,
        related_name='livres',
        verbose_name="Auteur"
    )
    
    def __str__(self):
        return f"{self.titre} - {self.auteur.nom}"
    
    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
