# ============================================================
# Fichier : apps/accounts/backends.py
# Permet plusieurs sessions simultanées pour différents users
# ============================================================

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class MultiSessionBackend(ModelBackend):
    """
    Backend d'authentification qui permet à plusieurs utilisateurs
    d'être connectés simultanément depuis des navigateurs différents,
    sans que la connexion de l'un invalide celle de l'autre.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user if self.user_can_authenticate(user) else None
        except User.DoesNotExist:
            return None