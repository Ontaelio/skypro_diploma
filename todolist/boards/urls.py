from django.urls import path

from . import views

urlpatterns = [
    path("create", views.BoardCreateView.as_view(), name='create-board'),
    path("list", views.BoardListView.as_view(), name='board-list'),
    path("<pk>", views.BoardView.as_view(), name='board-details'),
]
