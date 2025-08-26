from django.core.management.base import BaseCommand
from gestion.models import Livre, Personne

class Command(BaseCommand):
    help = 'Crée des données d\'exemple pour la bibliothèque'

    def handle(self, *args, **options):
        # Suppression des données existantes
        Personne.objects.all().delete()
        Livre.objects.all().delete()
        
        # Création des livres
        livres_data = [
            {
                'titre': 'Le Petit Prince',
                'auteur': 'Antoine de Saint-Exupéry',
                'theme': 'Fiction',
                'note': 5
            },
            {
                'titre': 'Les Misérables',
                'auteur': 'Victor Hugo',
                'theme': 'Classique',
                'note': 4
            },
            {
                'titre': '1984',
                'auteur': 'George Orwell',
                'theme': 'Science-Fiction',
                'note': 5
            }
        ]
        
        livres = []
        for livre_data in livres_data:
            livre = Livre.objects.create(**livre_data)
            livres.append(livre)
            self.stdout.write(
                self.style.SUCCESS(f'Livre créé : {livre.titre}')
            )
        
        # Création des personnes
        personnes_data = [
            {
                'nom': 'Dupont',
                'prenom': 'Jean',
                'age': 25,
                'lieu_residence': 'Montreuil'
            },
            {
                'nom': 'Martin',
                'prenom': 'Marie',
                'age': 30,
                'lieu_residence': 'Montreuil'
            },
            {
                'nom': 'Bernard',
                'prenom': 'Pierre',
                'age': 16,  # Mineur
                'lieu_residence': 'Montreuil'
            },
            {
                'nom': 'Petit',
                'prenom': 'Sophie',
                'age': 28,
                'lieu_residence': 'Paris'  # Pas Montreuil
            },
            {
                'nom': 'Durand',
                'prenom': 'Paul',
                'age': 15,  # Mineur
                'lieu_residence': 'Vincennes'  # Pas Montreuil
            }
        ]
        
        for personne_data in personnes_data:
            personne = Personne.objects.create(**personne_data)
            self.stdout.write(
                self.style.SUCCESS(f'Personne créée : {personne.prenom} {personne.nom}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Données d\'exemple créées avec succès!')
        )
        self.stdout.write(
            self.style.WARNING('Note: Les personnes mineures et celles ne résidant pas à Montreuil ne pourront pas emprunter de livres.')
        )
