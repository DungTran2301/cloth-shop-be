# Generated by Django 4.1.7 on 2023-05-07 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_rename_cart_id_cartitem_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='user_id',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
