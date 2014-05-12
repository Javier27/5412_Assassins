# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table('mobile_api_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owned_games', null=True, to=orm['mobile_api.Profile'])),
            ('game_status', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('mobile_api', ['Game'])

        # Adding model 'Player'
        db.create_table('mobile_api_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alive', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='players', to=orm['mobile_api.Game'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mobile_api.Player'], null=True, blank=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='players', to=orm['mobile_api.Profile'])),
            ('accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mobile_api', ['Player'])

        # Adding unique constraint on 'Player', fields ['game', 'profile']
        db.create_unique('mobile_api_player', ['game_id', 'profile_id'])

        # Adding model 'PowerUp'
        db.create_table('mobile_api_powerup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('spawn_chance', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=3)),
        ))
        db.send_create_signal('mobile_api', ['PowerUp'])

        # Adding model 'Inventory'
        db.create_table('mobile_api_inventory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inventory', to=orm['mobile_api.Player'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mobile_api.PowerUp'])),
        ))
        db.send_create_signal('mobile_api', ['Inventory'])

        # Adding model 'Assassinations'
        db.create_table('mobile_api_assassinations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assassination', to=orm['mobile_api.Player'])),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assassination_attemp', to=orm['mobile_api.Player'])),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('checked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('mobile_api', ['Assassinations'])

        # Adding model 'Profile'
        db.create_table('mobile_api_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='profile', to=orm['auth.User'])),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('picture', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('mobile_api', ['Profile'])

        # Adding M2M table for field friends on 'Profile'
        m2m_table_name = db.shorten_name('mobile_api_profile_friends')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_profile', models.ForeignKey(orm['mobile_api.profile'], null=False)),
            ('to_profile', models.ForeignKey(orm['mobile_api.profile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_profile_id', 'to_profile_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Player', fields ['game', 'profile']
        db.delete_unique('mobile_api_player', ['game_id', 'profile_id'])

        # Deleting model 'Game'
        db.delete_table('mobile_api_game')

        # Deleting model 'Player'
        db.delete_table('mobile_api_player')

        # Deleting model 'PowerUp'
        db.delete_table('mobile_api_powerup')

        # Deleting model 'Inventory'
        db.delete_table('mobile_api_inventory')

        # Deleting model 'Assassinations'
        db.delete_table('mobile_api_assassinations')

        # Deleting model 'Profile'
        db.delete_table('mobile_api_profile')

        # Removing M2M table for field friends on 'Profile'
        db.delete_table(db.shorten_name('mobile_api_profile_friends'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mobile_api.assassinations': {
            'Meta': {'object_name': 'Assassinations'},
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assassination'", 'to': "orm['mobile_api.Player']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assassination_attemp'", 'to': "orm['mobile_api.Player']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        'mobile_api.game': {
            'Meta': {'object_name': 'Game'},
            'game_status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owned_games'", 'null': 'True', 'to': "orm['mobile_api.Profile']"})
        },
        'mobile_api.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mobile_api.PowerUp']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory'", 'to': "orm['mobile_api.Player']"})
        },
        'mobile_api.player': {
            'Meta': {'unique_together': "(('game', 'profile'),)", 'object_name': 'Player'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['mobile_api.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['mobile_api.Profile']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mobile_api.Player']", 'null': 'True', 'blank': 'True'})
        },
        'mobile_api.powerup': {
            'Meta': {'object_name': 'PowerUp'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'spawn_chance': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '3'})
        },
        'mobile_api.profile': {
            'Meta': {'object_name': 'Profile'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'friended_by'", 'null': 'True', 'to': "orm['mobile_api.Profile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'to': "orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['mobile_api']