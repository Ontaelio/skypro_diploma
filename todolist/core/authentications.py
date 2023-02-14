import logging

from rest_framework import authentication
from rest_framework import exceptions

from core.models import TgUser


class TgUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        tg_user = request.META.get('HTTP_TG_USER')
        # print(dir(request))
        # print(request.META)
        # print('tg_user', tg_user)
        # logging.critical(tg_user)
        if not tg_user:
            return None

        try:
            tuser = TgUser.objects.get(tg_user=int(tg_user))
        except TgUser.DoesNotExist:
            return None

        return (tuser.user, None)
