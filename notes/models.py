from django.contrib.postgres.fields import ArrayField
from django.db import models
from notes.features.generate_random_string import generate_random_string


class User(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    nickname = models.CharField(max_length=24)
    email = models.EmailField()
    passwordHash = models.TextField()

    def to_json(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "email": self.email,
            "passwordHash": self.passwordHash
        }


class Vault(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    title = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isPublic = models.BooleanField()
    description = models.TextField(1000)
    tags = ArrayField(models.CharField(max_length=40), max_length=10)
    # notes = ArrayField(models.ForeignKey(Note, on_delete=models.CASCADE))

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "user": self.user,
            "isPublic": self.isPublic,
            "description": self.description,
            "tags": self.tags,
        }


class Image(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    file = models.ImageField(upload_to="backgrounds/", default=generate_random_string)

    def to_json(self):
        return {
            "id": self.id,
            "user": self.user,
            "file": self.file
        }


class Note(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    title = models.CharField(max_length=100)
    colors = ArrayField(models.CharField(max_length=7), max_length=3)
    content = models.JSONField()
    image = models.ForeignKey(Image, on_delete=models.PROTECT, default=generate_random_string)
    vault = models.ForeignKey(Vault, on_delete=models.CASCADE)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "colors": self.colors,
            "image": self.image,
            "content": self.content,
            "vault": self.vault,
        }


class OpenaiApiKey(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.TextField()

    def to_json(self):
        return {
            "id": self.id,
            "key": self.key,
        }


class AiChat(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apikey = models.ForeignKey(OpenaiApiKey, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    keyHash = models.TextField()

    def to_json(self):
        return {
            "id": self.id,
            "user": self.user,
            "apikey": self.apikey,
            "note": self.note,
            "keyHash": self.keyHash,
        }
