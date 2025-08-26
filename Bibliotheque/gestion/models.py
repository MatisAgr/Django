from django.db import models
from django.core.exceptions import ValidationError

class Livre(models.Model):
    theme = models.CharField(max_length=200, verbose_name="Thème")
    auteur = models.CharField(max_length=200, verbose_name="Auteur")
    titre = models.CharField(max_length=200, verbose_name="Titre")
    note = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)], 
        verbose_name="Note (1-5)"
    )
    disponibilite = models.BooleanField(default=True, verbose_name="Disponibilité")
    
    def __str__(self):
        return f"{self.titre} - {self.auteur}"
    
    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"

class Personne(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom")
    prenom = models.CharField(max_length=200, verbose_name="Prénom")
    age = models.IntegerField(verbose_name="Âge")
    lieu_residence = models.CharField(max_length=200, verbose_name="Lieu de résidence")
    # Relation OneToOneField pour qu'une personne ne puisse emprunter qu'un seul livre
    # et qu'un livre ne puisse être emprunté que par une seule personne
    livre_emprunte = models.OneToOneField(
        Livre, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Livre emprunté",
        related_name="emprunteur"
    )
    
    def clean(self):
        """Validation des règles métier"""
        super().clean()
        
        if self.livre_emprunte:
            # Règle 1: Une personne mineure ne peut pas emprunter de livre
            if self.age < 18:
                raise ValidationError("Une personne mineure ne peut pas emprunter de livre.")
            
            # Règle 2: Seules les personnes de Montreuil peuvent emprunter
            if self.lieu_residence.lower() != 'montreuil':
                raise ValidationError("Seules les personnes résidant à Montreuil peuvent emprunter des livres.")
            
            # Règle 3: On ne peut pas emprunter un livre déjà indisponible
            if not self.livre_emprunte.disponibilite:
                raise ValidationError("Ce livre n'est pas disponible à l'emprunt.")
    
    def save(self, *args, **kwargs):
        """Override save pour gérer la disponibilité automatique des livres"""
        # Si on assigne un livre à une personne, le marquer comme indisponible
        if self.livre_emprunte:
            # Validation des règles métier
            self.clean()
            # Marquer le livre comme indisponible
            self.livre_emprunte.disponibilite = False
            self.livre_emprunte.save()
        
        # Si on avait un livre précédemment et qu'on le retire, le marquer comme disponible
        if self.pk:  # Si l'objet existe déjà
            old_instance = Personne.objects.get(pk=self.pk)
            if old_instance.livre_emprunte and old_instance.livre_emprunte != self.livre_emprunte:
                old_instance.livre_emprunte.disponibilite = True
                old_instance.livre_emprunte.save()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    class Meta:
        verbose_name = "Personne"
        verbose_name_plural = "Personnes"
