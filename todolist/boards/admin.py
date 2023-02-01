from django.contrib import admin

from boards.models import Board, BoardParticipant

admin.site.register(Board)
admin.site.register(BoardParticipant)
