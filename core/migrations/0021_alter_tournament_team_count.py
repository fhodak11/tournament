# Generated by Django 4.2.7 on 2024-02-07 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='team_count',
            field=models.IntegerField(choices=[(4, 'Eight'), (8, 'Sixteen')]),
        ),
    ]
