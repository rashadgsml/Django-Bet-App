# Generated by Django 3.1.6 on 2021-02-07 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210207_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='odd',
            field=models.FloatField(default=1.5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='prediction',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Odds',
        ),
    ]