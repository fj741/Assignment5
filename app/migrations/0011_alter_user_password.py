# Generated by Django 5.0 on 2023-12-12 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_user_email_alter_user_fname_alter_user_lname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]