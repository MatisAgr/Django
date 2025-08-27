from django.db import models
from django.urls import reverse

class Categorie(models.Model):
    nom = models.CharField(max_length=50, verbose_name="Nom") #50 car c'est dans l'énoncé (Chap2 2.E)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

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

class Article(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    contenu = models.TextField(verbose_name="Contenu")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name="Catégorie"
    )
    
    def __str__(self):
        return self.titre
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date']

class Commentaire(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='commentaires',
        verbose_name="Article"
    )
    nom = models.CharField(max_length=100, verbose_name="Nom")
    contenu = models.TextField(verbose_name="Commentaire")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    
    def __str__(self):
        return f"Commentaire de {self.nom} sur {self.article.titre}"
    
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-date']
