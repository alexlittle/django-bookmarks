# Generated by Django 5.1.3 on 2024-11-14 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatlog',
            name='thread',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]