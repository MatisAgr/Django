from datetime import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
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

# vue  basique (pareil que les autres chapitres)
def current_datetime(request):
    now = datetime.now()
    return render(request, 'bibliotheque/now.html', {'datetime': now})

# vues items
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

# form de création d'article
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'bibliotheque/article_form.html'
    success_url = reverse_lazy('article_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Article créé avec succès !')
        return super().form_valid(form)

# form de création d'un commentaire
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

    # filtrer par année de naissance
    def get_queryset(self):
        queryset = Auteur.objects.all()
        year = self.request.query_params.get('year', None)
        if year is not None:
            try:
                year = int(year)
                queryset = queryset.filter(date_naissance__year__gte=year)
            except ValueError:
                pass
        return queryset

    # action qui renvoie les titres des livres de l'auteur
    @action(detail=True, methods=['get'])
    def titres(self, request, pk=None):
        auteur = self.get_object()
        titres = [livre.titre for livre in auteur.livres.all()]
        return Response({'titres': titres})


# ArticleListViewSet public
class ArticleListViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny] #E – AllowAny

    # l'utilisateur devient automatiquement le owner de l'article si authentifié
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            serializer.save()


# 5. B – Permission basée sur le propriétaire : NoteViewSet avec IsOwnerOrReadOnly
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    # filtre par propriétaire
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
    
    # utilisateur devient automatiquement le owner de la note si authentifié
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# 6. A – Permission basée sur le groupe : CommentViewSet avec IsInGroup("moderator")
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # donne la list des perms pour cette vues
    def get_permissions(self):
        if self.action == 'destroy':
            # modérateurs peuvent supprimer
            permission_classes = [IsInGroupFactory("moderator")]
        else:
            # Lecture pour tous, écriture pour les auth
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]
    
    # utilisateur devient automatiquement le owner du commentaire si authentifié
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# E – Test BasicAuthentication
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def basic_auth_test(request):
    """
    Endpoint de test pour BasicAuthentication
    Testez avec: curl -u username:password http://127.0.0.1:8000/api/test-basic/
    """
    return Response({
        'message': 'BasicAuthentication fonctionne !',
        'user': request.user.username,
        'is_staff': request.user.is_staff,
        'groups': [group.name for group in request.user.groups.all()],
        'authentication': str(request.auth),
        'authentication_class': request.authenticators[0].__class__.__name__ if request.authenticators else 'None'
    })


# D – SessionAuth et CSRF
@api_view(['GET'])
def session_auth_test(request):
    """
    Endpoint de test pour SessionAuthentication avec gestion CSRF
    Accessible via navigateur après connexion admin Django
    """
    from rest_framework.authentication import SessionAuthentication
    from rest_framework import permissions as drf_permissions
    
    # Utiliser SessionAuthentication pour cette vue spécifiquement
    if request.user.is_authenticated:
        return Response({
            'message': 'SessionAuthentication fonctionne !',
            'user': request.user.username,
            'is_staff': request.user.is_staff,
            'session_key': request.session.session_key,
            'csrf_token': request.META.get('CSRF_COOKIE', 'Non trouvé'),
            'authentication_method': 'Session',
            'groups': [group.name for group in request.user.groups.all()],
        })
    else:
        return Response({
            'message': 'Non authentifié',
            'hint': 'Connectez-vous via /admin/ puis revenez ici',
            'login_url': '/admin/login/'
        }, status=401)


# C – TokenAuth
@api_view(['POST'])
def generate_token(request):
    """
    Endpoint pour générer un token d'authentification
    POST avec basic auth ou session auth : username/password
    """
    from rest_framework.authtoken.models import Token
    from rest_framework.authentication import BasicAuthentication, SessionAuthentication
    from django.contrib.auth import authenticate
    
    # Si déjà authentifié, générer token directement
    if request.user.is_authenticated:
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({
            'token': token.key,
            'user': request.user.username,
            'created': 'Nouveau token' if created else 'Token existant',
            'instructions': 'Utilisez ce token dans l\'header: Authorization: Token ' + token.key
        })
    
    # Sinon, authentifier avec username/password
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username et password requis',
            'format': 'POST /generate-token/ avec {"username": "...", "password": "..."}'
        }, status=400)
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': user.username,
            'created': 'Nouveau token' if created else 'Token existant',
            'instructions': 'Utilisez ce token dans l\'header: Authorization: Token ' + token.key
        })
    else:
        return Response({
            'error': 'Identifiants invalides'
        }, status=401)


@api_view(['GET'])
def token_auth_test(request):
    """
    Endpoint de test pour TokenAuthentication
    Requiert header: Authorization: Token <your-token>
    """
    from rest_framework.authtoken.models import Token
    
    # Vérifier si la requête utilise TokenAuthentication
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Token '):
        return Response({
            'error': 'Token requis',
            'format': 'Header: Authorization: Token <your-token>',
            'get_token': 'POST /generate-token/ avec vos identifiants'
        }, status=401)
    
    token_key = auth_header.replace('Token ', '')
    
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
        return Response({
            'message': 'TokenAuthentication fonctionne !',
            'user': user.username,
            'token': token_key[:10] + '...',  # Masquer le token complet
            'is_staff': user.is_staff,
            'authentication_method': 'Token',
            'groups': [group.name for group in user.groups.all()],
        })
    except Token.DoesNotExist:
        return Response({
            'error': 'Token invalide'
        }, status=401)
