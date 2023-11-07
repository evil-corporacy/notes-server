from user import User
from openai_apikey import OpenaiApiKey
from note import Note
from django.db import models


class AiChat(models.Model):
    id = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apikey = models.ForeignKey(OpenaiApiKey, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    keyHash = models.TextField()
