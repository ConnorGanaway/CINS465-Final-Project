# Generated by Django 3.2.9 on 2021-12-07 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_messagemodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messagemodel',
            options={'ordering': ('-date_added',)},
        ),
        migrations.AddField(
            model_name='communitymodel',
            name='mod_list',
            field=models.TextField(default='[]'),
        ),
    ]