# Generated by Django 4.2.7 on 2023-12-28 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_team_opponent_team_score_team_score_modified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='opponent',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
