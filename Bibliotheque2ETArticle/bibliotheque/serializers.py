from rest_framework import serializers
from .models import Auteur, Livre, Article, Commentaire, Note

class LivreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livre
        fields = ['id', 'titre', 'date_sortie', 'auteur']

class AuteurSerializer(serializers.ModelSerializer):
    livres = LivreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Auteur
        fields = ['id', 'nom', 'date_naissance', 'livres']


class ArticleSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'titre', 'contenu', 'date', 'categorie', 'owner']
        read_only_fields = ['date', 'owner']


class CommentaireSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Commentaire
        fields = ['id', 'article', 'nom', 'contenu', 'date', 'owner']
        read_only_fields = ['date', 'owner']


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'titre', 'contenu', 'date_creation', 'date_modification', 'owner']
        read_only_fields = ['date_creation', 'date_modification', 'owner']
