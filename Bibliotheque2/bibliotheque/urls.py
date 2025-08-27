from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LivreViewSet, AuteurViewSet

router = DefaultRouter()
router.register(r'livres', LivreViewSet)
router.register(r'auteurs', AuteurViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
