from rest_framework import permissions

class MentorOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        mentor_permission = bool(request.user and request.user.is_mentor and request.user.user_status)
        return request.method == "GET" or mentor_permission
