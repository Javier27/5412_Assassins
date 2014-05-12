from rest_framework import serializers
from mobile_api.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id','username','email')
    
class GameSerializer(serializers.ModelSerializer):
  players = serializers.PrimaryKeyRelatedField(many=True)
  class Meta:
    model = Game
    fields = ('name', 'owner', 'game_status', 'id')
    
class PlayerSerializer(serializers.ModelSerializer):
  target = serializers.PrimaryKeyRelatedField(many=False, required=False)
  assassination = serializers.PrimaryKeyRelatedField(many=True, required=False)
  assassination_attemps = serializers.PrimaryKeyRelatedField(many=True, required=False)
  class Meta:
    model = Player
    fields = ('alive','game','target','profile','accepted','id')

class LocationSerializer(serializers.Serializer):
  profile = serializers.IntegerField(required=True)
  latitude = serializers.FloatField(required=True)
  longitude = serializers.FloatField(required=True)

class AssassinationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Assassinations
    fields = ('player', 'success', 'target', 'longitude', 'latitude', 'timestamp', 'checked')
    
class PowerUpSerializer(serializers.ModelSerializer):
  class Meta:
    model = PowerUp
    fields = ('name','spawn_chance')
    
class InventorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Inventory
    fields = ('player','item')

class ProfileSerializer(serializers.ModelSerializer):
  players = serializers.PrimaryKeyRelatedField(many=True)
  games = serializers.PrimaryKeyRelatedField(many=True)
  def validate_username(self, attrs, source):
          """
          check username doesnt contain @.
          """
          value = attrs[source]
          if "@" in value.lower():
              raise serializers.ValidationError("Username cannot contain @")
          return attrs
  
  class Meta:
    model = Profile
    fields = ('id','friends','players','owned_games','user','username','email','picture')

class FriendSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('username','email','id','picture')