from django.urls import path
from notes.views.ai import Ai

urlpatterns = [
    path("ai/", Ai.as_view(), name='ai')
]
