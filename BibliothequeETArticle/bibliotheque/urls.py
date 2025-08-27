from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LivreViewSet, AuteurViewSet, current_datetime,
    ArticleListView, ArticleDetailView, ArticleCreateView,
    CommentaireCreateView
)

# Router DRF
router = DefaultRouter()
router.register(r'livres', LivreViewSet)
router.register(r'auteurs', AuteurViewSet)

urlpatterns = [
    # API DRF (Chapitre 3)
    path('api/', include(router.urls)),
    
    # Vues Django classiques (Chapitre 2)
    path('now/', current_datetime, name='current_datetime'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/nouveau/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:article_pk>/commentaire/', CommentaireCreateView.as_view(), name='commentaire_create'),
]
