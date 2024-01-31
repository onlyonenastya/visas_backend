from rest_framework.permissions import BasePermission
import redis


from django.conf import settings
from .models import CustomUser

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)



class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        access_token = request.COOKIES.get("access_token") 
        # print(access_token)
        if access_token is None: 
            return False 
        try: 
            user = session_storage.get(access_token).decode('utf-8') 
        except Exception as e: 
            return False 
 
        return True


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        access_token = request.COOKIES.get("access_token")

        if not access_token:
            return False

        try:
            username = session_storage.get(access_token).decode('utf-8')
        except Exception as e:
            return False

        user = CustomUser.objects.filter(email=username).first()

        if not user or not user.is_moderator:
            return False

        return True
