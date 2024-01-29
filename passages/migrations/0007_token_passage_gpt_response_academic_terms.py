# Generated by Django 4.2.6 on 2024-01-17 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passages', '0006_alter_passage_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lemma', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='passage',
            name='gpt_response_academic_terms',
            field=models.TextField(blank=True, null=True),
        ),
    ]