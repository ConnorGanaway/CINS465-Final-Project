# Generated by Django 3.2.9 on 2021-12-09 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_usermodel_pending_mod_invites'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitymodel',
            name='ban_list',
            field=models.TextField(default='[]'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='pending_mod_invites',
            field=models.TextField(default='[]'),
        ),
    ]
