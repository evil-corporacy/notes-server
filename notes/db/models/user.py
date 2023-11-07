from django.db import models


class User(models.Model):
    id = models.CharField(max_length=32)
    nickname = models.CharField(max_length=24)
    email = models.EmailField()
    passwordHash = models.TextField()
