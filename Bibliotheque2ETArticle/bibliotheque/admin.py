from django.contrib import admin
from .models import Auteur, Livre, Categorie, Article, Commentaire

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_naissance')
    list_filter = ('date_naissance',)
    search_fields = ('nom',)

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_sortie')
    list_filter = ('date_sortie', 'auteur')
    search_fields = ('titre', 'auteur__nom')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'date')
    list_filter = ('categorie', 'date')
    search_fields = ('titre', 'contenu')
    date_hierarchy = 'date'

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'article', 'date')
    list_filter = ('date', 'article')
    search_fields = ('nom', 'contenu', 'article__titre')
