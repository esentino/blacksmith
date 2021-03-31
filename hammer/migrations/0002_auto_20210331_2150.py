# Generated by Django 3.1.7 on 2021-03-31 21:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hammer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacksmith',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blacksmith', to=settings.AUTH_USER_MODEL),
        ),
    ]
