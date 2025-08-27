# IA

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from bibliotheque.models import Auteur, Livre, Categorie, Article, Commentaire

class Command(BaseCommand):
    help = 'Crée des données d\'exemple pour l\'API bibliotheque et le mini-blog'

    def handle(self, *args, **options):
        # Suppression des données existantes
        Commentaire.objects.all().delete()
        Article.objects.all().delete()
        Livre.objects.all().delete()
        Auteur.objects.all().delete()
        Categorie.objects.all().delete()
        
        # Création des catégories
        categories_data = [
            'Technologie',
            'Science',
            'Littérature',
            'Histoire',
            'Art'
        ]
        
        categories = []
        for cat_name in categories_data:
            categorie = Categorie.objects.create(nom=cat_name)
            categories.append(categorie)
            self.stdout.write(
                self.style.SUCCESS(f'Catégorie créée : {categorie.nom}')
            )
        
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
        
        # Création des articles pour le mini-blog
        articles_data = [
            {
                'titre': 'Introduction à Django REST Framework',
                'contenu': '''Django REST Framework (DRF) est un toolkit puissant et flexible pour construire des API Web avec Django.
                
Il offre des fonctionnalités avancées comme :
- La sérialisation automatique des données
- Les ViewSets pour une gestion CRUD simplifiée
- L'authentification et les permissions
- La pagination automatique
- Une interface de navigation web pour tester les API

Ce framework est devenu un standard pour le développement d'APIs REST avec Python et Django.''',
                'categorie': categories[0]  # Technologie
            },
            {
                'titre': 'L\'architecture MVT de Django',
                'contenu': '''Django suit le pattern architectural MVT (Model-View-Template) :

**Modèles (Models)** : Définissent la structure des données et gèrent la base de données
**Vues (Views)** : Contiennent la logique métier et traitent les requêtes HTTP  
**Templates** : Gèrent l'affichage et la présentation des données

Cette architecture permet une séparation claire des responsabilités et facilite la maintenance du code.''',
                'categorie': categories[0]  # Technologie
            },
            {
                'titre': 'Les grands classiques de la littérature française',
                'contenu': '''La littérature française regorge d\'œuvres exceptionnelles :

- Les Misérables de Victor Hugo : une fresque sociale grandiose
- L\'Étranger d\'Albert Camus : une réflexion sur l\'absurdité de l\'existence
- Madame Bovary de Gustave Flaubert : un portrait du romantisme bourgeois
- À la recherche du temps perdu de Marcel Proust : une exploration de la mémoire

Ces œuvres continuent d\'influencer la littérature mondiale aujourd\'hui.''',
                'categorie': categories[2]  # Littérature
            },
            {
                'titre': 'L\'impact de la science sur la société moderne',
                'contenu': '''La science transforme continuellement notre société :

Les avancées en intelligence artificielle révolutionnent de nombreux secteurs, de la médecine à la finance.
Les technologies vertes offrent des solutions aux défis environnementaux.
La recherche médicale permet des traitements toujours plus efficaces.

Il est crucial de comprendre ces évolutions pour s\'adapter au monde de demain.''',
                'categorie': categories[1]  # Science
            },
            {
                'titre': 'L\'art numérique : nouvelle forme d\'expression',
                'contenu': '''L\'art numérique ouvre de nouveaux horizons créatifs :

- Les installations interactives immergent le spectateur
- La réalité virtuelle crée des expériences artistiques inédites
- Les NFT questionnent la propriété artistique
- L\'IA génère des œuvres originales

Cette révolution artistique redéfinit notre rapport à la création et à l\'art.''',
                'categorie': categories[4]  # Art
            }
        ]
        
        articles = []
        for article_data in articles_data:
            article = Article.objects.create(**article_data)
            articles.append(article)
            self.stdout.write(
                self.style.SUCCESS(f'Article créé : {article.titre}')
            )
        
        # Création de commentaires d'exemple
        commentaires_data = [
            {
                'article': articles[0],
                'nom': 'Jean Dupont',
                'contenu': 'Excellent article ! DRF m\'a vraiment simplifié le développement d\'API.'
            },
            {
                'article': articles[0], 
                'nom': 'Marie Martin',
                'contenu': 'Très utile pour comprendre les bases de DRF. Merci pour ce partage !'
            },
            {
                'article': articles[1],
                'nom': 'Pierre Durant',
                'contenu': 'L\'architecture MVT est effectivement très claire une fois qu\'on la comprend.'
            },
            {
                'article': articles[2],
                'nom': 'Sophie Moreau',
                'contenu': 'Ces classiques restent d\'actualité. J\'ajouterais Germinal à cette liste.'
            },
            {
                'article': articles[3],
                'nom': 'Paul Petit',
                'contenu': 'La science évolue si vite ! Il faut se former continuellement.'
            }
        ]
        
        for commentaire_data in commentaires_data:
            commentaire = Commentaire.objects.create(**commentaire_data)
            self.stdout.write(
                self.style.SUCCESS(f'Commentaire créé par {commentaire.nom}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('\n=== Données d\'exemple créées avec succès! ===')
        )
        self.stdout.write(
            self.style.WARNING('\n--- URLs disponibles ---')
        )
        self.stdout.write('MINI-BLOG (Chapitre 2) :')
        self.stdout.write('- /articles/ - Liste des articles avec pagination')
        self.stdout.write('- /articles/<id>/ - Détail d\'un article avec commentaires')
        self.stdout.write('- /articles/nouveau/ - Créer un nouvel article')
        self.stdout.write('- /now/ - Date et heure actuelles')
        self.stdout.write('\nAPI DRF (Chapitre 3) :')
        self.stdout.write('- /api/auteurs/ - Liste des auteurs')
        self.stdout.write('- /api/auteurs/?year=1900 - Auteurs nés après 1900')
        self.stdout.write('- /api/auteurs/<id>/titres/ - Titres des livres d\'un auteur')
        self.stdout.write('- /api/livres/ - Liste des livres')
        self.stdout.write('\nADMINISTRATION :')
        self.stdout.write('- /admin/ - Interface d\'administration Django')
