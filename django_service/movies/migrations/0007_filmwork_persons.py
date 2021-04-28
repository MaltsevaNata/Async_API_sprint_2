# Generated by Django 3.1 on 2021-03-07 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_remove_filmwork_persons'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonRole', to='movies.Person'),
        ),
    ]
