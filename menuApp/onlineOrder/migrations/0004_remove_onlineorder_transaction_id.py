# Generated by Django 2.2 on 2020-10-28 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineOrder', '0003_auto_20201028_0217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onlineorder',
            name='transaction_id',
        ),
    ]
