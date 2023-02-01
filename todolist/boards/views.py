from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from boards.models import Board
from boards.serializers import BoardCreateSerializer, BoardSerializer
from boards.permissions import BoardPermissions
from goals.models import Goal


class BoardCreateView(generics.CreateAPIView):
    model = Board
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = (BoardPermissions,)
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


# add permissions!
class BoardListView(generics.ListAPIView):
    model = Board
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BoardSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = ["title", "description"]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.prefetch_related('participants').filter(
            participants__user_id=self.request.user.id,
            is_deleted=False
        )
