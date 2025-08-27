from datetime import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Auteur, Livre, Article, Commentaire, Categorie, Note
from .serializers import (
    AuteurSerializer, 
    LivreSerializer, 
    ArticleSerializer, 
    CommentaireSerializer, 
    NoteSerializer
)
from .forms import ArticleForm, CommentaireForm
from .permissions import IsOwnerOrReadOnly, IsInGroupFactory

# Exercice 3 : Vue fonction basique
def current_datetime(request):
    now = datetime.now()
    return render(request, 'bibliotheque/now.html', {'datetime': now})

# Exercice 4 : Vues génériques
class ArticleListView(ListView):
    model = Article
    template_name = 'bibliotheque/article_list.html'
    context_object_name = 'articles'
    paginate_by = 5

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'bibliotheque/article_detail.html'
    context_object_name = 'article'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commentaire_form'] = CommentaireForm()
        return context

# Exercice 6 : Formulaire et messages
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'bibliotheque/article_form.html'
    success_url = reverse_lazy('article_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Article créé avec succès !')
        return super().form_valid(form)

# Vue pour ajouter un commentaire
class CommentaireCreateView(CreateView):
    model = Commentaire
    form_class = CommentaireForm
    template_name = 'bibliotheque/commentaire_form.html'
    
    def form_valid(self, form):
        form.instance.article_id = self.kwargs['article_pk']
        messages.success(self.request, 'Commentaire ajouté avec succès !')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.kwargs['article_pk']})

# DRF ViewSets avec permissions (Chapitre 3)

# 3. D – Restrictions de lecture/écriture : IsAuthenticatedOrReadOnly pour LivreViewSet
class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    
    def get_queryset(self):
        """Filtrage par année de naissance"""
        queryset = Auteur.objects.all()
        year = self.request.query_params.get('year', None)
        if year is not None:
            try:
                year = int(year)
                queryset = queryset.filter(date_naissance__year__gte=year)
            except ValueError:
                pass
        return queryset
    
    @action(detail=True, methods=['get'])
    def titres(self, request, pk=None):
        """Action personnalisée qui renvoie les titres des livres de l'auteur"""
        auteur = self.get_object()
        titres = [livre.titre for livre in auteur.livres.all()]
        return Response({'titres': titres})


# ArticleListViewSet public
class ArticleListViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny] #E – AllowAny
    
    def perform_create(self, serializer):
        """Assigne automatiquement l'utilisateur connecté comme propriétaire"""
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            serializer.save()


# 5. B – Permission basée sur le propriétaire : NoteViewSet avec IsOwnerOrReadOnly
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Filtre les notes pour ne montrer que celles de l'utilisateur connecté"""
        return Note.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        """Assigne automatiquement l'utilisateur connecté comme propriétaire"""
        serializer.save(owner=self.request.user)


# 6. A – Permission basée sur le groupe : CommentViewSet avec IsInGroup("moderator")
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        """
        Instancie et retourne la liste des permissions requises pour cette vue.
        """
        if self.action == 'destroy':
            # Seuls les modérateurs peuvent supprimer
            permission_classes = [IsInGroupFactory("moderator")]
        else:
            # Lecture pour tous, écriture pour les authentifiés
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Assigne automatiquement l'utilisateur connecté comme propriétaire"""
        serializer.save(owner=self.request.user)
