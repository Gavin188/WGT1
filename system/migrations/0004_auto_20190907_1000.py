# Generated by Django 2.2.2 on 2019-09-07 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_accessory'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='accessory',
            new_name='Access',
        ),
        migrations.RenameField(
            model_name='access',
            old_name='accessory',
            new_name='access',
        ),
    ]