# Generated by Django 3.1 on 2021-03-13 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0017_auto_20210310_2259'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='personrole',
            unique_together={('person', 'filmwork', 'role')},
        ),
    ]
