# Generated by Django 5.0 on 2024-05-17 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplication', '0005_emails_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emails',
            name='category',
            field=models.CharField(default='Queued', max_length=100),
        ),
    ]
