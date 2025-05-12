from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_games),
    path("<int:pk>", views.get_game),
]