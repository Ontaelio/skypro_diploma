import faker
import pytest


@pytest.fixture
@pytest.mark.django_db
def new_board_owner(user_factory, board_factory, participant_factory):
    owner = user_factory.create()
    board = board_factory.create()
    participant_factory.create(user=owner, board=board, role=1)
    return board, owner


@pytest.fixture
@pytest.mark.django_db
def new_board_editor(user_factory, board_factory, participant_factory):
    user = user_factory.create()
    board = board_factory.create()
    participant_factory.create(user=user, board=board, role=2)
    return board, user


@pytest.fixture
@pytest.mark.django_db
def new_board_reader(user_factory, board_factory, participant_factory):
    user = user_factory.create()
    board = board_factory.create()
    participant_factory.create(user=user, board=board, role=3)
    return board, user


# @pytest.fixture
# @pytest.mark.django_db
# def new_board_owner_participant(user_factory, board_factory, participant_factory):
#     owner = user_factory.create()
#     participant = user_factory.create()
#     board = board_factory.create()
#     participant_factory.create(user=owner, board=board, role=1)
#     return owner, board, participant
