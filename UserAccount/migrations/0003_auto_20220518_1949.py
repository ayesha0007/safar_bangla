# Generated by Django 3.2.5 on 2022-05-18 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0002_auto_20220418_0204'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reserve_Room',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]
