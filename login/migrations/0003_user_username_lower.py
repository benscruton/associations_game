# Generated by Django 5.0.4 on 2024-05-24 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_user_email_disambiguated'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username_lower',
            field=models.CharField(default='', max_length=31),
            preserve_default=False,
        ),
    ]