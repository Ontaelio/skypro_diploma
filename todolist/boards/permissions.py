from rest_framework import permissions, serializers

from boards.models import BoardParticipant, Board


class BoardPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):

        _filters: dict = {'user': request.user, 'board': obj}
        if request.method not in permissions.SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**_filters).exists()

