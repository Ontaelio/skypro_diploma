import pytest
from django.urls import reverse
from rest_framework import status

from tests.utils import BaseTestCase


@pytest.mark.django_db
class TestTgUser(BaseTestCase):

    def test_create(self, client, tg_user_factory):
        tg_user = tg_user_factory.build(user=None)
        url = reverse('create_tg_user')
        response = client.post(url, data={'tg_user': tg_user.tg_user,
                                          'verification_code': tg_user.verification_code},
                               format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['verification_code'] == tg_user.verification_code
        assert response.json()['tg_user'] == tg_user.tg_user
        assert not response.json()['user']

    def test_auth_verify(self, client, faker):
        url = reverse('verify_tg_user')
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_verify(self, client, user_factory, tg_user_factory):
        user = user_factory.create()
        client.force_login(user)
        tg_user = tg_user_factory.create(user=None)
        url = reverse('verify_tg_user')
        response = client.patch(url, data={'verification_code': tg_user.verification_code})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['user'] == user.id

    def test_wrong_code(self, client, user_factory, tg_user_factory):
        user = user_factory.create()
        client.force_login(user)
        tg_user = tg_user_factory.create(user=None)
        url = reverse('verify_tg_user')
        wrong_code = tg_user.verification_code.lower()
        response = client.patch(url, data={'verification_code': wrong_code})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_unbind(self, client, user_factory, tg_user_factory):
        user = user_factory.create()
        client.force_login(user)
        tg_user = tg_user_factory.create(user=user)
        url = reverse('delete_binding', kwargs={'tg_user': tg_user.tg_user})
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


