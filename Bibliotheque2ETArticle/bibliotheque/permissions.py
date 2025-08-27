from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée qui autorise seulement les propriétaires d'un objet à l'éditer.
    """
    
    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour toute requête,
        # donc on autorise toujours les requêtes GET, HEAD ou OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissions d'écriture seulement pour le propriétaire de l'objet.
        return obj.owner == request.user


class IsInGroup(permissions.BasePermission):
    """
    Permission qui vérifie si l'utilisateur appartient à un groupe spécifique.
    """
    
    def __init__(self, group_name):
        self.group_name = group_name
    
    def __call__(self):
        """
        Permet d'utiliser cette classe comme une fonction.
        Nécessaire pour l'utilisation avec DRF.
        """
        return IsInGroupPermission(self.group_name)


class IsInGroupPermission(permissions.BasePermission):
    """
    Permission qui vérifie si l'utilisateur appartient à un groupe spécifique.
    """
    
    def __init__(self, group_name):
        self.group_name = group_name
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.groups.filter(name=self.group_name).exists()
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


# Fonction utilitaire pour créer facilement une permission de groupe
def IsInGroupFactory(group_name):
    """
    Factory pour créer une permission basée sur un groupe.
    Usage: permission_classes = [IsInGroupFactory("moderator")]
    """
    class DynamicIsInGroup(permissions.BasePermission):
        def has_permission(self, request, view):
            if not request.user or not request.user.is_authenticated:
                return False
            return request.user.groups.filter(name=group_name).exists()
        
        def has_object_permission(self, request, view, obj):
            return self.has_permission(request, view)
    
    return DynamicIsInGroup
