import pytest
from django.urls import reverse
from rest_framework import status

from tests.utils import BaseTestCase


@pytest.mark.django_db
class TestProfileRetrieve(BaseTestCase):
    url = reverse('core:profile')

    def test_auth_get(self, client):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_profile(self, auth_client, user):
        response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }


@pytest.mark.django_db
class TestProfileDestroy(BaseTestCase):
    url = reverse('core:profile')

    def test_auth_destroy(self, client, faker):
        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_logout(self, auth_client):
        response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        response = auth_client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestProfileUpdate(BaseTestCase):
    url = reverse('core:profile')

    def test_auth_patch(self, client):
        response = client.patch(self.url, data={"first_name": "Ivan", "last_name": "Ivanov"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_profile_patch(self, auth_client):
        response = auth_client.patch(self.url, data={"first_name": "Ivan11", "last_name": "Ivanov22"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['first_name'] == 'Ivan11'
        assert response.json()['last_name'] == 'Ivanov22'


@pytest.mark.django_db
class TestPasswordUpdate(BaseTestCase):
    url = reverse('core:update_password')

    def test_auth_patch(self, client):
        response = client.patch(self.url, data={"old_password": "trewq666atat", "new_password": "qwert666tata"})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        response = client.put(self.url, data={"old_password": "trewq666atat", "new_password": "qwert666tata"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_bad_old_pass(self, auth_client, faker):
        response = auth_client.patch(self.url, data={
            'old_password': 'aaa123bbb666qqqggg777000999',
            'new_password': faker.password(),
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'old_password': {'old_password': 'Password is incorrect.'}}

    @pytest.mark.parametrize(('weak_pass', 'status_code'),
                             [('ac2', status.HTTP_400_BAD_REQUEST),
                              ('qwerty123', status.HTTP_400_BAD_REQUEST),
                              ('qasd234WuWu22', status.HTTP_200_OK)])
    def test_weak_or_good_pass(self, client, user_factory, faker, weak_pass, status_code):
        password = faker.password()
        user = user_factory.create(password=password)

        client.force_login(user)
        response = client.patch(self.url, data={
            'old_password': password,
            'new_password': weak_pass,
        })
        assert response.status_code == status_code

    def test_password_changed(self, client, faker, user_factory):
        old_password = faker.password()
        user = user_factory.create(password=old_password)
        new_password = faker.password()
        client.force_login(user)
        response = client.patch(self.url, data={
            'old_password': old_password,
            'new_password': new_password,
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {}
        user.refresh_from_db(fields=('password',))
        assert user.check_password(new_password)



