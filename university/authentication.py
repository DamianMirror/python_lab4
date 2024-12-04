from rest_framework.authentication import BaseAuthentication
from .models import User

class SessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return None  # Authentication failed

        try:
            user = User.objects.get(id=user_id)
            return (user, None)  # (authenticated user, authentication method)
        except User.DoesNotExist:
            return None
