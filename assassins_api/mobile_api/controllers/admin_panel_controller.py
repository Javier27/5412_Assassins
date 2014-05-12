from mobile_api.serializers import ProfileSerializer
from mobile_api.serializers import FriendSerializer
from mobile_api.models import Profile
from mobile_api.models import Player
from mobile_api.models import Assassinations
from mobile_api.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from mobile_api import util
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.shortcuts import render
from mobile_api.models import Game
from mobile_api.serializers import GameSerializer
from django.shortcuts import redirect
import random
from django.db.models import Count

class List_Games(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def get(self, request):
    profile = util.get_profile_given_user_id(request.user.id)
    active_games = util.get_games_for_profile(profile, status=util.active)
    pending_games = util.get_players_for_profile(profile, status=util.pending)
    ended_games = util.get_games_for_profile(profile, status=util.ended)
    owned_games = util.get_games_for_profile(profile, status=util.owned)
    return render(request,"admin_list_games.html",{'active_games':active_games,'pending_games':pending_games,'ended_games':ended_games,'owned_games':owned_games})
    
class Edit_Game(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def get(self, request, game_id):
    game = Games.objects.find(id=game_id)
    return render(request, "admin_edit_game.html",{})

class Start_Game(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def post(self, request, game_id):
    game = util.get_game(game_id)
    if (int(game.game_status) > 1):
      print "TEST: already started"
      return redirect('/admin_panel/');
    player_ids = list(game.players.filter(accepted=True).values_list('id',flat=True))
    players = game.players.all()
    random.shuffle(player_ids)
    
    #make sure there are at least two players in a game
    if(len(player_ids) < 2):
      print "TEST not enough players only " + str(len(player_ids))
      return redirect('/admin_panel/');
    
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
    game.game_status=2
    game.save()
    print "TEST Success"
    return redirect('/admin_panel/');
    
class Friends(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def get(self,request):
    profile = util.get_profile_given_user_id(request.user.id)
    return render(request,"admin_friends.html",{'profile':profile,'friends':profile.friends.all()})

class Decline_Game(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def post(self, request, game_id):
    profile = util.get_profile_given_user_id(request.user.id)
    player = util.get_player_given_profile_game(profile.id, game_id)
    player.delete()
    return redirect('/admin_panel/');
    
class Accept_Game(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def post(self, request, game_id):
    profile = util.get_profile_given_user_id(request.user.id)
    player = util.get_player_given_profile_game(profile.id, game_id)
    player.accepted = True
    player.save()
    return redirect('/admin_panel/');
    
class Stats_AOL(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def get(self, request):
    counts = Assassinations.objects.values('target').annotate(dcount=Count('target')).order_by('dcount')[:10]
    results = {}
    for value in counts:
      profile = Player.objects.get(id=value["target"]).profile
      print profile.username
      if profile.username in results:
        results[str(profile.username)] = results[str(profile.username)] + value['dcount']
      else:
        results[str(profile.username)] = value['dcount']
    return render(request, "assassins_stats.html",{"results":results,"data":"Attempts On Life"})
    
class Stats_Attempts(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def get(self, request):
    counts = Assassinations.objects.values('player').annotate(dcount=Count('player')).order_by('dcount')[:10]
    results = {}
    for value in counts:
      profile = Player.objects.get(id=value["player"]).profile
      print profile.username
      if profile.username in results:
        results[str(profile.username)] = results[str(profile.username)] + value['dcount']
      else:
        results[str(profile.username)] = value['dcount']
    return render(request, "assassins_stats.html",{"results":results,"data":"Attempts"})
    
class Stats_Assassinations(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def get(self, request):
    counts = Assassinations.objects.filter(success=True).values('player').annotate(dcount=Count('player')).order_by('dcount')[:10]
    print "DEBUG " + str(len(Assassinations.objects.filter(success=True)))
    results = {}
    for value in counts:
      profile = Player.objects.get(id=value["player"]).profile
      print profile.username
      if profile.username in results:
        results[str(profile.username)] = results[str(profile.username)] + value['dcount']
      else:
        results[str(profile.username)] = value['dcount']
    return render(request, "assassins_stats.html",{"results":results,"data":"Assassinations"})
    
class Create_Game(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def get(self, request):
    return render(request, "admin_create_game.html",{})
    
  def post(self, request):
    data = request.DATA.copy()
    profile = util.get_profile_given_user_id(request.user.id)
    data.__setitem__('owner', profile.id)
    data.__setitem__('game_status','1')
    data.pop('csrfmiddlewaretoken')
    print data
    serializer = GameSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      serializer.save()
      game = serializer.object
      player = Player(game = game, profile = profile)
      player.save()
      return redirect('/admin_panel/');
    return render(request, "admin_create_game.html",{"errors":serializer.errors})