# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 21:56
from __future__ import unicode_literals

from django.db import migrations
import misago.core.pgutils


class Migration(migrations.Migration):

    dependencies = [
        ('misago_users', '0008_ban_registration_only'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='user',
            index=misago.core.pgutils.PgPartialIndex(fields=['is_staff'], name='misago_user_is_staf_bf68aa_part', where={'is_staff': True}),
        ),
        migrations.AddIndex(
            model_name='user',
            index=misago.core.pgutils.PgPartialIndex(fields=['requires_activation'], name='misago_user_require_05204a_part', where={'requires_activation__gt': 0}),
        ),
    ]