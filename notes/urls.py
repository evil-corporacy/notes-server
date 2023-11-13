from django.urls import path, re_path
from notes.views.ai import *
from notes.views.api_keys import *
from notes.views.users import *
from notes.views.images import *

urlpatterns = [
    path("ai/", Ai.as_view(), name='ai'),
    path("apikeys/", ApiKeys.as_view(), name='apikeys'),
    path("auth/login", Login.as_view(), name='login'),
    path("auth/registration", Registration.as_view(), name='registration'),
    path("auth/me", Me.as_view(), name='get me'),
    path("auth/refresh", RefreshTokenView.as_view(), name='refresh token'),
    path("image", ImageView.as_view(), name='image'),
]
