from django.urls import path
from notes.views.ai import Ai, ApiKeys

urlpatterns = [
    path("ai/", Ai.as_view(), name='ai'),
    path("apikeys/", ApiKeys.as_view(), name='apikeys')
]
