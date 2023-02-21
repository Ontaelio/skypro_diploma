import pytest
from django.urls import reverse
from rest_framework import status

from tests.utils import BaseTestCase

from boards.models import BoardParticipant


@pytest.mark.django_db
class TestGetBoard(BaseTestCase):

    def test_no_auth(self, client):
        url = reverse('goals:boards:board-details', kwargs={'pk': 1})
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('role', [1, 2, 3])
    def test_get_board(self, board_factory, user_factory, client, participant_factory, role):
        user = user_factory.create()
        client.force_login(user)
        board = board_factory.create()
        participant_factory.create(user=user, board=board, role=role)
        url = reverse('goals:boards:board-details', kwargs={'pk': board.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCreateBoard(BaseTestCase):
    url = reverse('goals:boards:create-board')

    def test_no_auth(self, client, faker):
        response = client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create(self, client, faker, board_factory, user_factory):
        board = board_factory.build()
        user = user_factory.create()
        client.force_login(user)
        response = client.post(self.url, data={'title': board.title})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['title'] == board.title

        a = BoardParticipant.objects.filter(user=user)
        assert a[0].user.username == user.username
        assert a[0].role == 1
        assert a[0].board.title == board.title


@pytest.mark.django_db
class TestDeleteBoard(BaseTestCase):

    @pytest.mark.parametrize(('role', 'status_code'),
                             [(1, status.HTTP_204_NO_CONTENT),
                              (2, status.HTTP_403_FORBIDDEN),
                              (3, status.HTTP_403_FORBIDDEN),])
    def test_not_an_owner(self, client, user_factory, board_factory, participant_factory,
                          role, status_code):
        user = user_factory.create()
        client.force_login(user)
        board = board_factory.create()
        participant_factory.create(user=user, board=board, role=role)
        url = reverse('goals:boards:board-details', kwargs={'pk': board.id})
        response = client.delete(url)
        assert response.status_code == status_code

    def test_delete_is_owner(self, client, new_board_owner):
        board, user = new_board_owner
        client.force_login(user)
        url = reverse('goals:boards:board-details', kwargs={'pk': board.id})
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestUpdateBoard(BaseTestCase):

    def test_not_an_owner(self, client, new_board_editor):
        board, user = new_board_editor
        client.force_login(user)
        url = reverse('goals:boards:board-details', kwargs={'pk': board.id})
        response = client.patch(url, data={'title': 'A new one'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_title(self, client, new_board_owner):
        board, owner = new_board_owner
        client.force_login(owner)
        url = reverse('goals:boards:board-details', kwargs={'pk': board.id})
        response = client.patch(url, data={'title': 'A new one'})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == 'A new one'

    def test_add_participant(self, client, user_factory, new_board_owner):
        board, owner = new_board_owner
        client.force_login(owner)
        participant = user_factory.create()
        url = reverse('goals:boards:board-details', kwargs={'pk': board.id})
        response = client.patch(url, data={"participants": [{"user": participant.username, "role": 2}]}, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['participants']) == 2

    def test_owner_not_deleted_with_put(self, client, user_factory, new_board_owner):
        board, owner = new_board_owner
        client.force_login(owner)
        participant = user_factory.create()
        url = reverse('goals:boards:board-details', kwargs={'pk': board.id})
        response = client.put(url, data={"participants": [{"user": participant.username, "role": 2}],
                                         "title": "Test title"}, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['participants']) == 2

    def test_extra_owners(self, client, user_factory, new_board_owner):
        board, owner = new_board_owner
        client.force_login(owner)
        participant = user_factory.create()
        url = reverse('goals:boards:board-details', kwargs={'pk': board.id})
        response = client.put(url, data={"participants": [{"user": participant.username, "role": 1}],
                                         "title": "Test title"}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

