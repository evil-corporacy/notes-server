from user import User
from note import Note
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Vault(models.Model):
    id = models.CharField(max_length=32)
    title = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isPublic = models.BooleanField()
    description = models.TextField(1000)
    tags = ArrayField(models.CharField(max_length=40), max_length=10)
    notes = ArrayField(models.ForeignKey(Note, on_delete=models.CASCADE))
