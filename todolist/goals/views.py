from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from goals.models import GoalCategory, Goal, GoalComment
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer
from goals.permissions import GoalCategoryPermissions, GoalPermissions, IsOwnerOrReadOnly

from goals.filters import GoalDateFilter


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    permission_classes = (GoalCategoryPermissions,)
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    permission_classes = (GoalCategoryPermissions,)
    serializer_class = GoalCategorySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ['board']
    ordering_fields = ["title"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    permission_classes = (GoalCategoryPermissions,)
    serializer_class = GoalCategorySerializer

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        """
        We do not delete, we keep it for some reason as 'is_deleted' record (as requested).
        TODO: change this approach if intend to use this as a working app.
        """

        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)
        return instance


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    permission_classes = (GoalPermissions,)
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GoalSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "description"]
    ordering = ["title"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.prefetch_related('category__board__participants').filter(
            Q(category__board__participants__user_id=self.request.user.id) &
            ~Q(status=Goal.Status.archived) &
            Q(category__is_deleted=False)
        )


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    permission_classes = (GoalPermissions,)
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.prefetch_related('category__board__participants').filter(
            Q(category__board__participants__user_id=self.request.user.id) &
            Q(category__is_deleted=False)
        )


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    """
    Order by updated field, the latest first.
    """
    model = GoalComment
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GoalCommentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = ["updated"]
    ordering = ["-updated"]

    def get_queryset(self):
        if goal := self.request.query_params.get('goal'):
            return GoalComment.objects.filter(goal__id=goal)
        return GoalComment.objects.filter(user_id=self.request.user.id)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)
