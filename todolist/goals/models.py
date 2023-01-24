from django.db import models

from core.models import User


class ModelWithDates(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')


class GoalCategory(ModelWithDates):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(max_length=255, verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')

    def __str__(self):
        return self.title


class Goal(ModelWithDates):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    title = models.CharField(max_length=255, verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey(GoalCategory, on_delete=models.RESTRICT, related_name='Goals', verbose_name='Категория')
    status = models.SmallIntegerField(choices=Status.choices, default=Status.to_do, verbose_name='Статус')
    priority = models.SmallIntegerField(choices=Priority.choices, default=Priority.medium, verbose_name='Приоритет')
    due_date = models.DateField(null=True, blank=True, verbose_name='Дата дедлайна')

    def __str__(self):
        return self.title


class GoalComment(ModelWithDates):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Comments', verbose_name='Автор')
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='Comments', verbose_name='Цель')
    text = models.TextField(verbose_name='Комментарий')

