# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Comment'
        db.create_table('links_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['links.Link'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('posted_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posted_by', to=orm['auth.User'])),
            ('posted_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('links', ['Comment'])

        # Adding M2M table for field reported_by on 'Comment'
        db.create_table('links_comment_reported_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm['links.comment'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('links_comment_reported_by', ['comment_id', 'user_id'])

        # Adding model 'Channel'
        db.create_table('links_channel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_tr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')()),
            ('description_tr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_official', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('links', ['Channel'])

        # Adding model 'LinkVote'
        db.create_table('links_linkvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['links.Link'])),
        ))
        db.send_create_signal('links', ['LinkVote'])

        # Adding model 'Link'
        db.create_table('links_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('posted_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('posted_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2048, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True, blank=True)),
            ('thumbnail_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('shown', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('player', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_banned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['links.Channel'])),
        ))
        db.send_create_signal('links', ['Link'])

        # Adding model 'Report'
        db.create_table('links_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reporter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['links.Link'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('reported_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('seen', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('links', ['Report'])


    def backwards(self, orm):
        
        # Deleting model 'Comment'
        db.delete_table('links_comment')

        # Removing M2M table for field reported_by on 'Comment'
        db.delete_table('links_comment_reported_by')

        # Deleting model 'Channel'
        db.delete_table('links_channel')

        # Deleting model 'LinkVote'
        db.delete_table('links_linkvote')

        # Deleting model 'Link'
        db.delete_table('links_link')

        # Deleting model 'Report'
        db.delete_table('links_report')


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
        'links.channel': {
            'Meta': {'object_name': 'Channel'},
            'description_en': ('django.db.models.fields.TextField', [], {}),
            'description_tr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_official': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_tr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'links.comment': {
            'Meta': {'object_name': 'Comment'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['links.Link']"}),
            'posted_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posted_by'", 'to': "orm['auth.User']"}),
            'reported_by': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'links.link': {
            'Meta': {'object_name': 'Link'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['links.Channel']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'player': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'posted_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'rating': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'shown': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'thumbnail_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'links.linkvote': {
            'Meta': {'ordering': "('date',)", 'object_name': 'LinkVote'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['links.Link']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'links.report': {
            'Meta': {'object_name': 'Report'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['links.Link']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'reported_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['links']
