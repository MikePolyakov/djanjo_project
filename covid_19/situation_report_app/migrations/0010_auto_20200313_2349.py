# Generated by Django 3.0.3 on 2020-03-13 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('situation_report_app', '0009_article_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='source',
            field=models.CharField(max_length=16),
        ),
    ]