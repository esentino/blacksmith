import pytest
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

@pytest.mark.django_db
def test_profile_check_task_contain_four_elements(user_with_blacksmith: User, client: Client):
    client.force_login(user_with_blacksmith)
    assert user_with_blacksmith.blacksmith.tasks.count() == 0
    response = client.get(reverse('profile'))
    assert response.status_code == 200
    assert user_with_blacksmith.blacksmith.tasks.count() == 4

