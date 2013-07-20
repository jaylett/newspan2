# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Label'
        db.create_table(u'feeds_label', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'feeds', ['Label'])

        # Adding model 'Feed'
        db.create_table(u'feeds_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1024)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_checked', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_error', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('last_contents', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'feeds', ['Feed'])

        # Adding M2M table for field labels on 'Feed'
        m2m_table_name = db.shorten_name(u'feeds_feed_labels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(orm[u'feeds.feed'], null=False)),
            ('label', models.ForeignKey(orm[u'feeds.label'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feed_id', 'label_id'])

        # Adding model 'Article'
        db.create_table(u'feeds_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('published', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('guid', self.gf('django.db.models.fields.TextField')()),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['feeds.Feed'])),
            ('as_json', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'feeds', ['Article'])


    def backwards(self, orm):
        # Deleting model 'Label'
        db.delete_table(u'feeds_label')

        # Deleting model 'Feed'
        db.delete_table(u'feeds_feed')

        # Removing M2M table for field labels on 'Feed'
        db.delete_table(db.shorten_name(u'feeds_feed_labels'))

        # Deleting model 'Article'
        db.delete_table(u'feeds_article')


    models = {
        u'feeds.article': {
            'Meta': {'object_name': 'Article'},
            'as_json': ('django.db.models.fields.TextField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': u"orm['feeds.Feed']"}),
            'guid': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
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