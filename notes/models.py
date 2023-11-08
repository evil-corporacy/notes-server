from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    nickname = models.CharField(max_length=24)
    email = models.EmailField()
    passwordHash = models.TextField()


class Vault(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    title = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isPublic = models.BooleanField()
    description = models.TextField(1000)
    tags = ArrayField(models.CharField(max_length=40), max_length=10)
    # notes = ArrayField(models.ForeignKey(Note, on_delete=models.CASCADE))


class Note(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    title = models.CharField(max_length=100)
    colors = ArrayField(models.CharField(max_length=7), max_length=3)
    content = models.JSONField()
    vault = models.ForeignKey(Vault, on_delete=models.CASCADE)


class OpenaiApiKey(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyHash = models.TextField()


class AiChat(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apikey = models.ForeignKey(OpenaiApiKey, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    keyHash = models.TextField()
