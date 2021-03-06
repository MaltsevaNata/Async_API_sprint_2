# Generated by Django 3.1 on 2021-03-07 20:38

import datetime

from django.db import migrations


def create_through_relations(apps, schema_editor):
    Filmwork = apps.get_model('movies', 'Filmwork')
    PersonRole = apps.get_model('movies', 'PersonRole')
    for film in Filmwork.objects.all():
        for person in PersonRole.person.objects.all():
            PersonRole(
                person=person,
                filmwork=film,
            ).save()

class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20210307_2338'),
    ]

    operations = [
        migrations.RunPython(create_through_relations, reverse_code=migrations.RunPython.noop),
    ]
