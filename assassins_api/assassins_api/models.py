from django.db import models
GAME_STATUS =[('1','pending'),('2','in_progress'),('3','over')]

class Game(models.Model):
  name = models.CharField(blank=False ,max_length=50)
  owner = models.ForeignKey('Profile', related_name='owned_games')
  status = models.CharField(max_length=100, choices=GAME_STATUS)
  
class Player(models.Model):
  alive = models.BooleanField(default=True)
  game = models.ForeignKey('Game', related_name='players')
  target = models.ForeignKey('Player', null=True)
  profile = models.ForeignKey('Profile', related_name='players')

class PowerUp(models.Model):
  name = models.CharField(max_length=100, unique=True)
  spawn_chance = models.DecimalField(decimal_places=3,max_digits=3)
  
class Inventory(models.Model):
  player = models.ForeignKey('Player', related_name='inventory')
  item = models.ForeignKey('PowerUp')
  
class Profile(models.Model):
  user = models.ForeignKey('auth.User', related_name='profile')
  email = models.EmailField(max_length=75)
  username = models.CharField(max_length=20, unique=True)
  friends = models.ManyToManyField('self', symmetrical=False, 
                                           related_name='friended_by', 
                                           null=True,)
  picture = models.TextField(null=True)