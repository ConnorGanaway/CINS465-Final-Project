# Generated by Django 3.2.9 on 2021-12-03 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_usermodel_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('room', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('date_added',),
            },
        ),
    ]
