# Generated by Django 5.1.4 on 2024-12-23 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_propertyvisit'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='code',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='penthouse',
            name='code',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='villa',
            name='code',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
