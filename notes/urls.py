from django.urls import path
from .views import GptView

urlpatterns = [
    path("poops/", GptView.as_view(), name='poop')
]