# Generated by Django 4.1.4 on 2022-12-28 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='user',
        ),
        migrations.DeleteModel(
            name='ServiceSalt',
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
    ]
