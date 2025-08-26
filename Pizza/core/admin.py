from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Pizza, Ingredient, Comment

# Register your models here.

# Inline pour les commentaires
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Nombre de formulaires vides à afficher
    fields = ('auteur', 'texte')
    readonly_fields = ('created_at',)

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    # 3 colonnes pertinentes dans la liste + colonne calculée + nb commentaires
    list_display = ('title', 'slug', 'prix', 'disponible', 'is_recent', 'nb_comments', 'created_at')
    
    # Champs de recherche
    search_fields = ('title', 'slug', 'prix')
    
    # Filtres latéraux
    list_filter = ('disponible', 'created_at', 'prix')
    
    # Champs éditables directement dans la liste
    list_editable = ('disponible',)
    
    # Colonnes cliquables (liens vers la page de détail)
    list_display_links = ('title', 'slug')
    
    # Tri par défaut (sera surchargé par le Meta.ordering du modèle)
    ordering = ('-created_at', 'title')
    
    # Hiérarchie par date pour navigation temporelle
    date_hierarchy = 'created_at'
    
    # Nombre d'éléments par page
    list_per_page = 20
    
    # Prépopulation du slug depuis le title
    prepopulated_fields = {"slug": ("title",)}
    
    # Champs en lecture seule
    readonly_fields = ('created_at', 'updated_at')
    
    # Gestion des ingrédients avec interface horizontale
    filter_horizontal = ('ingredients',)
    
    # Inclusion des commentaires en inline
    inlines = [CommentInline]
    
    # Organisation du formulaire en sections
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'slug', 'prix')
        }),
        ('Disponibilité', {
            'fields': ('disponible',),
            'description': 'Statut de disponibilité de la pizza'
        }),
        ('Ingrédients', {
            'fields': ('ingredients',),
            'description': 'Sélectionnez les ingrédients de cette pizza'
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Section repliable
            'description': 'Informations automatiques sur les dates'
        }),
    )
    
    # Méthode calculée pour déterminer si la pizza est récente (≤ 7 jours)
    @admin.display(boolean=True, ordering='created_at', description='Récente ?')
    def is_recent(self, obj):
        """Retourne True si la pizza a été créée il y a 7 jours ou moins"""
        if obj.created_at:
            return timezone.now() - obj.created_at <= timedelta(days=7)
        return False
    
    # Méthode calculée pour afficher le nombre de commentaires
    @admin.display(ordering='comments__count', description='Nb commentaires')
    def nb_comments(self, obj):
        """Retourne le nombre de commentaires pour cette pizza"""
        return obj.comments.count()
    
    # Optimisation des requêtes pour éviter le problème N+1
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('comments')
    
    # Actions personnalisées avec décorateurs @admin.action
    actions = ['mark_as_available', 'mark_as_unavailable']
    
    @admin.action(description='Marquer comme disponible')
    def mark_as_available(self, request, queryset):
        """Marque les pizzas sélectionnées comme disponibles"""
        updated = queryset.update(disponible=True)
        self.message_user(
            request, 
            f'{updated} pizza{"s" if updated > 1 else ""} marquée{"s" if updated > 1 else ""} comme disponible{"s" if updated > 1 else ""}.',
            level='success'
        )
    
    @admin.action(description='Marquer comme indisponible')
    def mark_as_unavailable(self, request, queryset):
        """Marque les pizzas sélectionnées comme indisponibles"""
        updated = queryset.update(disponible=False)
        self.message_user(
            request, 
            f'{updated} pizza{"s" if updated > 1 else ""} marquée{"s" if updated > 1 else ""} comme indisponible{"s" if updated > 1 else ""}.',
            level='warning'
        )

# Administration pour les ingrédients
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'allergens')
    search_fields = ('name', 'allergens')
    list_filter = ('allergens',)
    ordering = ('name',)

# Administration pour les commentaires
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pizza', 'auteur', 'texte_resume', 'created_at')
    list_filter = ('created_at', 'pizza')
    search_fields = ('auteur', 'texte', 'pizza__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def texte_resume(self, obj):
        """Affiche un résumé du commentaire"""
        return obj.texte[:50] + "..." if len(obj.texte) > 50 else obj.texte
    texte_resume.short_description = 'Commentaire'
