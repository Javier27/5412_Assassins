from mobile_api.models import Game
from mobile_api.serializers import GameSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.contrib.auth.models import User
from mobile_api import util
from mobile_api.models import Player

#TODO: Stuff at top should probably be moved into another file
GAME_STATUS =[(1,'pending'),(2,'in_progress'),(3,'over')]

def get_game(pk):
  try:
    return Game.objects.get(pk=pk)
  except Game.DoesNotExist:
    raise Http404
    
class Create(APIView):
  def post(self, request):
    data = request.DATA
    data.__setitem__('owner', request.user.id)
    data.__setitem__('status',0)
    serializer = GameSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Give all the games a profile is playing
class List_All_Playing(APIView):
  def get(self, request):
    profile = util.get_profile_given_user_id(request.user.id)
    games = util.get_games_for_profile(profile)
    serializer = GameSerializer(games)
    return Response(serializer.data)
  
    
class Status(APIView):
  def get(self, request, pk):
    game = get_game(pk)
    serializer = GameSerializer(game)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
  #TODO make sure owner
  def delete(self, request, pk):
    game = get_game(pk)
    game.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

#TODO make sure owner
class Start(APIView):
  def post(self, request, pk):
    game = get_game(pk)
    if (int(game.status) > 0):
      return Response(data="Game has already started", status=status.HTTP_400_BAD_REQUEST)
    players = Player.objects.filter(game_id=pk)
    player_id_query =Player.objects.values_list('id',flat=True).filter(game_id=pk).filter(accepted=True)
    player_ids = list(player_id_query)
    random.shuffle(player_ids)
    
    #make sure there are at least two players in a game
    if(len(player_ids) < 2):
      return Response("Not enough players",status=status.HTTP_400_BAD_REQUEST)
    
    #Assign a player their target by id aslong as its not themselfs
    for player in players:
      if not player.accepted:
        player.delete()
      else:
        for p_id in player_ids:
          if p_id != player.id:
            player.target = Player(id=p_id)
            player_ids.remove(p_id)
            player.save()
            break
    game.status=2
    
    game.save()
    return Response(status=status.HTTP_200_OK)