# Generated by Django 3.0.1 on 2020-05-08 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
    ]