# Generated by Django 4.2.1 on 2023-08-10 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_remove_customuser_senha_alter_customuser_points_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]