import factory
from pytest_factoryboy import register

from core.models import User


@register
class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = factory.Faker('ascii_email')
