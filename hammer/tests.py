import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


@pytest.mark.django_db
def test_profile_check_task_contain_four_elements(user_with_blacksmith: User, client: Client):
    client.force_login(user_with_blacksmith)
    assert user_with_blacksmith.blacksmith.tasks.count() == 0
    response = client.get(reverse("profile"))
    assert response.status_code == 200
    assert user_with_blacksmith.blacksmith.tasks.count() == 4


@pytest.mark.django_db
def test_start_task_should_change_status(user_with_blacksmith_and_task: User, client: Client):
    client.force_login(user_with_blacksmith_and_task)
    task = user_with_blacksmith_and_task.blacksmith.tasks.first()
    assert task
    assert task.can_start

    response = client.get(reverse("start-task", args=[task.id]), follow=True)

    task.refresh_from_db()
    assert response.status_code == 200
    assert task.in_progress


@pytest.mark.django_db
def test_start_in_progress_should_show_error_message(user_with_blacksmith_and_task: User, client: Client):
    client.force_login(user_with_blacksmith_and_task)
    task = user_with_blacksmith_and_task.blacksmith.tasks.first()
    assert task
    task.start()
    assert task.can_start is False

    response = client.get(reverse("start-task", args=[task.id]), follow=True)

    assert response.status_code == 200
    messages = list(response.context["messages"])
    assert len(messages) == 1
    assert str(messages[0]) == """Can't start task other task in progress"""


@pytest.mark.django_db
def test_start_other_in_progress_should_show_error_message(user_with_blacksmith_and_task: User, client: Client):
    client.force_login(user_with_blacksmith_and_task)
    other_task = user_with_blacksmith_and_task.blacksmith.tasks.first()
    assert other_task
    assert other_task.start()
    other_task.refresh_from_db()
    task = user_with_blacksmith_and_task.blacksmith.tasks.first()
    assert task
    assert task.can_start is False

    response = client.get(reverse("start-task", args=[task.id]), follow=True)

    assert response.status_code == 200
    messages = list(response.context["messages"])
    assert len(messages) == 1
    assert str(messages[0]) == """Can't start task other task in progress"""
