from vault import Vault
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Note(models.Model):
    id = models.CharField(max_length=32)
    title = models.CharField(max_length=100)
    colors = ArrayField(models.CharField(max_length=7), max_length=3)
    content = models.JSONField()
    vault = models.ForeignKey(Vault, on_delete=models.CASCADE)
