# IA

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from bibliotheque.models import Auteur, Livre

class Command(BaseCommand):
    help = 'Crée des données d\'exemple pour l\'API bibliotheque'

    def handle(self, *args, **options):
        # Suppression des données existantes
        Livre.objects.all().delete()
        Auteur.objects.all().delete()
        
        # Création des auteurs
        auteurs_data = [
            {
                'nom': 'Victor Hugo',
                'date_naissance': date(1802, 2, 26)
            },
            {
                'nom': 'George Orwell',
                'date_naissance': date(1903, 6, 25)
            },
            {
                'nom': 'J.K. Rowling',
                'date_naissance': date(1965, 7, 31)
            },
            {
                'nom': 'Albert Camus',
                'date_naissance': date(1913, 11, 7)
            },
            {
                'nom': 'Agatha Christie',
                'date_naissance': date(1890, 9, 15)
            }
        ]
        
        auteurs = []
        for auteur_data in auteurs_data:
            auteur = Auteur.objects.create(**auteur_data)
            auteurs.append(auteur)
            self.stdout.write(
                self.style.SUCCESS(f'Auteur créé : {auteur.nom}')
            )
        
        # Création des livres
        livres_data = [
            {
                'titre': 'Les Misérables',
                'date_sortie': date(1862, 3, 30),
                'auteur': auteurs[0]  # Victor Hugo
            },
            {
                'titre': 'Notre-Dame de Paris',
                'date_sortie': date(1831, 1, 14),
                'auteur': auteurs[0]  # Victor Hugo
            },
            {
                'titre': '1984',
                'date_sortie': date(1949, 6, 8),
                'auteur': auteurs[1]  # George Orwell
            },
            {
                'titre': 'La Ferme des animaux',
                'date_sortie': date(1945, 8, 17),
                'auteur': auteurs[1]  # George Orwell
            },
            {
                'titre': 'Harry Potter à l\'école des sorciers',
                'date_sortie': date(1997, 6, 26),
                'auteur': auteurs[2]  # J.K. Rowling
            },
            {
                'titre': 'Harry Potter et la Chambre des secrets',
                'date_sortie': date(1998, 7, 2),
                'auteur': auteurs[2]  # J.K. Rowling
            },
            {
                'titre': 'L\'Étranger',
                'date_sortie': date(1942, 5, 19),
                'auteur': auteurs[3]  # Albert Camus
            },
            {
                'titre': 'Le Meurtre de Roger Ackroyd',
                'date_sortie': date(1926, 6, 1),
                'auteur': auteurs[4]  # Agatha Christie
            }
        ]
        
        for livre_data in livres_data:
            livre = Livre.objects.create(**livre_data)
            self.stdout.write(
                self.style.SUCCESS(f'Livre créé : {livre.titre}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Données d\'exemple créées avec succès!')
        )
        self.stdout.write(
            self.style.WARNING('URLs disponibles:')
        )
        self.stdout.write('- /api/auteurs/ - Liste des auteurs')
        self.stdout.write('- /api/auteurs/?year=1900 - Auteurs nés après 1900')
        self.stdout.write('- /api/auteurs/{id}/titres/ - Titres des livres d\'un auteur')
        self.stdout.write('- /api/livres/ - Liste des livres')
