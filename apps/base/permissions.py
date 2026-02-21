from rest_framework.permissions import BasePermission, SAFE_METHODS

# admin write, user read
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # everyone can GET
        if request.method in SAFE_METHODS:
            return True

        # only admin can POST / PUT / DELETE
        return (
            request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )
    
     
class MessagePermission(BasePermission):
    """
    Officer: POST only
    Admin: GET + PATCH only
    """ 
    def has_permission(self, request, view):
        user = request.user
 
        if not user or not user.is_authenticated:
            return False

        # Admin rules
        if user.is_staff or user.is_superuser:
            # Admin can GET and PATCH generally. Admin can also POST for the custom 'reply' action.
            if request.method in ["GET", "PATCH"]:
                return True
            if request.method == "POST" and getattr(view, "action", None) == "reply":
                return True
            return False

        # Officer rules
        return request.method in ["GET", "POST"]