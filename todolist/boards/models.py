from django.db import models

from todolist.commons import ModelWithDates

from core.models import User


class Board(ModelWithDates):
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self):
        return self.title


class BoardParticipant(ModelWithDates):
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(Board, on_delete=models.PROTECT, related_name="participants", verbose_name="Доска")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="participants", verbose_name="Пользователь")
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.owner, verbose_name="Роль")
