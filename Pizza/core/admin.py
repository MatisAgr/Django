from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Pizza, Ingredient, Comment

# inline commentaires
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('auteur', 'texte')
    readonly_fields = ('created_at',)

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    # colonnes liste + calculées
    list_display = ('title', 'slug', 'prix', 'disponible', 'is_recent', 'nb_comments', 'created_at')
    
    # recherche
    search_fields = ('title', 'slug', 'prix')
    
    # filtres
    list_filter = ('disponible', 'created_at', 'prix')
    
    # édition directe
    list_editable = ('disponible',)
    
    # liens cliquables
    list_display_links = ('title', 'slug')
    
    # tri défaut
    ordering = ('-created_at', 'title')
    
    # hiérarchie dates
    date_hierarchy = 'created_at'
    
    # pagination
    list_per_page = 20
    
    # slug auto
    prepopulated_fields = {"slug": ("title",)}
    
    # lecture seule
    readonly_fields = ('created_at', 'updated_at')
    
    # interface horizontale ingrédients
    filter_horizontal = ('ingredients',)
    
    # commentaires inline
    inlines = [CommentInline]
    
    # sections formulaire
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'slug', 'prix')
        }),
        ('Disponibilité', {
            'fields': ('disponible',),
            'description': 'statut disponibilité'
        }),
        ('Ingrédients', {
            'fields': ('ingredients',),
            'description': 'ingrédients pizza'
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'dates auto'
        }),
    )
    
    # colonne récente ≤ 7j
    @admin.display(boolean=True, ordering='created_at', description='récente ?')
    def is_recent(self, obj):
        if obj.created_at:
            return timezone.now() - obj.created_at <= timedelta(days=7)
        return False
    
    # nb commentaires
    @admin.display(ordering='comments__count', description='nb commentaires')
    def nb_comments(self, obj):
        return obj.comments.count()
    
    # optimisation requêtes
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('comments')
    
    # actions bulk
    actions = ['mark_as_available', 'mark_as_unavailable']
    
    @admin.action(description='marquer disponible')
    def mark_as_available(self, request, queryset):
        updated = queryset.update(disponible=True)
        self.message_user(
            request, 
            f'{updated} pizza{"s" if updated > 1 else ""} disponible{"s" if updated > 1 else ""}.',
            level='success'
        )
    
    @admin.action(description='marquer indisponible')
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(disponible=False)
        self.message_user(
            request, 
            f'{updated} pizza{"s" if updated > 1 else ""} indisponible{"s" if updated > 1 else ""}.',
            level='warning'
        )

# admin ingrédients
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'allergens')
    search_fields = ('name', 'allergens')
    list_filter = ('allergens',)
    ordering = ('name',)

# admin commentaires
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pizza', 'auteur', 'texte_resume', 'created_at')
    list_filter = ('created_at', 'pizza')
    search_fields = ('auteur', 'texte', 'pizza__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def texte_resume(self, obj):
        return obj.texte[:50] + "..." if len(obj.texte) > 50 else obj.texte
    texte_resume.short_description = 'commentaire'
