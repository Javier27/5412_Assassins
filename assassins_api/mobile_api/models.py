from django.db import models
from django.core.exceptions import ValidationError
GAME_STATUS =[('1','pending'),('2','in_progress'),('3','over')]

class Game(models.Model):
  name = models.CharField(blank=False ,max_length=50)
  owner = models.ForeignKey('Profile', related_name='owned_games', null=True)
  game_status = models.CharField(max_length=100, choices=GAME_STATUS, null=True)
  
class Player(models.Model):
  alive = models.BooleanField(default=True)
  game = models.ForeignKey('Game', related_name='players')
  target = models.ForeignKey('Player', null=True, blank=True)
  profile = models.ForeignKey('Profile', related_name='players')
  accepted = models.BooleanField(default=False)
  class Meta:
     unique_together = ('game', 'profile',)
  

class PowerUp(models.Model):
  name = models.CharField(max_length=100, unique=True)
  spawn_chance = models.DecimalField(decimal_places=3,max_digits=3)
  
class Inventory(models.Model):
  player = models.ForeignKey('Player', related_name='inventory')
  item = models.ForeignKey('PowerUp')
  
class Assassinations(models.Model):
  player = models.ForeignKey('Player', related_name='assassination')
  success = models.BooleanField(default=False, blank=True)
  target = models.ForeignKey('Player',related_name="assassination_attemp")
  longitude = models.FloatField()
  latitude = models.FloatField()
  checked = models.BooleanField(default=False, blank=True)
  timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  
class Profile(models.Model):
  user = models.ForeignKey('auth.User', related_name='profile')
  email = models.EmailField(max_length=75, unique=True)
  username = models.CharField(max_length=20, unique=True)
  friends = models.ManyToManyField('self', symmetrical=False, 
                                           related_name='friended_by', 
                                           null=True,)
  picture = models.TextField(null=True)
  
  def check_save(self):
    try:
      self.validate_unique()
    except ValidationError:
      self.user.delete()
    self.save()