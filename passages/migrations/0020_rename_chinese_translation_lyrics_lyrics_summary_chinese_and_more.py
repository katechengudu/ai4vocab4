# Generated by Django 4.2.6 on 2024-04-04 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passages', '0019_alter_album_singer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lyrics',
            old_name='chinese_translation',
            new_name='lyrics_summary_chinese',
        ),
        migrations.RenameField(
            model_name='lyrics',
            old_name='english_translation',
            new_name='lyrics_summary_english',
        ),
    ]
