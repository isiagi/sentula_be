from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    '''
    Custom permission to only allow owners of an object to view, update and delete
    '''

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        # if request.method in SAFE_METHODS:
        #     return True
        if request.user and request.user.is_staff:
            return True
        
        # if obj.user == request.user:
        #     return True
    
        return obj.user == request.user