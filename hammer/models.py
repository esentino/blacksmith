from __future__ import annotations

import math
import random
import uuid
from datetime import timedelta
from typing import Optional, Type, TypeVar

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

DAY_IN_SECONDS = 3600 * 24


class TaskStatus(models.IntegerChoices):
    WAITING = 1, _("Waiting")
    IN_PROGRESS = 2, _("In progress")


class Blacksmith(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gold = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    heating_attribute = models.IntegerField(default=1)
    holding_attribute = models.IntegerField(default=1)
    hitting_attribute = models.IntegerField(default=1)
    shaping_attribute = models.IntegerField(default=1)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="blacksmith")

    def add_exp(self, experience: int):
        self.experience = F("experience") + experience

    def add_gold(self, gold: int):
        self.gold = F("gold") + gold

    @property
    def attribute_multiplication(self) -> int:
        return self.heating_attribute * self.holding_attribute * self.hitting_attribute * self.shaping_attribute

    @property
    def heating_experience_price(self) -> int:
        return self.heating_attribute * 100 + self.attribute_multiplication

    @property
    def holding_experience_price(self) -> int:
        return self.holding_attribute * 100 + self.attribute_multiplication

    @property
    def hitting_experience_price(self) -> int:
        return self.hitting_attribute * 100 + self.attribute_multiplication

    @property
    def shaping_experience_price(self) -> int:
        return self.shaping_attribute * 100 + self.attribute_multiplication

    def add_heating_attribute(self) -> bool:
        if self.experience < self.heating_experience_price:
            return False

        self.experience -= self.heating_experience_price
        self.heating_attribute = F("heating_attribute") + 1
        self.save()
        return True

    def add_holding_attribute(self) -> bool:
        if self.experience < self.holding_experience_price:
            return False

        self.experience -= self.holding_experience_price
        self.holding_attribute = F("holding_attribute") + 1
        self.save()
        return True

    def add_hitting_attribute(self) -> bool:
        if self.experience < self.hitting_experience_price:
            return False

        self.experience -= self.hitting_experience_price
        self.hitting_attribute = F("hitting_attribute") + 1
        self.save()
        return True

    def add_shaping_attribute(self) -> bool:
        if self.experience < self.shaping_experience_price:
            return False

        self.experience -= self.shaping_experience_price
        self.shaping_attribute = F("shaping_attribute") + 1
        self.save()
        return True


T = TypeVar("T", bound="Task")


class Task(models.Model):
    blacksmith = models.ForeignKey(Blacksmith, on_delete=models.CASCADE, related_name="tasks")
    heating_work = models.IntegerField()
    holding_work = models.IntegerField()
    hitting_work = models.IntegerField()
    shaping_work = models.IntegerField()
    status = models.IntegerField(choices=TaskStatus.choices, default=TaskStatus.WAITING)
    start_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-status']

    @property
    def experience(self) -> int:
        return self.heating_work + self.holding_work + self.hitting_work + self.shaping_work

    @property
    def gold(self) -> int:
        time_part = math.log(self.heating_work + self.holding_work + self.hitting_work + self.shaping_work)
        exp_part = math.log(self.experience)
        return math.ceil(time_part + exp_part)

    @property
    def time_to_done(self) -> int:
        return self.heating_time + self.holding_time + self.hitting_time + self.shaping_time

    @property
    def time_left(self) -> Optional[timedelta]:
        if self.elapsed_time:
            return timedelta(days=self.days_of_work, seconds=self.seconds_of_work) - self.elapsed_time
        return None

    @property
    def elapsed_time(self) -> Optional[timedelta]:
        if not self.start_time:
            return None
        return now() - self.start_time

    @property
    def progress(self) -> Optional[int]:
        if self.elapsed_time and self.time_left:
            total_time_delta = self.time_left + self.elapsed_time
            return math.floor(self.elapsed_time/total_time_delta * 100)
        return None

    @property
    def left_progress(self) -> Optional[int]:
        return 100 - self.progress if self.progress else None

    @property
    def shaping_time(self) -> int:
        return math.ceil(self.shaping_work / self.blacksmith.shaping_attribute)

    @property
    def hitting_time(self) -> int:
        return math.ceil(self.hitting_work / self.blacksmith.hitting_attribute)

    @property
    def holding_time(self) -> int:
        return math.ceil(self.holding_work / self.blacksmith.holding_attribute)

    @property
    def heating_time(self) -> int:
        return math.ceil(self.heating_work / self.blacksmith.heating_attribute)

    @classmethod
    def generate_task(cls: Type[T], blacksmith: Blacksmith) -> T:
        task = cls()
        task.blacksmith = blacksmith
        task.heating_work = random.randint(1, blacksmith.heating_attribute * 100)
        task.holding_work = random.randint(1, blacksmith.holding_attribute * 100)
        task.hitting_work = random.randint(1, blacksmith.hitting_attribute * 100)
        task.shaping_work = random.randint(1, blacksmith.shaping_attribute * 100)
        task.save()
        return task

    @property
    def can_start(self) -> bool:
        if self.status != TaskStatus.WAITING:
            return False
        for task in self.blacksmith.tasks.all():
            if task.status != TaskStatus.WAITING:
                return False
        return True

    @property
    def in_progress(self) -> bool:
        return self.status == TaskStatus.IN_PROGRESS

    def start(self) -> bool:
        if self.can_start:
            self.status = TaskStatus.IN_PROGRESS
            self.start_time = now()
            self.save()
            return True
        return False

    @property
    def is_done(self) -> bool:
        if self.status == TaskStatus.IN_PROGRESS and self.elapsed_time:
            days_work = self.days_of_work
            seconds_work = self.seconds_of_work
            work_time = timedelta(days=days_work, seconds=seconds_work)
            return self.elapsed_time > work_time
        return False

    @property
    def seconds_of_work(self) -> float:
        return self.time_to_done % DAY_IN_SECONDS

    @property
    def days_of_work(self) -> float:
        return self.time_to_done // DAY_IN_SECONDS

    def process(self):
        if self.is_done:
            self.blacksmith.add_gold(self.gold)
            self.blacksmith.add_exp(self.experience)
            self.blacksmith.save()
            self.delete()
