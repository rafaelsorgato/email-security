# Generated by Django 5.0 on 2024-03-12 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplication', '0005_alter_account_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='picture',
            field=models.ImageField(blank=True, default='../static/img_uploads/default.png', null=True, upload_to='static/img_uploads'),
        ),
    ]