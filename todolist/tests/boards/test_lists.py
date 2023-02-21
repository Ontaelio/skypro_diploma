import pytest
from django.urls import reverse
from rest_framework import status

from tests.utils import BaseTestCase


@pytest.mark.django_db
class TestBoardsList(BaseTestCase):
    url = reverse('goals:boards:board-list')

    def test_no_auth(self, client):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('role', [1, 2, 3])
    def test_get_list_by_role(self, board_factory, user_factory, client, participant_factory, role):
        user = user_factory.create()
        client.force_login(user)
        boards = board_factory.create_batch(5)
        participant_factory.create(user=user, board=boards[0], role=role)
        participant_factory.create(user=user, board=boards[2], role=role)
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

    @pytest.mark.parametrize(('user_status', 'responses_count'),
                             [('man', 9),
                              ('lesser', 6),
                              ('tiny', 2)])
    def test_get_list_by_user(self, board_factory, user_factory, client,
                              participant_factory, user_status, responses_count):
        users = {'man': user_factory.create(),
                 'lesser': user_factory.create(),
                 'tiny': user_factory.create()}

        boards = board_factory.create_batch(10)

        for k in range(9):
            participant_factory.create(user=users['man'], board=boards[k], role=1)
        participant_factory.create(user=users['lesser'], board=boards[9], role=1)

        for k in range(5):
            participant_factory.create(user=users['lesser'], board=boards[k], role=2)
        participant_factory.create(user=users['tiny'], board=boards[0], role=3)
        participant_factory.create(user=users['tiny'], board=boards[9], role=3)

        client.force_login(users[user_status])
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == responses_count
