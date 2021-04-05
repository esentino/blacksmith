import math
import random
import uuid
from datetime import timedelta
from typing import Optional

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

    def add_exp(self, experience):
        self.experience = F("experience") + experience

    def add_gold(self, gold):
        self.gold = F("gold") + gold


class Task(models.Model):
    blacksmith = models.ForeignKey(Blacksmith, on_delete=models.CASCADE, related_name="tasks")
    heating_work = models.IntegerField()
    holding_work = models.IntegerField()
    hitting_work = models.IntegerField()
    shaping_work = models.IntegerField()
    status = models.IntegerField(choices=TaskStatus.choices, default=TaskStatus.WAITING)
    start_time = models.DateTimeField(null=True, blank=True)

    @property
    def experience(self) -> int:
        return self.heating_work + self.holding_work + self.hitting_work + self.shaping_work

    @property
    def gold(self) -> int:
        time_part = math.log(self.heating_work + self.holding_work + self.hitting_work + self.shaping_work)
        exp_part = math.log(self.experience)
        return math.ceil(time_part + exp_part)

    @property
    def time_to_done(self):
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
        return  now() - self.start_time

    @property
    def shaping_time(self):
        return math.ceil(self.shaping_work / self.blacksmith.shaping_attribute)

    @property
    def hitting_time(self):
        return math.ceil(self.hitting_work / self.blacksmith.hitting_attribute)

    @property
    def holding_time(self):
        return math.ceil(self.holding_work / self.blacksmith.holding_attribute)

    @property
    def heating_time(self) -> float:
        return math.ceil(self.heating_work / self.blacksmith.heating_attribute)

    @classmethod
    def generate_task(cls, blacksmith):
        task = cls()
        task.blacksmith = blacksmith
        task.heating_work = random.randint(1, blacksmith.heating_attribute * 100)
        task.holding_work = random.randint(1, blacksmith.holding_attribute * 100)
        task.hitting_work = random.randint(1, blacksmith.hitting_attribute * 100)
        task.shaping_work = random.randint(1, blacksmith.shaping_attribute * 100)
        task.save()
        return task

    @property
    def can_start(self):
        if self.status != TaskStatus.WAITING:
            return False
        for task in self.blacksmith.tasks.all():
            if task.status != TaskStatus.WAITING:
                return False
        return True

    @property
    def in_progress(self):
        return self.status == TaskStatus.IN_PROGRESS

    def start(self):
        if self.can_start:
            self.status = TaskStatus.IN_PROGRESS
            self.start_time = now()
            self.save()
            return True
        return False

    @property
    def is_done(self):
        if self.status == TaskStatus.IN_PROGRESS:
            days_work = self.days_of_work
            seconds_work = self.seconds_of_work
            work_time = timedelta(days=days_work, seconds=seconds_work)
            return self.elapsed_time > work_time
        return False

    @property
    def seconds_of_work(self):
        return self.time_to_done % DAY_IN_SECONDS

    @property
    def days_of_work(self):
        return self.time_to_done // DAY_IN_SECONDS

    def process(self):
        if self.is_done:
            self.blacksmith.add_gold(self.gold)
            self.blacksmith.add_exp(self.experience)
            self.blacksmith.save()
            self.delete()
