from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Auteur, Livre
from .serializers import AuteurSerializer, LivreSerializer

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
