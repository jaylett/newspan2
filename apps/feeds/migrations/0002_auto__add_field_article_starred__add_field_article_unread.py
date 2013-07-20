# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.starred'
        db.add_column(u'feeds_article', 'starred',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Article.unread'
        db.add_column(u'feeds_article', 'unread',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Article.starred'
        db.delete_column(u'feeds_article', 'starred')

        # Deleting field 'Article.unread'
        db.delete_column(u'feeds_article', 'unread')


    models = {
        u'feeds.article': {
            'Meta': {'ordering': "('-updated',)", 'object_name': 'Article'},
            'as_json': ('django.db.models.fields.TextField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': u"orm['feeds.Feed']"}),
            'guid': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'starred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'feeds.feed': {
            'Meta': {'object_name': 'Feed'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'feeds'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['feeds.Label']"}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_contents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'last_error': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1024'})
        },
        u'feeds.label': {
            'Meta': {'object_name': 'Label'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['feeds']