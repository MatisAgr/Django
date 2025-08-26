from django.core.management.base import BaseCommand
from core.models import Comment, Pizza
import random

class Command(BaseCommand):
    help = 'Crée des commentaires d\'exemple'

    def handle(self, *args, **options):
        # Supprimer les commentaires existants
        Comment.objects.all().delete()
        
        # Récupérer toutes les pizzas
        pizzas = list(Pizza.objects.all())
        if not pizzas:
            self.stdout.write(
                self.style.ERROR('Aucune pizza trouvée. Créez d\'abord des pizzas.')
            )
            return
        
        # Commentaires d'exemple
        commentaires = [
            {"auteur": "Marie Dupont", "texte": "Excellente pizza ! La pâte est parfaite et les ingrédients de qualité."},
            {"auteur": "Jean Martin", "texte": "Un peu trop salée à mon goût, mais globalement très bonne."},
            {"auteur": "Sophie Durand", "texte": "Ma pizza préférée de tout le quartier ! Je recommande vivement."},
            {"auteur": "Pierre Moreau", "texte": "Service rapide et pizza délicieuse. Rien à redire."},
            {"auteur": "Lucie Bernard", "texte": "Très bonne mais un peu chère pour la taille."},
            {"auteur": "Thomas Petit", "texte": "Pizza authentique avec des ingrédients frais. Top !"},
            {"auteur": "Emma Richard", "texte": "Correcte sans plus. J'ai connu mieux ailleurs."},
            {"auteur": "Nicolas Dubois", "texte": "La meilleure margherita de la ville, sans hésitation !"},
            {"auteur": "Julie Leroy", "texte": "Très généreuse en garniture, parfait pour les gros appétits."},
            {"auteur": "Alexandre Simon", "texte": "Pizza originale et savoureuse, bravo au chef !"},
        ]
        
        created_comments = []
        # Distribuer aléatoirement les commentaires sur les pizzas
        for pizza in pizzas:
            # Chaque pizza aura entre 0 et 3 commentaires
            nb_comments = random.randint(0, 3)
            selected_comments = random.sample(commentaires, min(nb_comments, len(commentaires)))
            
            for comment_data in selected_comments:
                comment = Comment.objects.create(
                    pizza=pizza,
                    auteur=comment_data["auteur"],
                    texte=comment_data["texte"]
                )
                created_comments.append(comment)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(created_comments)} comments')
        )
