# Generated by Django 3.0.5 on 2020-10-04 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_remove_titles_rating'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
    ]