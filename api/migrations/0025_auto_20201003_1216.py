# Generated by Django 3.0.5 on 2020-10-03 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20201003_1215'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('author', 'title')},
        ),
    ]
