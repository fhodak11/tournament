# Generated by Django 4.2.7 on 2024-02-21 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_tournament_team_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='team_count',
            new_name='game_count',
        ),
    ]
