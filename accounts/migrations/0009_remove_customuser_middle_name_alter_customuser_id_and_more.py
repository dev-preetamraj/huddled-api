# Generated by Django 4.2.7 on 2023-12-16 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_customuser_id_alter_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='middle_name',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.CharField(default='huddled_user_70ccbe7c-ea59-4a8f-8cac-11ea57097794', max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='huddled_f60b8bf1-5b5c-4483-ba73-3f90a4d751d8', max_length=100, unique=True),
        ),
    ]