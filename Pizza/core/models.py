from django.db import models
from django.utils import timezone

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de l'ingrédient")
    allergens = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Allergènes séparés par des virgules (ex: gluten, lactose, noix)",
        verbose_name="Allergènes"
    )
    
    def __str__(self):
        if self.allergens:
            return f"{self.name} (allergènes : {self.allergens})"
        return self.name
    
    class Meta:
        verbose_name = "Ingrédient"
        verbose_name_plural = "Ingrédients"
        ordering = ['name']

class Pizza(models.Model):
    title = models.CharField(max_length=100, verbose_name="Nom de la pizza")
    slug = models.SlugField(default="", null=True, blank=True, unique=True, verbose_name="URL slug")
    prix = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Prix")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    ingredients = models.ManyToManyField(
        Ingredient, 
        blank=True, 
        verbose_name="Ingrédients",
        help_text="Sélectionnez les ingrédients de cette pizza"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    def __str__(self):
        status = "Disponible" if self.disponible else "Non disponible"
        return f"{self.title} - {self.prix}€ ({status})"
    
    class Meta:
        verbose_name = "Pizza"
        verbose_name_plural = "Pizzas"
        ordering = ['-created_at']

class Comment(models.Model):
    pizza = models.ForeignKey(
        Pizza, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name="Pizza"
    )
    auteur = models.CharField(max_length=100, verbose_name="Auteur")
    texte = models.TextField(verbose_name="Commentaire")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    def __str__(self):
        return f"Commentaire de {self.auteur} sur {self.pizza.title}"
    
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_at']
