# Generated by Django 4.2.6 on 2024-01-17 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passages', '0008_passage_haochen_database_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passage',
            name='haochen_database_id',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
    ]