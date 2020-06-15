# Generated by Django 3.0.3 on 2020-06-15 19:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Use real name', max_length=70, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('email', models.EmailField(max_length=64, null=True, unique=True)),
                ('message', models.TextField(blank=True, max_length=300, null=True)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime(2020, 6, 15, 21, 18, 38, 160488), null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('review', models.TextField(blank=True, null=True)),
                ('date_reviewed', models.DateTimeField(blank=True, null=True)),
                ('is_favourite', models.BooleanField(default=False, verbose_name='Favourite?')),
                ('authors', models.ManyToManyField(related_name='books', to='books.Author')),
                ('comments', models.ManyToManyField(related_name='feedback', to='books.Comment')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
