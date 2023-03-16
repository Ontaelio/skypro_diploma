import pytest
from django.urls import reverse
from rest_framework import status

from tests.utils import BaseTestCase


@pytest.mark.django_db
class TestLogin(BaseTestCase):
    url = reverse('core:login')

    def test_user_not_found(self, client, user_factory):
        user = user_factory.build()

        response = client.post(self.url, data={
            'username': user.username,
            'password': user.password,
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_valid_login_logout(self, client, faker, user_factory):
        password = faker.password()
        user = user_factory.create(password=password, is_active=True)

        response = client.post(self.url, data={
            'username': user.username,
            'password': password,
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }

    def test_wrong_password(self, client, faker, user_factory):
        password = faker.password()
        user = user_factory.create(password=password, is_active=True)

        response = client.post(self.url, data={
            'username': user.username,
            'password': '123qwert2',
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(('is_active', 'status_code'),
                             [(True, status.HTTP_201_CREATED), (False, status.HTTP_403_FORBIDDEN)])
    def test_inactive_user(self, client, faker, user_factory, is_active, status_code):
        password = faker.password()
        user = user_factory.create(password=password, is_active=is_active)

        response = client.post(self.url, data={
            'username': user.username,
            'password': password,
        })

        assert response.status_code == status_code





