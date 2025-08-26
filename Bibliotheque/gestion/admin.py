from django.contrib import admin
from .models import Livre, Personne

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'theme', 'note', 'disponibilite')
    list_filter = ('theme', 'disponibilite', 'note')
    search_fields = ('titre', 'auteur', 'theme')
    list_editable = ('disponibilite',)

@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'age', 'lieu_residence', 'livre_emprunte')
    list_filter = ('lieu_residence', 'age')
    search_fields = ('nom', 'prenom')
    
    def save_model(self, request, obj, form, change):
        """Override pour gérer les validations lors de la sauvegarde depuis l'admin"""
        try:
            obj.full_clean()  # Appelle clean() et les validations
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Erreur lors de la sauvegarde : {e}")
