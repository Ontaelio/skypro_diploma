import pytest
from django.urls import reverse
from rest_framework import status

from tests.utils import BaseTestCase


@pytest.mark.django_db
class TestProfileRetrieve(BaseTestCase):
    url = reverse('core:signup')

    def test_not_matched_passwords(self, client, faker):
        password_1 = faker.password()
        password_2 = faker.password()
        username = faker.user_name()
        response = client.post(self.url, data={
            'username': username,
            'password': password_1,
            'password_repeat': password_2,
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'password_repeat': ['Passwords do not match.']}

    @pytest.mark.parametrize(('weak_pass', 'status_code'),
                             [('ac2', status.HTTP_400_BAD_REQUEST),
                              ('qwerty123', status.HTTP_400_BAD_REQUEST),
                              ('qasd234WuWu22', status.HTTP_201_CREATED)])
    def test_weak_or_good_pass(self, client, faker, weak_pass, status_code):
        username = faker.user_name()
        response = client.post(self.url, data={
            'username': username,
            'password': weak_pass,
            'password_repeat': weak_pass,
        })
        assert response.status_code == status_code

    def test_signup_good(self, client, user_factory, faker, django_user_model):
        assert not django_user_model.objects.count()

        user = user_factory.build()
        response = client.post(self.url, data={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password,
            'password_repeat': user.password,
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert django_user_model.objects.count() == 1

        new_user = django_user_model.objects.last()
        assert response.json() == {
            'id': new_user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        assert new_user.password != user.password
        assert new_user.check_password(user.password)

