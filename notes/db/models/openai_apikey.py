from user import User
from django.db import models


class OpenaiApiKey(models.Model):
    id = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyHash = models.TextField()
