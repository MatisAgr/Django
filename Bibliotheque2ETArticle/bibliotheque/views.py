from datetime import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Auteur, Livre, Article, Commentaire, Categorie
from .serializers import AuteurSerializer, LivreSerializer
from .forms import ArticleForm, CommentaireForm

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

# DRF ViewSets (Chapitre 3)
class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer

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
