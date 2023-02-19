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
