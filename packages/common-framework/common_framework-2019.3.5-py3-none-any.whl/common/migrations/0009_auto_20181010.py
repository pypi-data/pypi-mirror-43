# Generated by Django 2.1.2 on 2018-10-10 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20180302'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceusage',
            name='reset',
            field=models.CharField(choices=[('H', 'Toutes les heures'), ('D', 'Tous les jours'), ('W', 'Toutes les semaines'), ('M', 'Tous les mois'), ('Y', 'Tous les ans')], blank=True, max_length=1, verbose_name='réinitialisation'),
        ),
        migrations.AddField(
            model_name='serviceusage',
            name='reset_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date réinitialisation'),
        ),
    ]
