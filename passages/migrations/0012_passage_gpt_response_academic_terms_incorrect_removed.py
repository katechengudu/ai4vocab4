# Generated by Django 4.2.6 on 2024-03-29 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passages', '0011_academicterm'),
    ]

    operations = [
        migrations.AddField(
            model_name='passage',
            name='gpt_response_academic_terms_incorrect_removed',
            field=models.TextField(blank=True, null=True),
        ),
    ]
