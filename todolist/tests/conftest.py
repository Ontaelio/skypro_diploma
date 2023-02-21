import pytest
from rest_framework.test import APIClient

# from tests.factories import *

pytest_plugins = ['tests.factories', 'tests.fixtures']


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
def auth_client(client, user):
    client.force_login(user)
    return client
