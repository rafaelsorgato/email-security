# Generated by Django 5.0 on 2024-03-05 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.TextField(choices=[('user', 'User'), ('admin', 'Admin'), ('custom', 'Custom')], default='user'),
        ),
    ]