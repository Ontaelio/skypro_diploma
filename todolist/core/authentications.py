from rest_framework import authentication

from core.models import TgUser


class TgUserAuthentication(authentication.BaseAuthentication):
    """
    Telegram user authentication. Makes a known TG ID authenticated.
    """
    def authenticate(self, request):
        tg_user = request.META.get('HTTP_TG_USER')

        if not tg_user:
            return None

        try:
            tuser = TgUser.objects.get(tg_user=int(tg_user))
        except TgUser.DoesNotExist:
            return None

        return (tuser.user, None)
