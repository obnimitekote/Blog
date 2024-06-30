import uuid

from django.db import models
from django.contrib.auth.models import User

class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)
