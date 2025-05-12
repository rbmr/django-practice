from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Game 
from .serializers import GameSerializer
from rest_framework import status 
from . import main
# Create your views here.

@api_view(["GET", "POST", "DELETE"])
def get_games(request):
    if request.method == "POST":
        game = Game.objects.create()
        serializer = GameSerializer(game, many=False)
        return Response(serializer.data)
    if request.method == "DELETE":
        Game.objects.all().delete()
        return Response("Boom!")
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

@api_view(["GET", "DELETE", "PUT"])
def get_game(request, pk):
    if not Game.objects.filter(pk=pk).exists():
        return Response("Game not found", status=404)
    game = Game.objects.get(pk=pk)
    if request.method == "DELETE":
        game.delete()
        stat = status.HTTP_204_NO_CONTENT
    if request.method == "PUT":
        moved = game.move(request.data) 
        game.save()
        stat = status.HTTP_200_OK if moved else status.HTTP_400_BAD_REQUEST
    if request.method == "GET":
        stat = status.HTTP_200_OK
    print(main.neat(game.state))
    serialized_game = GameSerializer(game, many=False)
    return Response(serialized_game.data, status=stat)