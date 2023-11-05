from django.urls import path
from notes.views.ai import GenerateText

urlpatterns = [
    path("ai/", GenerateText.as_view(), name='generate_text')
]
