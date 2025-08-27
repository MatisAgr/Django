from rest_framework import serializers
from .models import Auteur, Livre

class LivreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livre
        fields = ['id', 'titre', 'date_sortie', 'auteur']

class AuteurSerializer(serializers.ModelSerializer):
    livres = LivreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Auteur
        fields = ['id', 'nom', 'date_naissance', 'livres']
