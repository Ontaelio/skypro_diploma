import factory
from pytest_factoryboy import register

from core.models import User, TgUser
from boards.models import Board, BoardParticipant


@register
class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = factory.Faker('ascii_email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs)


@register
class BoardFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Board

    title = factory.Faker('text', locale='ru_RU', max_nb_chars=255)
    is_deleted = False


@register
class ParticipantFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = factory.Faker('pyint', min_value=2, max_value=3)


@register
class TgUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TgUser

    tg_user = factory.Faker('pyint', min_value=1000000000, max_value=9999999999)
    user = factory.SubFactory(UserFactory)
    verification_code = factory.Faker('password', special_chars=False)