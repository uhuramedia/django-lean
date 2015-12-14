# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Participant.user'
        db.alter_column(u'experiments_participant', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL))

    def backwards(self, orm):

        # Changing field 'Participant.user'
        db.alter_column(u'experiments_participant', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'experiments.anonymousvisitor': {
            'Meta': {'object_name': 'AnonymousVisitor'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'experiments.dailyconversionreport': {
            'Meta': {'object_name': 'DailyConversionReport'},
            'confidence': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'control_group_size': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['experiments.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overall_control_conversion': ('django.db.models.fields.IntegerField', [], {}),
            'overall_test_conversion': ('django.db.models.fields.IntegerField', [], {}),
            'test_group_size': ('django.db.models.fields.IntegerField', [], {})
        },
        u'experiments.dailyconversionreportgoaldata': {
            'Meta': {'object_name': 'DailyConversionReportGoalData'},
            'confidence': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'control_conversion': ('django.db.models.fields.IntegerField', [], {}),
            'goal_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['experiments.GoalType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'goal_data'", 'to': u"orm['experiments.DailyConversionReport']"}),
            'test_conversion': ('django.db.models.fields.IntegerField', [], {})
        },
        u'experiments.dailyengagementreport': {
            'Meta': {'object_name': 'DailyEngagementReport'},
            'confidence': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'control_group_size': ('django.db.models.fields.IntegerField', [], {}),
            'control_score': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['experiments.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'test_group_size': ('django.db.models.fields.IntegerField', [], {}),
            'test_score': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        u'experiments.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'start_date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'experiments.goalrecord': {
            'Meta': {'object_name': 'GoalRecord'},
            'anonymous_visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['experiments.AnonymousVisitor']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'goal_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['experiments.GoalType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'experiments.goaltype': {
            'Meta': {'object_name': 'GoalType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'experiments.participant': {
            'Meta': {'unique_together': "(('user', 'experiment'), ('anonymous_visitor', 'experiment'))", 'object_name': 'Participant'},
            'anonymous_visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['experiments.AnonymousVisitor']", 'null': 'True', 'blank': 'True'}),
            'enrollment_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['experiments.Experiment']"}),
            'group': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'})
        }
    }

    complete_apps = ['experiments']