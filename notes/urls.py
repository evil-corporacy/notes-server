from django.urls import path
from notes.views.ai import Ai
from notes.views.api_keys import ApiKeys
from notes.views.users import Login, Registration, GetMe

urlpatterns = [
    path("ai/", Ai.as_view(), name='ai'),
    path("apikeys/", ApiKeys.as_view(), name='apikeys'),
    path("auth/login", Login.as_view(), name='login'),
    path("auth/registration", Registration.as_view(), name='registration'),
    path("auth/me", GetMe.as_view(), name='get me'),
]
