from django.contrib import admin
from .models import Auteur, Livre

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
