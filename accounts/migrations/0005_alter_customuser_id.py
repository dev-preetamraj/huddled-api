# Generated by Django 4.2.7 on 2023-12-16 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_customuser_mobile_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
