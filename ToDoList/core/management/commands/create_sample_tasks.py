# AI

from django.core.management.base import BaseCommand
from core.models import Task

class Command(BaseCommand):
    help = 'Crée des tâches d\'exemple pour la démonstration'

    def handle(self, *args, **options):
        # Supprimer les tâches existantes pour éviter les doublons
        Task.objects.all().delete()
        
        # Créer des tâches d'exemple
        tasks = [
            {"title": "task 1", "completed": True},
            {"title": "task 2", "completed": True},
            {"title": "task 3", "completed": True},
            {"title": "task 4", "completed": True},
            {"title": "task 5", "completed": False},
            {"title": "task 6", "completed": False},
            {"title": "task 7", "completed": False},
            {"title": "task 8", "completed": False},
            {"title": "task 9", "completed": False},
            {"title": "task 10", "completed": False},
            {"title": "task 11", "completed": False},
            {"title": "task 12", "completed": True},
            {"title": "task 13", "completed": False},
        ]
        
        created_count = 0
        for task_data in tasks:
            Task.objects.create(**task_data)
            created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'{created_count} tâches créées'
            )
        )
