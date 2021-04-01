import math
import random
import uuid

from django.contrib.auth.models import User
from django.db import models


class Blacksmith(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gold = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    heating_attribute = models.IntegerField(default=1)
    holding_attribute = models.IntegerField(default=1)
    hitting_attribute = models.IntegerField(default=1)
    shaping_attribute = models.IntegerField(default=1)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="blacksmith")


class Task(models.Model):
    blacksmith = models.ForeignKey(Blacksmith, on_delete=models.CASCADE, related_name="tasks")
    heating_work = models.IntegerField()
    holding_work = models.IntegerField()
    hitting_work = models.IntegerField()
    shaping_work = models.IntegerField()

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
