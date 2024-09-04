# Generated by Django 4.2.15 on 2024-08-29 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('QuestionBank', '0004_rename_completed_at_attempt_completed_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='test',
            name='description',
            field=models.CharField(default='description', max_length=500),
        ),
        migrations.AlterField(
            model_name='test',
            name='topic',
            field=models.CharField(default='Topic', max_length=100),
        ),
    ]
