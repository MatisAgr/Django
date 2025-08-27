from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (LivreViewSet, AuteurViewSet, ArticleListViewSet, NoteViewSet, CommentViewSet,current_datetime, ArticleListView, ArticleDetailView, ArticleCreateView, CommentaireCreateView, basic_auth_test, session_auth_test, generate_token, token_auth_test)

# Router DRF
router = DefaultRouter()
router.register(r'livres', LivreViewSet)
router.register(r'auteurs', AuteurViewSet)
router.register(r'articles', ArticleListViewSet)    # E – AllowAny
router.register(r'notes', NoteViewSet)              # B – IsOwnerOrReadOnly
router.register(r'commentaires', CommentViewSet)    # A – IsInGroup("moderator")

urlpatterns = [
    # API DRF (Chapitre 3)
    path('api/', include(router.urls)),
    
    # E – Test BasicAuthentication
    path('api/test-basic/', basic_auth_test, name='basic_auth_test'),
    
    # D – Test SessionAuthentication
    path('api/test-session/', session_auth_test, name='session_auth_test'),
    
    # C – TokenAuthentication
    path('api/generate-token/', generate_token, name='generate_token'),
    path('api/test-token/', token_auth_test, name='token_auth_test'),
    
    # Vues Django (Chapitre 2)
    path('now/', current_datetime, name='current_datetime'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/nouveau/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:article_pk>/commentaire/', CommentaireCreateView.as_view(), name='commentaire_create'),
]
