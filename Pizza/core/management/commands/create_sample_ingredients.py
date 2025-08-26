from django.core.management.base import BaseCommand
from core.models import Ingredient

class Command(BaseCommand):
    help = 'Crée des ingrédients d\'exemple'

    def handle(self, *args, **options):
        # Supprimer les ingrédients existants
        Ingredient.objects.all().delete()
        
        # Créer des ingrédients d'exemple
        ingredients = [
            {"name": "Tomate", "allergens": ""},
            {"name": "Mozzarella", "allergens": "lactose"},
            {"name": "Basilic", "allergens": ""},
            {"name": "Pepperoni", "allergens": ""},
            {"name": "Champignons", "allergens": ""},
            {"name": "Olives", "allergens": ""},
            {"name": "Anchois", "allergens": "poisson"},
            {"name": "Fromage de chèvre", "allergens": "lactose"},
            {"name": "Jambon", "allergens": ""},
            {"name": "Roquette", "allergens": ""},
            {"name": "Parmesan", "allergens": "lactose"},
            {"name": "Pâte", "allergens": "gluten"},
            {"name": "Œuf", "allergens": "œuf"},
            {"name": "Chorizo", "allergens": ""},
            {"name": "Fruits de mer", "allergens": "fruits de mer, mollusques"},
        ]
        
        created_ingredients = []
        for ingredient_data in ingredients:
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_data["name"],
                defaults={'allergens': ingredient_data["allergens"]}
            )
            created_ingredients.append(ingredient)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(created_ingredients)} ingredients')
        )
