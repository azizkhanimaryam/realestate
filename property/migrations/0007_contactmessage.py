# Generated by Django 5.0.6 on 2024-12-19 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_remove_apartment_image_remove_penthouse_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
