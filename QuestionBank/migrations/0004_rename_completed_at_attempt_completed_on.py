# Generated by Django 4.2.15 on 2024-08-29 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionBank', '0003_rename_name_test_title_test_created_on_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attempt',
            old_name='completed_at',
            new_name='completed_on',
        ),
    ]
