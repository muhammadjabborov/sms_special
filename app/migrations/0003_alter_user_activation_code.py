# Generated by Django 4.0.6 on 2022-07-27 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_user_managers_user_activation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_code',
            field=models.IntegerField(),
        ),
    ]
