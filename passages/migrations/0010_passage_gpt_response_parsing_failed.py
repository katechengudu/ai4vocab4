# Generated by Django 4.2.6 on 2024-01-18 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passages', '0009_alter_passage_haochen_database_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='passage',
            name='gpt_response_parsing_failed',
            field=models.TextField(blank=True, null=True),
        ),
    ]
