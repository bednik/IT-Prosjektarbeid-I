# Generated by Django 2.1.2 on 2018-11-02 12:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='subscription_authors',
            field=models.ManyToManyField(related_name='subscription_authors', to=settings.AUTH_USER_MODEL),
        ),
    ]