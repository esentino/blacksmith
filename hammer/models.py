import uuid

from django.contrib.auth.models import User
from django.db import models


class Blacksmith(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    heating_attribute = models.IntegerField(default=1)
    holding_attribute = models.IntegerField(default=1)
    hitting_attribute = models.IntegerField(default=1)
    shaping_attribute = models.IntegerField(default=1)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blacksmith')
