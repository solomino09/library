# Generated by Django 3.0.8 on 2020-07-09 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20200709_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='publishing_year',
            field=models.IntegerField(blank=True, default='', help_text='year', verbose_name='year'),
        ),
    ]
