# Generated by Django 3.0.8 on 2020-07-09 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20200708_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='gender',
            field=models.CharField(blank=True, choices=[('man', 'Man'), ('woman', 'Woman')], default='m', help_text='Author gender', max_length=5),
        ),
    ]
