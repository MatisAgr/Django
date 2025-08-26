# IA

from django.core.management.base import BaseCommand
from core.models import Pizza
from decimal import Decimal
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta

class Command(BaseCommand):
    help = 'Crée des pizzas d\'exemple avec des dates et des slugs variés'

    def handle(self, *args, **options):
        # Supprimer les pizzas existantes
        Pizza.objects.all().delete()
        
        # Créer des pizzas d'exemple avec des dates variées
        now = timezone.now()
        
        pizzas = [
            {"title": "Margherita", "prix": Decimal("12.50"), "disponible": True, "created_at": now - timedelta(days=5)},
            {"title": "Pepperoni", "prix": Decimal("14.00"), "disponible": True, "created_at": now - timedelta(days=4)},
            {"title": "Quatre Fromages", "prix": Decimal("15.50"), "disponible": False, "created_at": now - timedelta(days=3)},
            {"title": "Napolitaine", "prix": Decimal("13.75"), "disponible": True, "created_at": now - timedelta(days=2)},
            {"title": "Calzone", "prix": Decimal("16.00"), "disponible": True, "created_at": now - timedelta(days=1)},
            {"title": "Végétarienne", "prix": Decimal("13.25"), "disponible": False, "created_at": now},
            {"title": "Chorizo", "prix": Decimal("14.75"), "disponible": True, "created_at": now},
            {"title": "Fruits de Mer", "prix": Decimal("18.50"), "disponible": True, "created_at": now - timedelta(hours=2)},
        ]
        
        for pizza_data in pizzas:
            # Générer un slug unique
            base_slug = slugify(pizza_data["title"])
            slug = base_slug
            counter = 1
            while Pizza.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            pizza = Pizza(
                title=pizza_data["title"],
                slug=slug,
                prix=pizza_data["prix"],
                disponible=pizza_data["disponible"]
            )
            pizza.save()
            # Mettre à jour la date de création manuellement
            Pizza.objects.filter(pk=pizza.pk).update(created_at=pizza_data["created_at"])
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(pizzas)} pizzas with varied dates and unique slugs')
        )
