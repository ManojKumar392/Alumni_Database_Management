# Generated by Django 4.2.6 on 2023-11-08 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Position',
            new_name='work',
        ),
        migrations.RenameField(
            model_name='jobopening',
            old_name='position',
            new_name='position_name',
        ),
    ]
