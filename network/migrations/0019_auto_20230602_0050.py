# Generated by Django 3.0.2 on 2023-06-02 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0018_alter_rating_rater_alter_rating_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]