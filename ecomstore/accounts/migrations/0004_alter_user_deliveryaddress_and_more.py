# Generated by Django 4.1.7 on 2023-05-07 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_verifytoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='deliveryAddress',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='telephoneNumber',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]