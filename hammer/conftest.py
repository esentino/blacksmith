import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from hammer.models import Blacksmith
from hammer.views import ProfileView


@pytest.fixture()
def new_user(faker):
    return get_user_model().objects.create(username=faker.user_name())


@pytest.fixture()
def user_with_blacksmith(new_user: User) -> User:
    new_user = get_user_model().objects.create(username="test1")
    Blacksmith.objects.create(owner=new_user)
    new_user.refresh_from_db()
    return new_user


@pytest.fixture()
def user_with_blacksmith_and_task(user_with_blacksmith: User) -> User:
    ProfileView.prepare_tasks_for_blacksmith(user_with_blacksmith.blacksmith)
    user_with_blacksmith.refresh_from_db()
    return user_with_blacksmith
